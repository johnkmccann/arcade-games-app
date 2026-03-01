import pytest
from fastapi.testclient import TestClient
from app import main

client = TestClient(main.app)


# Test the GET /games endpoint

def test_get_games():
    response = client.get('/games')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test the POST /games endpoint

def test_create_game():
    new_game = {'title': 'Test Game', 'genre': 'Arcade'}
    response = client.post('/games', json=new_game)
    assert response.status_code == 201
    assert response.json()['title'] == 'Test Game'
    assert response.json()['genre'] == 'Arcade'

# Test the GET /games/{id} endpoint

def test_get_game_by_id():
    response = client.get('/games/1')  # Assuming a game with ID 1 exists
    assert response.status_code == 200
    assert response.json()['id'] == 1

# Test the DELETE /games/{id} endpoint

def test_delete_game():
    response = client.delete('/games/1')  # Assuming a game with ID 1 exists
    assert response.status_code == 204

# Test updating a game

def test_update_game():
    updated_game = {'title': 'Updated Game', 'genre': 'Puzzle'}
    response = client.put('/games/1', json=updated_game)  # Assuming a game with ID 1 exists
    assert response.status_code == 200
    assert response.json()['title'] == 'Updated Game'
    assert response.json()['genre'] == 'Puzzle'