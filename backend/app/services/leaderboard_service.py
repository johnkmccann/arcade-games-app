"""
Leaderboard Service - Manages ranking and scoring

Supports:
- Global leaderboards (all-time, weekly, daily)
- Game-specific leaderboards
- Friend leaderboards
- Personal bests tracking
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models.score import ScoreLeaderboard

class LeaderboardService:
    """Service for leaderboard and ranking operations"""
    
    def __init__(self, db_client):
        self.db = db_client
        self.scores_collection = db_client.db.scores
        self.users_collection = db_client.db.users
    
    async def get_global_leaderboard(
        self, 
        game_id: str,
        time_period: str = "all_time",
        limit: int = 100,
        offset: int = 0
    ) -> List[ScoreLeaderboard]:
        """
        Get global leaderboard for a game
        
        Args:
            game_id: Which game's leaderboard
            time_period: 'all_time', 'weekly', 'daily'
            limit: How many results
            offset: For pagination
        
        Returns:
            List of leaderboard entries with rankings
        """
        # Calculate time window
        now = datetime.utcnow()
        if time_period == "daily":
            start_time = now - timedelta(days=1)
        elif time_period == "weekly":
            start_time = now - timedelta(days=7)
        else:  # all_time
            start_time = datetime.min
        
        # Query scores
        pipeline = [
            {
                "$match": {
                    "game_id": game_id,
                    "achieved_at": {"$gte": start_time}
                }
            },
            {
                "$sort": {"score_value": -1}
            },
            {
                "$skip": offset
            },
            {
                "$limit": limit
            },
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user_info"
                }
            },
            {
                "$unwind": "$user_info"
            },
            {
                "$project": {
                    "user_id": 1,
                    "score_value": 1,
                    "achieved_at": 1,
                    "play_duration_seconds": 1,
                    "username": "$user_info.username"
                }
            }
        ]
        
        scores = await self.scores_collection.aggregate(pipeline).to_list(None)
        
        # Add rank to each entry
        leaderboard = []
        for rank, score in enumerate(scores, start=offset + 1):
            leaderboard.append(ScoreLeaderboard(
                rank=rank,
                user_id=score['user_id'],
                username=score['username'],
                score_value=score['score_value'],
                achieved_at=score['achieved_at'],
                play_duration_seconds=score.get('play_duration_seconds')
            ))
        
        return leaderboard
    
    async def get_friend_leaderboard(
        self,
        user_id: str,
        game_id: str,
        include_self: bool = True
    ) -> List[ScoreLeaderboard]:
        """
        Get leaderboard showing only user's friends
        
        Args:
            user_id: The user viewing the leaderboard
            game_id: Which game
            include_self: Include the requesting user
        
        Returns:
            Sorted leaderboard of friends' scores
        """
        # Get user's friends
        user = await self.users_collection.find_one({"_id": user_id})
        if not user:
            return []
        
        friend_ids = user.get('friend_ids', [])
        if include_self:
            friend_ids.append(user_id)
        
        # Get best score for each friend in this game
        pipeline = [
            {
                "$match": {
                    "user_id": {"$in": friend_ids},
                    "game_id": game_id
                }
            },
            {
                "$sort": {"achieved_at": -1}
            },
            {
                "$group": {
                    "_id": "$user_id",
                    "score_value": {"$first": "$score_value"},
                    "achieved_at": {"$first": "$achieved_at"},
                    "play_duration_seconds": {"$first": "$play_duration_seconds"}
                }
            },
            {
                "$sort": {"score_value": -1}
            },
            {
                "$lookup": {
                    "from": "users",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "user_info"
                }
            },
            {
                "$unwind": "$user_info"
            },
            {
                "$project": {
                    "user_id": "$_id",
                    "score_value": 1,
                    "achieved_at": 1,
                    "play_duration_seconds": 1,
                    "username": "$user_info.username"
                }
            }
        ]
        
        scores = await self.scores_collection.aggregate(pipeline).to_list(None)
        
        leaderboard = []
        for rank, score in enumerate(scores, start=1):
            leaderboard.append(ScoreLeaderboard(
                rank=rank,
                user_id=score['user_id'],
                username=score['username'],
                score_value=score['score_value'],
                achieved_at=score['achieved_at'],
                play_duration_seconds=score.get('play_duration_seconds')
            ))
        
        return leaderboard
    
    async def get_user_best_score(self, user_id: str, game_id: str) -> Optional[Dict[str, Any]]:
        """Get a user's best score in a specific game"""
        score = await self.scores_collection.find_one(
            {"user_id": user_id, "game_id": game_id},
            sort=[("score_value", -1)]
        )
        return score
    
    async def get_user_rank(self, user_id: str, game_id: str) -> Optional[int]:
        """Get a user's rank in a game's global leaderboard"""
        # Count how many scores are better
        count = await self.scores_collection.count_documents({
            "game_id": game_id,
            "score_value": {
                "$gt": (await self.get_user_best_score(user_id, game_id) or {}).get('score_value', -1)
            }
        })
        return count + 1 if count or (await self.get_user_best_score(user_id, game_id)) else None
    
    async def get_user_game_stats(self, user_id: str, game_id: str) -> Dict[str, Any]:
        """
        Get comprehensive stats for a user in a specific game
        
        Returns stats like:
        - Best score
        - Average score
        - Total games played
        - Win rate (if applicable)
        - Current rank
        """
        # Aggregate stats
        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "game_id": game_id
                }
            },
            {
                "$group": {
                    "_id": None,
                    "best_score": {"$max": "$score_value"},
                    "average_score": {"$avg": "$score_value"},
                    "total_plays": {"$sum": 1},
                    "avg_duration": {"$avg": "$play_duration_seconds"},
                    "latest_score": {"$max": "$achieved_at"}
                }
            }
        ]
        
        stats = await self.scores_collection.aggregate(pipeline).to_list(1)
        
        if not stats:
            return {
                "user_id": user_id,
                "game_id": game_id,
                "best_score": None,
                "total_plays": 0
            }
        
        stat = stats[0]
        return {
            "user_id": user_id,
            "game_id": game_id,
            "best_score": stat.get('best_score'),
            "average_score": round(stat.get('average_score', 0), 2),
            "total_plays": stat.get('total_plays', 0),
            "avg_duration_seconds": round(stat.get('avg_duration', 0), 0),
            "rank": await self.get_user_rank(user_id, game_id),
            "last_played": stat.get('latest_score')
        }
    
    async def mark_personal_best(self, score_id: str, user_id: str, game_id: str) -> None:
        """Mark a score as a personal best"""
        # Check if this is actually the best
        best = await self.get_user_best_score(user_id, game_id)
        score = await self.scores_collection.find_one({"_id": score_id})
        
        if score and best and score['score_value'] >= best['score_value']:
            await self.scores_collection.update_one(
                {"_id": score_id},
                {"$set": {"is_record": True}}
            )
    
    async def get_top_games_by_plays(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the most-played games (by total sessions)"""
        pipeline = [
            {
                "$group": {
                    "_id": "$game_id",
                    "play_count": {"$sum": 1},
                    "avg_score": {"$avg": "$score_value"}
                }
            },
            {
                "$sort": {"play_count": -1}
            },
            {
                "$limit": limit
            }
        ]
        
        games = await self.scores_collection.aggregate(pipeline).to_list(limit)
        return games
    
    async def get_trending_games(self, days: int = 7, limit: int = 10) -> List[Dict[str, Any]]:
        """Get games with most activity in the last N days"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {
                "$match": {
                    "achieved_at": {"$gte": cutoff}
                }
            },
            {
                "$group": {
                    "_id": "$game_id",
                    "play_count": {"$sum": 1},
                    "unique_players": {"$addToSet": "$user_id"}
                }
            },
            {
                "$addFields": {
                    "unique_player_count": {"$size": "$unique_players"}
                }
            },
            {
                "$sort": {"unique_player_count": -1}
            },
            {
                "$limit": limit
            }
        ]
        
        games = await self.scores_collection.aggregate(pipeline).to_list(limit)
        return games


class UserGameProgressService:
    """Track user's progress across games"""
    
    def __init__(self, db_client):
        self.db = db_client
        self.sessions_collection = db_client.db.game_sessions
        self.scores_collection = db_client.db.scores
    
    async def get_user_favorites(self, user_id: str) -> List[str]:
        """Get user's favorite games"""
        from app.models.user import User
        user = await self.db.db.users.find_one({"_id": user_id})
        if user:
            return user.get('favorite_game_ids', [])
        return []
    
    async def get_user_unfinished_games(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's games in progress"""
        sessions = await self.sessions_collection.find({
            "user_id": user_id,
            "status": "in_progress"
        }).to_list(None)
        return [dict(s) for s in sessions]
    
    async def get_user_recent_scores(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's most recent scores"""
        scores = await self.scores_collection.find(
            {"user_id": user_id}
        ).sort("achieved_at", -1).limit(limit).to_list(limit)
        return [dict(s) for s in scores]
