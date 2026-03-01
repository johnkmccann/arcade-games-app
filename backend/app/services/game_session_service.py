"""
Game Session Service - Manages game lifecycle

Handles creating sessions, processing moves, calculating scores,
and persisting game progress to database.
"""

from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from app.models.game import GameSession, GameMetadata
from app.models.score import Score
from app.services.game_adapter import GameRegistry
import time

class GameSessionService:
    """Service for managing game sessions"""
    
    def __init__(self, db_client):
        """Initialize with database client"""
        self.db = db_client
        self.sessions_collection = db_client.db.game_sessions
        self.scores_collection = db_client.db.scores
        self.games_collection = db_client.db.games
    
    async def start_game(self, user_id: str, game_id: str, difficulty: Optional[str] = None) -> GameSession:
        """
        Start a new game session for a user
        
        Args:
            user_id: The player starting the game
            game_id: Which game to play
            difficulty: Optional difficulty level
            
        Returns:
            GameSession with initialized game_state
        """
        # Get game adapter
        adapter = GameRegistry.get(game_id)
        if not adapter:
            raise ValueError(f"Game '{game_id}' not found")
        
        # Create initial game state
        game_state = adapter.create_new_game(user_id, difficulty)
        
        # Create session
        session = GameSession(
            user_id=user_id,
            game_id=game_id,
            status="in_progress",
            game_state=game_state
        )
        
        # Save to database
        result = await self.sessions_collection.insert_one(session.model_dump(by_alias=False))
        session.id = str(result.inserted_id)
        
        return session
    
    async def process_move(self, session_id: str, move: Dict[str, Any]) -> Tuple[GameSession, bool, Optional[str]]:
        """
        Process a move in an active game
        
        Args:
            session_id: The game session ID
            move: The move to process
            
        Returns:
            (updated_session, is_game_over, winner_user_id)
        """
        # Get current session
        session = await self.sessions_collection.find_one({"_id": session_id})
        if not session:
            raise ValueError(f"Session '{session_id}' not found")
        
        session = GameSession(**session)
        
        if session.status != "in_progress":
            raise ValueError(f"Cannot move in '{session.status}' game")
        
        # Get game adapter
        adapter = GameRegistry.get(session.game_id)
        if not adapter:
            raise ValueError(f"Game '{session.game_id}' not found")
        
        # Process move
        try:
            updated_state = adapter.process_move(session.game_state, move)
        except ValueError as e:
            raise ValueError(f"Invalid move: {str(e)}")
        
        # Check if game is over
        is_over, winner = adapter.is_game_over(updated_state)
        
        if is_over:
            session.status = "completed"
            session.completed_at = datetime.utcnow()
            
            # Calculate score
            duration = (session.completed_at - session.started_at).total_seconds()
            score_data = adapter.calculate_score(updated_state, int(duration))
            
            session.score = score_data['score_value']
            session.score_breakdown = score_data.get('score_breakdown')
            session.game_state = updated_state
        else:
            session.game_state = updated_state
        
        # Save updated session
        await self.sessions_collection.update_one(
            {"_id": session_id},
            {"$set": session.model_dump(by_alias=False, exclude={'id'})}
        )
        
        return session, is_over, winner
    
    async def get_session(self, session_id: str) -> Optional[GameSession]:
        """Get a game session by ID"""
        session = await self.sessions_collection.find_one({"_id": session_id})
        if session:
            session['id'] = str(session.pop('_id'))
            return GameSession(**session)
        return None
    
    async def save_and_finish_game(self, session_id: str) -> GameSession:
        """
        Finish a game session and save score to leaderboard
        
        Args:
            session_id: The session to finish
            
        Returns:
            Updated session
        """
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session '{session_id}' not found")
        
        if session.status == "completed":
            # Already finished
            return session
        
        # Mark as completed
        session.status = "completed"
        session.completed_at = datetime.utcnow()
        
        # Get game adapter for final score calculation
        adapter = GameRegistry.get(session.game_id)
        if adapter and session.score is None:
            duration = (session.completed_at - session.started_at).total_seconds()
            score_data = adapter.calculate_score(session.game_state, int(duration))
            session.score = score_data['score_value']
            session.score_breakdown = score_data.get('score_breakdown')
        
        # Save session
        await self.sessions_collection.update_one(
            {"_id": session_id},
            {"$set": session.model_dump(by_alias=False, exclude={'id'})}
        )
        
        # Save score to leaderboard only if score exists
        if session.score is not None:
            score = Score(
                user_id=session.user_id,
                game_id=session.game_id,
                game_session_id=session_id,
                score_value=session.score,
                score_type=session.game_id,  # Can be more specific
                score_breakdown=session.score_breakdown,
                final_game_state=session.game_state,
                play_duration_seconds=int((session.completed_at - session.started_at).total_seconds())
            )
            
            await self.scores_collection.insert_one(score.model_dump(by_alias=False))
        
        return session
    
    async def get_user_active_session(self, user_id: str) -> Optional[GameSession]:
        """Get the active game session for a user (if any)"""
        session = await self.sessions_collection.find_one({
            "user_id": user_id,
            "status": "in_progress"
        })
        if session:
            session['id'] = str(session.pop('_id'))
            return GameSession(**session)
        return None
    
    async def get_user_game_history(self, user_id: str, game_id: Optional[str] = None, limit: int = 50) -> list[GameSession]:
        """Get a user's completed game sessions"""
        query = {"user_id": user_id, "status": "completed"}
        if game_id:
            query["game_id"] = game_id
        
        sessions = await self.sessions_collection.find(query).limit(limit).sort("completed_at", -1).to_list(limit)
        return [GameSession(**{**s, 'id': str(s.pop('_id'))}) for s in sessions]
    
    async def validate_session_integrity(self, session_id: str) -> bool:
        """
        Validate that a session's game_state is still valid
        Useful for recovery after crashes
        """
        session = await self.get_session(session_id)
        if not session:
            return False
        
        adapter = GameRegistry.get(session.game_id)
        if not adapter:
            return False
        
        return adapter.validate_game_state(session.game_state)
    
    async def get_unfinished_games(self, user_id: str) -> list[GameSession]:
        """Get all in-progress game sessions for a user"""
        sessions = await self.sessions_collection.find({
            "user_id": user_id,
            "status": "in_progress"
        }).to_list(None)
        return [GameSession(**{**s, 'id': str(s.pop('_id'))}) for s in sessions]


