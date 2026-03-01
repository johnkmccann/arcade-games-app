from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

class User(BaseModel):
    """User model with game access control and preferences"""
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    password_hash: str  # Always hashed, never store plain text
    disabled: bool = False
    
    # Game access control - determines which games user can access
    accessible_game_ids: List[str] = Field(default_factory=list, description="List of game IDs user has access to")
    restricted_games: bool = False  # If True, use accessible_game_ids as whitelist. If False, user can access all non-restricted games
    
    # Preferences and social features  
    favorite_game_ids: List[str] = Field(default_factory=list)
    friend_ids: List[str] = Field(default_factory=list)
    blocked_user_ids: List[str] = Field(default_factory=list)
    
    # Game progress tracking
    current_game_session_id: Optional[str] = None  # ID of active game session
    
    # Profile
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    age_group: Optional[str] = None  # Used for game access control (e.g., 'kid', 'teen', 'adult')
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "player123",
                "email": "player@example.com",
                "full_name": "John Doe",
                "accessible_game_ids": ["chess", "tetris", "pac-man"],
                "favorite_game_ids": ["chess"],
                "age_group": "adult"
            }
        }


class UserPublic(BaseModel):
    """Public user profile - safe to share"""
    id: str
    username: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserCredentials(BaseModel):
    """Login request model"""
    username: str
    password: str