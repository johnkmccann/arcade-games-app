from typing import Optional, Any, Dict, List
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId

class GameMetadata(BaseModel):
    """Metadata about a game - shared across all instances"""
    id: str = Field(..., description="Unique game identifier (e.g., 'chess', 'tetris')")
    title: str
    genre: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    developer: Optional[str] = None
    publisher: Optional[str] = None
    rating: Optional[float] = None
    thumbnail_url: Optional[str] = None
    
    # Game implementation details - defines how this game is played
    game_type: str = Field(..., description="Type of game: 'arcade', 'boardgame', 'puzzle', etc.")
    min_players: int = 1
    max_players: int = 1
    avg_playtime_minutes: Optional[int] = None
    
    # Scoring configuration - different games have different scoring
    scoring_type: str = Field(..., description="'points', 'time', 'rating', 'custom'")
    scoring_direction: str = Field(default="higher_better", description="'higher_better' or 'lower_better'")
    max_score: Optional[float] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "chess",
                "title": "Chess",
                "genre": "Strategy",
                "game_type": "boardgame",
                "scoring_type": "points",
                "scoring_direction": "higher_better"
            }
        }


class GameSession(BaseModel):
    """Represents an active or completed game session"""
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
    user_id: str
    game_id: str  # Reference to GameMetadata
    
    # Session state
    status: str = Field(default="in_progress", description="'in_progress', 'completed', 'abandoned'")
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    # Generic game state - each game stores its state differently
    game_state: Dict[str, Any] = Field(default_factory=dict, description="JSON-serializable game state")
    
    # Flexible scoring - accommodates different scoring systems
    score: Optional[float] = None
    score_breakdown: Optional[Dict[str, Any]] = None  # e.g., {"points": 100, "multiplier": 2, "bonus": 50}
    
    # Metadata
    is_multiplayer: bool = False
    other_players: List[str] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "game_id": "chess",
                "status": "in_progress",
                "game_state": {"board": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", "turn": "white"},
                "score": None
            }
        }


class Game(BaseModel):
    """Backward compatibility model - can be either metadata or session"""
    id: str
    title: str
    genre: str
    release_year: Optional[int] = None
    rating: Optional[float] = None
    description: Optional[str] = None
    developer: Optional[str] = None
    publisher: Optional[str] = None