class GameAccessControl:
    """Manages who can play which games"""
    
    def __init__(self, db_client):
        self.db = db_client
        self.users_collection = db_client.db.users
        self.game_access_rules = db_client.db.game_access_rules
    
    async def can_play_game(self, user_id: str, game_id: str) -> bool:
        """
        Check if a user has access to a game
        
        Respects:
        - User's accessible_game_ids list
        - User's age_group restrictions
        - Game's required_age_group
        
        For development/testing without a database, allows all games for all users.
        """
        try:
            # Get user
            user = await self.users_collection.find_one({"_id": user_id})
            if not user:
                # User doesn't exist in database - allow access for development
                return True
            
            # Check explicit access list
            if user.get('restricted_games'):
                return game_id in user.get('accessible_game_ids', [])
            
            # Check age-based restrictions
            user_age = user.get('age_group')
            rule = await self.game_access_rules.find_one({"game_id": game_id})
            if rule and 'required_min_age' in rule:
                age_order = {'kid': 0, 'teen': 1, 'adult': 2}
                user_age_val = age_order.get(user_age, 0)
                required_val = age_order.get(rule['required_min_age'], 0)
                if user_age_val < required_val:
                    return False
            
            # If not explicitly restricted, user can play
            return True
        except Exception as e:
            # If database is down or any error occurs, allow access for development
            print(f"Warning: Database error in access control: {e}")
            return True
    
    async def set_game_access(self, user_id: str, game_ids: list[str]) -> None:
        """Set which games a user can access (whitelist mode)"""
        await self.users_collection.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "accessible_game_ids": game_ids,
                    "restricted_games": True
                }
            }
        )
    
    async def remove_game_restriction(self, user_id: str) -> None:
        """Allow user to access all non-age-restricted games"""
        await self.users_collection.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "accessible_game_ids": [],
                    "restricted_games": False
                }
            }
        )
    
    async def set_game_age_requirement(self, game_id: str, min_age_group: str) -> None:
        """
        Set age requirement for a game
        
        Args:
            game_id: The game
            min_age_group: 'kid', 'teen', or 'adult'
        """
        await self.game_access_rules.update_one(
            {"game_id": game_id},
            {"$set": {"required_min_age": min_age_group}},
            upsert=True
        )
