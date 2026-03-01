from typing import Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId

class Score(BaseModel):
    """Score entry supporting various scoring systems"""
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
    user_id: str = Field(..., description="Reference to user")
    game_id: str = Field(..., description="Reference to game")
    game_session_id: Optional[str] = Field(None, description="Reference to game session if from active play")
    
    # Flexible score representation
    score_value: float = Field(..., description="Primary score metric")
    score_type: str = Field(..., description="Type: 'points', 'time', 'rating', 'moves', etc.")
    
    # Detailed scoring breakdown for complex games
    score_breakdown: Optional[Dict[str, Any]] = Field(
        None,
        description="Details like {'base_points': 100, 'multiplier': 2, 'bonus': 50, 'time_bonus': 25}"
    )
    
    # Game state snapshot (optional - useful for replays)
    final_game_state: Optional[Dict[str, Any]] = None
    
    # Metadata
    achieved_at: datetime = Field(default_factory=datetime.utcnow)
    play_duration_seconds: Optional[int] = None
    is_record: bool = False  # Marks if this is a personal best
    
    # Additional context
    difficulty_level: Optional[str] = None  # e.g., 'easy', 'normal', 'hard'
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "game_id": "tetris",
                "score_value": 42500,
                "score_type": "points",
                "score_breakdown": {
                    "lines_cleared": 42,
                    "level": 10,
                    "base_points": 40000,
                    "level_bonus": 2500
                },
                "play_duration_seconds": 180,
                "is_record": True
            }
        }


class ScoreLeaderboard(BaseModel):
    """Leaderboard entry with rank"""
    rank: int
    user_id: str
    username: str
    score_value: float
    achieved_at: datetime
    play_duration_seconds: Optional[int] = None
    rank_change: Optional[int] = None  # +/- from previous rank


class ScoreFilter(BaseModel):
    """Filters for score queries"""
    game_id: Optional[str] = None
    user_id: Optional[str] = None
    time_period_days: Optional[int] = None  # Last N days
    min_score: Optional[float] = None
    max_score: Optional[float] = None
    difficulty_level: Optional[str] = None
    limit: int = 100
    offset: int = 0