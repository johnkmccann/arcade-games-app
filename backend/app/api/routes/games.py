"""
Games API routes - Handles all game-related endpoints

Supports:
- Listing available games (filtered by user access)
- Getting game details
- Starting new game sessions
- Processing moves in active games
- Finishing/saving games
"""

import logging
from fastapi import APIRouter, HTTPException, Depends, Query, Body
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import uuid

from app.models.game import Game, GameMetadata, GameSession
from app.services.game_adapter import GameRegistry
from app.services.game_session_service import GameSessionService, GameAccessControl
from app.services.leaderboard_service import LeaderboardService

logger = logging.getLogger(__name__)

# Request models
class StartGameRequest(BaseModel):
    """Request body for starting a game"""
    players: Optional[List[str]] = None

# In-memory session storage (temporary, until database is connected)
_game_sessions: Dict[str, GameSession] = {}

router = APIRouter(prefix="/games", tags=["games"])

# In production, these would be injected from a DI container
async def get_game_session_service():
    """Get game session service"""
    # This would come from your database client
    from app.config import db_client
    return GameSessionService(db_client)

async def get_access_control():
    """Get access control service"""
    from app.config import db_client
    return GameAccessControl(db_client)

async def get_leaderboard_service():
    """Get leaderboard service"""
    from app.config import db_client
    return LeaderboardService(db_client)


@router.get("", response_model=List[GameMetadata])
async def get_available_games(
    user_id: Optional[str] = Query(None, description="If provided, only return games user can access")
):
    """
    Get all available games.
    
    If user_id provided, respects access control rules (age restrictions, game bans, etc.)
    """
    games = GameRegistry.list_all()
    
    if user_id:
        access_control = await get_access_control()
        # Filter by access
        games = [g for g in games if access_control.can_play_game(user_id, g.id)]
    
    return games


@router.get("/{game_id}", response_model=GameMetadata)
async def get_game(game_id: str, user_id: Optional[str] = Query(None)):
    """Get detailed information about a specific game"""
    adapter = GameRegistry.get(game_id)
    if not adapter:
        raise HTTPException(status_code=404, detail=f"Game '{game_id}' not found")
    
    metadata = adapter.get_metadata()
    
    # Check access if user provided
    if user_id:
        access_control = await get_access_control()
        can_play = await access_control.can_play_game(user_id, game_id)
        if not can_play:
            raise HTTPException(status_code=403, detail=f"User does not have access to '{game_id}'")
    
    return metadata


@router.post("/{game_id}/start", response_model=GameSession)
async def start_game(
    game_id: str,
    user_id: str = Query(...),
    difficulty: Optional[str] = Query(None),
    request_data: Optional[StartGameRequest] = Body(None)
):
    """
    Start a new game session
    
    For multi-player games like Darts, pass players array in request body:
    {
        "players": ["Player1", "Player2", ...]
    }
    
    Returns the initialized GameSession with starting game_state
    """
    logger.info(f"\n🎮 START_GAME endpoint called")
    logger.info(f"  game_id: {game_id}")
    logger.info(f"  user_id: {user_id}")
    logger.info(f"  difficulty: {difficulty}")
    logger.info(f"  request_data: {request_data}")
    
    try:
        # Check if game exists
        logger.info(f"  Checking if game '{game_id}' is registered...")
        if not GameRegistry.is_registered(game_id):
            logger.error(f"  ❌ Game '{game_id}' not found in registry")
            raise HTTPException(status_code=404, detail=f"Game '{game_id}' not found")
        logger.info(f"  ✓ Game registered")
        
        # Check access
        logger.info(f"  Checking access control...")
        access_control = await get_access_control()
        can_play = await access_control.can_play_game(user_id, game_id)
        logger.info(f"  Access check result: {can_play}")
        if not can_play:
            logger.error(f"  ❌ User '{user_id}' cannot play '{game_id}'")
            raise HTTPException(status_code=403, detail=f"User does not have access to play '{game_id}'")
        logger.info(f"  ✓ User has access")
        
        # Create session
        logger.info(f"  Creating game session...")
        service = await get_game_session_service()
        try:
            # Extract players from request body if provided (for multi-player games)
            players_list = None
            if request_data and request_data.players:
                players_list = request_data.players
                logger.info(f"  Players from request: {players_list}")
            
            # For Darts specifically, handle multiple players
            if game_id == 'darts' and players_list:
                logger.info(f"  Creating Darts game with {len(players_list)} players")
                # Create game state with all players
                game_state = {
                    'players': [
                        {'user_id': name, 'score': 501, 'status': 'active', 'busted': False}
                        for name in players_list
                    ],
                    'current_player_index': 0,
                    'turn_darts': [],
                    'turn_start_score': 501,
                    'history': [],
                    'game_status': 'active',
                    'winner_user_id': None
                }
                logger.info(f"  Game state created: {game_state}")
                
                logger.info(f"  Creating GameSession object...")
                session = GameSession(
                    id=str(uuid.uuid4()),
                    game_id=game_id,
                    user_id=user_id,
                    game_state=game_state,
                    status='in_progress'
                )
                logger.info(f"  ✓ GameSession object created: {session.id}")
                
                # Store in memory for now
                logger.info(f"  Storing session in memory...")
                _game_sessions[session.id] = session
                logger.info(f"  ✓ Session stored")
                
                logger.info(f"  ✅ Returning session: {session}")
                return session
            else:
                logger.info(f"  Creating session via service (non-Darts or no players list)")
                session = await service.start_game(user_id, game_id, difficulty)
                logger.info(f"  ✅ Session created: {session.id}")
                return session
        except ValueError as e:
            logger.error(f"  ❌ ValueError in game creation: {str(e)}", exc_info=True)
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"  ❌ Unexpected error in game creation: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Error creating game: {str(e)}")
    except HTTPException as e:
        logger.error(f"  ❌ HTTP Exception: {e.status_code} - {e.detail}")
        raise
    except Exception as e:
        logger.error(f"  ❌ Unexpected error in start_game: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/{game_id}/sessions/{session_id}/move")
