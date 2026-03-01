import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.routes import games as games_module
from app.models.game import Game

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_games():
    """Reset games list before each test"""
    games_module.games = [
        Game(id='chess', title='Chess', genre='Strategy'),
        Game(id='tetris', title='Tetris', genre='Puzzle'),
        Game(id='pac-man', title='Pac-Man', genre='Arcade')
    ]
    yield
    # Cleanup after test
    games_module.games = [
        Game(id='chess', title='Chess', genre='Strategy'),
        Game(id='tetris', title='Tetris', genre='Puzzle'),
        Game(id='pac-man', title='Pac-Man', genre='Arcade')
    ]


# Test the GET /games endpoint

def test_get_games():
    response = client.get('/games')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test the POST /games endpoint

def test_create_game():
    new_game = {'id': 'test-game', 'title': 'Test Game', 'genre': 'Arcade'}
    response = client.post('/games', json=new_game)
    assert response.status_code == 201
    assert response.json()['id'] == 'test-game'
    assert response.json()['title'] == 'Test Game'
    assert response.json()['genre'] == 'Arcade'

# Test POST /games with duplicate ID (should fail)

def test_create_game_duplicate_id():
    new_game = {'id': 'chess', 'title': 'Chess Duplicate', 'genre': 'Strategy'}
    response = client.post('/games', json=new_game)
    assert response.status_code == 409
    assert "already exists" in response.json()['detail']

# Test the GET /games/{id} endpoint

def test_get_game_by_id():
    response = client.get('/games/chess')
    assert response.status_code == 200
    assert response.json()['id'] == 'chess'

# Test the DELETE /games/{id} endpoint

def test_delete_game():
    response = client.delete('/games/chess')
    assert response.status_code == 204

# Test updating a game

def test_update_game():
    updated_game = {'id': 'chess', 'title': 'Updated Chess', 'genre': 'Strategy'}
    response = client.put('/games/chess', json=updated_game)
    assert response.status_code == 200
    assert response.json()['title'] == 'Updated Chess'
    assert response.json()['genre'] == 'Strategy'

# Test getting a non-existent game

def test_get_nonexistent_game():
    response = client.get('/games/nonexistent')
    assert response.status_code == 404
    assert "not found" in response.json()['detail']
