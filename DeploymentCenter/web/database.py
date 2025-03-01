'''
   Copyright 2025 Maximilian Gründinger

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib
from tkinter import messagebox
from argon2 import PasswordHasher

class Database:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Chatsystem']
        self.messages = self.db['messages']
        self.chatrooms = self.db['chatrooms']
        self.users = self.db['users']
    
    @staticmethod
    def add_message(message):
        client = MongoClient('localhost', 27017)
        db = client['Chatsystem']
        messages = db['messages']
        messages.create_index('chat_room')
        messages.insert_one(message)
        client.close()

    @staticmethod
    def get_messages(chat_room):
        client = MongoClient('localhost', 27017)
        db = client['Chatsystem']
        messages = db['messages']
        messages.create_index('chat_room')
        messages_return = messages.find({'chat_room': chat_room})
        return messages_return

    @staticmethod
    def get_message(message_id):
        client = MongoClient('localhost', 27017)
        db = client['Chatsystem']
        messages = db['messages']
        messages.create_index('chat_room')
        message_return = messages.find_one({'_id': ObjectId(message_id)})
        client.close()
        return message_return

    @staticmethod
    def delete_message(message_id):
        client = MongoClient('localhost', 27017)
        db = client['Chatsystem']
        messages = db['messages']
        messages.create_index('chat_room')
        messages.delete_one({'_id': ObjectId(message_id)})
        client.close()

    @staticmethod
    def update_message(message_id, message):
        client = MongoClient('localhost', 27017)
        db = client['Chatsystem']
        messages = db['messages']
        messages.create_index('chat_room')
        messages.update_one({'_id': ObjectId(message_id)}, {'$set': {'message': message}})
        client.close()

    def __del__(self):
        self.client.close()

class Chatroom:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Chatsystem']
        self.chatrooms = self.db['chatrooms']

    @staticmethod
    def hashing(key):
        return hashlib.sha256(key.encode()).hexdigest()

    @staticmethod
    def check_key(key):
        client = MongoClient('localhost', 27017)
        db = client['Chatsystem']
        chatrooms = db['chatrooms']
        chatrooms.create_index('name', unique=True)
        chatroom = chatrooms.find_one({'key': key})
        client.close()
        return chatroom

    @staticmethod
    def add_chatroom(name, key):
        client = MongoClient('localhost', 27017)
        db = client['Chatsystem']
        chatrooms = db['chatrooms']
        chatrooms.create_index('name', unique=True)
        try:
            chatrooms.insert_one({'name': name, 'key': key})
            client.close()
            return True
        except pymongo.errors.DuplicateKeyError:
            messagebox.showerror('Error', 'Chatroom already exists')
            client.close()
            return False

    @staticmethod
    def get_chatroom(name):
        client = MongoClient('localhost', 27017)
        db = client['Chatsystem']
        chatrooms = db['chatrooms']
        chatrooms.create_index('name', unique=True)
        chat_room = chatrooms.find_one({'name': name})
        client.close()
        return chat_room


class User:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Chatsystem']
        self.users = self.db['users']

    @staticmethod
    def check_password_strength(password):
        if len(password) < 12:
            messagebox.showerror('Critical', 'Password is too weak (12 characters required)\n youre request has been denied')
            return False
        return True

    @staticmethod
    def hashing(password):
        ph = PasswordHasher()
        return ph.hash(password.encode())

    @staticmethod
    def check_nm_pwd(username, password):
        ph = PasswordHasher()
        client = MongoClient('localhost', 27017)
        db = client['Chatsystem']
        users = db['users']
        hashed_password = ph.hash(password.encode())
        user = users.find_one({'Username': username, 'Password': hashed_password})
        client.close()
        return user

    @staticmethod
    def add_user(username, password):
        client = MongoClient('localhost', 27017)
        db = client['Chatsystem']
        users = db['users']
        if not User.check_password_strength(password):
            return False
        users.insert_one({'Username': username, 'Password': User.hashing(password)})
        client.close()
        return True

    @staticmethod
    def get_user(username):
        client = MongoClient('localhost', 27017)
        db = client['Chatsystem']
        users = db['users']
        users_return = users.find_one({'Username': username})
        client.close()
        return users_return