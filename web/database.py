import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib
from tkinter import messagebox

class Database: # chat database class, preset: (_id, name, message, chat_room)
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Chatsystem']
        self.messages = self.db['messages']
        self.messages.create_index('chat_room')

    def add_message(self, message):
        self.messages.insert_one(message)

    def get_messages(self, chat_room):
        return self.messages.find({'chat_room': chat_room})

    def get_message(self, message_id):
        return self.messages.find_one({'_id': ObjectId(message_id)})

    def delete_message(self, message_id):
        self.messages.delete_one({'_id': ObjectId(message_id)})

    def update_message(self, message_id, message):
        self.messages.update_one({'_id': ObjectId(message_id)}, {'$set': message})

    def close(self):
        self.client.close()


class Chatroom:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Chatsystem']
        self.chatrooms = self.db['chatrooms']
        self.chatrooms.create_index('name', unique=True)

    @staticmethod
    def hashing(key):
        return hashlib.sha256(key.encode()).hexdigest()

    def check_key(self, key):
        return self.chatrooms.find_one({'key': key})

    def add_chatroom(self, name, key):
        try:
            self.chatrooms.insert_one({'name': name, 'key': key})
            return True
        except pymongo.errors.DuplicateKeyError:
            messagebox.showerror('Error', 'Chatroom already exists')
            return False

    def get_chatroom(self, name):
        return self.chatrooms.find_one({'name': name})

    def close(self):
        self.client.close()

class User:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Chatsystem']
        self.users = self.db['users']
        self.users.create_index('Username', unique=True)

    def check_password_strength(self, password):
        if len(password) < 12:
            messagebox.showerror('Critical', 'Password is too weak (12 characters required)\n youre request has been denied')
            return False
        return True

    @staticmethod
    def hashing(password):
        return hashlib.sha512(password.encode()).hexdigest()

    @staticmethod
    def check_nm_pwd(username, password):
        client = MongoClient('localhost', 27017)
        db = client['Chatsystem']
        users = db['users']
        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        user = users.find_one({'Username': username, 'Password': hashed_password})
        client.close()
        return user

    
    def add_user(self, username, password):
        if not self.check_password_strength(password):
            return False
        self.users.insert_one({'Username': username, 'Password': self.hashing(password)})
        return True

    def get_user(self, username):
        return self.users.find_one({'Username': username})

    def __str__(self):
        return self.username