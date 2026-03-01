from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/games", tags=["games"])

games = [
    {'id': 1, 'title': 'Chess', 'genre': 'Strategy'},
    {'id': 2, 'title': 'Tetris', 'genre': 'Puzzle'},
    {'id': 3, 'title': 'Pac-Man', 'genre': 'Arcade'}
]

class Game(BaseModel):
    title: str
    genre: str

@router.get("", response_model=List[dict])
async def get_games():
    return games

@router.get("/{game_id}")
async def get_game(game_id: int):
    game = next((game for game in games if game['id'] == game_id), None)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.post("", status_code=201)
async def add_game(game: Game):
    new_game = game.model_dump()
    new_game['id'] = max([g['id'] for g in games]) + 1 if games else 1
    games.append(new_game)
    return new_game

@router.put("/{game_id}")
async def update_game(game_id: int, game: Game):
    game_obj = next((g for g in games if g['id'] == game_id), None)
    if not game_obj:
        raise HTTPException(status_code=404, detail="Game not found")
    game_obj.update(game.model_dump())
    return game_obj

@router.delete("/{game_id}", status_code=204)
async def delete_game(game_id: int):
    global games
    original_len = len(games)
    games = [game for game in games if game['id'] != game_id]
    if len(games) == original_len:
        raise HTTPException(status_code=404, detail="Game not found")