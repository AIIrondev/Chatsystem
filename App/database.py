import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

class Database: # chat database class, preset: (_id, name, message, chat_room)
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['chat']
        self.messages = self.db['messages']

    def add_message(self, message):
        self.messages.insert_one(message)

    def get_messages(self):
        return self.messages.find()

    def get_message(self, message_id):
        return self.messages.find_one({'_id': ObjectId(message_id)})

    def delete_message(self, message_id):
        self.messages.delete_one({'_id': ObjectId(message_id)})

    def update_message(self, message_id, message):
        self.messages.update_one({'_id': ObjectId(message_id)}, {'$set': message})

    def __del__(self):
        self.client.close()