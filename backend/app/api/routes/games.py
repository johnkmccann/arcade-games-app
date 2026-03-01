from flask import Flask, jsonify, request

app = Flask(__name__)

games = [
    {'id': 1, 'title': 'Chess', 'genre': 'Strategy'},
    {'id': 2, 'title': 'Tetris', 'genre': 'Puzzle'},
    {'id': 3, 'title': 'Pac-Man', 'genre': 'Arcade'}
]

@app.route('/games', methods=['GET'])
def get_games():
    return jsonify(games)

@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = next((game for game in games if game['id'] == game_id), None)
    if game:
        return jsonify(game)
    return jsonify({'error': 'Game not found'}), 404

@app.route('/games', methods=['POST'])
def add_game():
    new_game = request.get_json()
    new_game['id'] = len(games) + 1
    games.append(new_game)
    return jsonify(new_game), 201

@app.route('/games/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    game = next((game for game in games if game['id'] == game_id), None)
    if game:
        updates = request.get_json()
        game.update(updates)
        return jsonify(game)
    return jsonify({'error': 'Game not found'}), 404

@app.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    global games
    games = [game for game in games if game['id'] != game_id]
    return jsonify({'result': 'Game deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)