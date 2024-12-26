import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib

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

class User:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['user']
        self.users = self.db['users']

    def check_password_strength(self, password):
        if len(password) < 12:
            return False
        return True

    def hashing(self, password):
        return hashlib.sha512(password.encode()).hexdigest()

    def check_nm_pwd(self, username, password):
        return self.users.find_one({'Username': username, 'Password': self.hashing(password)})

    def __str__(self):
        return self.username