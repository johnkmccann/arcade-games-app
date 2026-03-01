class ScoreService:
    def __init__(self):
        self.scores = []

    def add_score(self, player_name, score):
        self.scores.append({'player_name': player_name, 'score': score})
        self.scores.sort(key=lambda x: x['score'], reverse=True)  # Sort scores descending

    def get_leaderboard(self, top_n=10):
        return self.scores[:top_n]  # Return top N scores

    def get_score(self, player_name):
        for entry in self.scores:
            if entry['player_name'] == player_name:
                return entry['score']
        return None

    def remove_score(self, player_name):
        self.scores = [entry for entry in self.scores if entry['player_name'] != player_name]