async def make_move(
    game_id: str,
    session_id: str,
    move: Dict[str, Any] = Body(...)
):
    """
    Process a move in an active game
    
    Returns updated game state and win/loss status
    """
    # Check in-memory store first
    if session_id in _game_sessions:
        session = _game_sessions[session_id]
        if session.game_id != game_id:
            raise HTTPException(status_code=404, detail="Session does not match game")
        
        # Use the game adapter to process the move
        adapter = GameRegistry.get(game_id)
        if not adapter:
            raise HTTPException(status_code=404, detail=f"Game '{game_id}' not found")
        
        try:
            updated_state = adapter.process_move(session.game_state, move)
            session.game_state = updated_state
            
            # Check if game is over
            is_over, winner = adapter.is_game_over(updated_state)
            if is_over:
                session.status = 'completed'
            
            # Store updated session
            _game_sessions[session_id] = session
            
            return {
                "game_state": updated_state,
                "is_game_over": is_over,
                "winner": winner
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    # Fall back to database service
    service = await get_game_session_service()
    
    try:
        updated_session, is_over, winner = await service.process_move(session_id, move)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {
        "game_state": updated_session.game_state,
        "is_game_over": is_over,
        "winner": winner if is_over else None
    }


@router.post("/{game_id}/sessions/{session_id}/finish")
async def finish_game(game_id: str, session_id: str):
    """Finish a game session and save score to leaderboard"""
    service = await get_game_session_service()
    
    try:
        session = await service.save_and_finish_game(session_id)
        return {
            "session": session,
            "score": session.score,
            "score_breakdown": session.score_breakdown
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{game_id}/sessions/{session_id}")
async def get_game_session(game_id: str, session_id: str):
    """Get current state of a game session"""
    # Check in-memory store first
    if session_id in _game_sessions:
        session = _game_sessions[session_id]
        if session.game_id != game_id:
            raise HTTPException(status_code=404, detail="Session does not match game")
        return session
    
    # Fall back to database service
    service = await get_game_session_service()
    session = await service.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    
    if session.game_id != game_id:
        raise HTTPException(status_code=404, detail="Session does not match game")
    
    return session


@router.get("/{game_id}/leaderboard")
async def get_game_leaderboard(
    game_id: str,
    time_period: str = Query("all_time", pattern="^(all_time|weekly|daily)$"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get global leaderboard for a game"""
    if not GameRegistry.is_registered(game_id):
        raise HTTPException(status_code=404, detail=f"Game '{game_id}' not found")
    
    leaderboard_service = await get_leaderboard_service()
    try:
        leaderboard = await leaderboard_service.get_global_leaderboard(
            game_id, time_period, limit, offset
        )
        return {"game_id": game_id, "leaderboard": leaderboard, "time_period": time_period}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{game_id}/leaderboard/friends")
async def get_friend_leaderboard(
    game_id: str,
    user_id: str = Query(...),
    include_self: bool = Query(True)
):
    """Get leaderboard showing only user's friends for a game"""
    if not GameRegistry.is_registered(game_id):
        raise HTTPException(status_code=404, detail=f"Game '{game_id}' not found")
    
    leaderboard_service = await get_leaderboard_service()
    try:
        leaderboard = await leaderboard_service.get_friend_leaderboard(
            user_id, game_id, include_self
        )
        return {"game_id": game_id, "leaderboard": leaderboard}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{game_id}/user/{user_id}/stats")
async def get_user_game_stats(game_id: str, user_id: str):
    """Get a user's stats for a specific game"""
    if not GameRegistry.is_registered(game_id):
        raise HTTPException(status_code=404, detail=f"Game '{game_id}' not found")
    
    leaderboard_service = await get_leaderboard_service()
    try:
        stats = await leaderboard_service.get_user_game_stats(user_id, game_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{game_id}/user/{user_id}/history")
async def get_user_game_history(
    game_id: str,
    user_id: str,
    limit: int = Query(50, ge=1, le=500)
):
    """Get a user's completed game sessions for a specific game"""
    if not GameRegistry.is_registered(game_id):
        raise HTTPException(status_code=404, detail=f"Game '{game_id}' not found")
    
    service = await get_game_session_service()
    try:
        history = await service.get_user_game_history(user_id, game_id, limit)
        return {"game_id": game_id, "user_id": user_id, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
