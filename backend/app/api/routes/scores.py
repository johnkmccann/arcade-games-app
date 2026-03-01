from flask import Blueprint, request, jsonify

# Initialize the scores blueprint
scores_bp = Blueprint('scores', __name__)

# Mock database
scores_db = []

# Route to get all scores
@scores_bp.route('/scores', methods=['GET'])
def get_scores():
    return jsonify(scores_db), 200

# Route to add a new score
@scores_bp.route('/scores', methods=['POST'])
def add_score():
    data = request.json
    if 'player' not in data or 'score' not in data:
        return jsonify({'error': 'Bad request, player and score are required.'}), 400
    scores_db.append(data)
    return jsonify(data), 201

# Route to get a score by player
@scores_bp.route('/scores/<string:player>', methods=['GET'])
def get_score_by_player(player):
    player_scores = [s for s in scores_db if s['player'] == player]
    if not player_scores:
        return jsonify({'error': 'Player not found.'}), 404
    return jsonify(player_scores), 200

# Route to delete a score by player
@scores_bp.route('/scores/<string:player>', methods=['DELETE'])
def delete_score(player):
    global scores_db
    scores_db = [s for s in scores_db if s['player'] != player]
    return jsonify({'message': 'Scores deleted for player: ' + player}), 200
