# Game Service

This file contains the business logic and operations for the Game service with MongoDB.

import pymongo

class GameService:
    def __init__(self, db_url, db_name):
        self.client = pymongo.MongoClient(db_url)
        self.db = self.client[db_name]
        self.games_collection = self.db['games']

    def create_game(self, game_data):
        """
        Create a new game entry in the database.
        :param game_data: Dictionary containing game details
        :return: The result of the insert operation
        """
        return self.games_collection.insert_one(game_data)

    def get_game(self, game_id):
        """
        Retrieve a game by its ID.
        :param game_id: The ID of the game
        :return: The game document
        """
        return self.games_collection.find_one({'_id': game_id})

    def update_game(self, game_id, update_data):
        """
        Update the game entry with the given ID.
        :param game_id: The ID of the game
        :param update_data: Dictionary containing updated fields
        :return: The result of the update operation
        """
        return self.games_collection.update_one({'_id': game_id}, {'$set': update_data})

    def delete_game(self, game_id):
        """
        Delete a game entry from the database.
        :param game_id: The ID of the game
        :return: The result of the delete operation
        """
        return self.games_collection.delete_one({'_id': game_id})