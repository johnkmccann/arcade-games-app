from pydantic import BaseModel

class Game(BaseModel):
    id: int
    title: str
    genre: str
    release_year: int
    rating: float
    description: str = None
    developer: str = None
    publisher: str = None
