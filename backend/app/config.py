import os

# Environment configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/mydatabase'
    DEBUG = os.environ.get('DEBUG') or False


# Mock database client for development without MongoDB
class MockCollection:
    """Mock MongoDB collection"""
    async def find_one(self, query):
        return None
    
    async def insert_one(self, doc):
        return None
    
    async def update_one(self, query, doc):
        return None
    
    async def find(self, query):
        return []
    
    async def insert_many(self, docs):
        return None


class MockDB:
    """Mock MongoDB client that allows development without actual database"""
    
    class DB:
        def __init__(self):
            # User-related collections
            self.users = MockCollection()
            self.game_access_rules = MockCollection()
            
            # Game session collections
            self.game_sessions = MockCollection()
            self.active_sessions = MockCollection()
            
            # Scoring and leaderboard collections
            self.scores = MockCollection()
            self.leaderboards = MockCollection()
            self.user_game_stats = MockCollection()
            
            # Game metadata (could be populated from GameRegistry)
            self.games = MockCollection()
    
    def __init__(self):
        self.db = self.DB()


# Create a database client instance
# In production, this would be a real MongoDB client
db_client = MockDB()