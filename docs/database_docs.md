# Chat System Documentation

## Overview
This Python-based chat system consists of three main classes: `Database`, `Chatroom`, and `User`. These classes interact with a MongoDB database to provide functionality for managing chat messages, chat rooms, and user accounts.

---

## Prerequisites
Ensure the following are installed and configured on your system:
- Python 3.8 or later
- MongoDB server running on `localhost:27017`
- Required Python libraries:
  - `pymongo`
  - `bson`
  - `tkinter`

Install the libraries using:
```bash
pip install pymongo bson
```

---

## Class: `Database`
Handles operations related to chat messages.

### Methods

#### `__init__()`
Initializes the connection to the MongoDB server and sets up the `messages` collection.

#### `add_message(message)`
Adds a new message to the `messages` collection.
- **Parameter:**
  - `message` (dict): A dictionary containing message details (e.g., `{'name': 'User', 'message': 'Hello', 'chat_room': 'room1'}`).

#### `get_messages(chat_room)`
Retrieves all messages from a specific chat room.
- **Parameter:**
  - `chat_room` (str): The name of the chat room.
- **Returns:**
  - A cursor to the retrieved messages.

#### `get_message(message_id)`
Fetches a single message by its ID.
- **Parameter:**
  - `message_id` (str): The ID of the message.
- **Returns:**
  - A dictionary with message details.

#### `delete_message(message_id)`
Deletes a message by its ID.
- **Parameter:**
  - `message_id` (str): The ID of the message.

#### `update_message(message_id, message)`
Updates a message by its ID.
- **Parameters:**
  - `message_id` (str): The ID of the message.
  - `message` (dict): A dictionary with updated message details.

#### `close()`
Closes the connection to the database.

### Example Usage
```python
from database_module import Database

db = Database()
db.add_message({'name': 'Alice', 'message': 'Hello!', 'chat_room': 'room1'})
messages = db.get_messages('room1')
for msg in messages:
    print(msg)
db.close()
```

---

## Class: `Chatroom`
Handles operations related to chat rooms.

### Methods

#### `__init__()`
Initializes the connection to the MongoDB server and sets up the `chatrooms` collection.

#### `hashing(key)`
Hashes a given key using SHA-256.
- **Parameter:**
  - `key` (str): The key to hash.
- **Returns:**
  - A hashed string.

#### `check_key(key)`
Checks if a key exists in the `chatrooms` collection.
- **Parameter:**
  - `key` (str): The key to check.
- **Returns:**
  - A dictionary with chatroom details if found, otherwise `None`.

#### `add_chatroom(name, key)`
Adds a new chat room.
- **Parameters:**
  - `name` (str): The name of the chat room.
  - `key` (str): The key for the chat room.
- **Returns:**
  - `True` if added successfully, `False` if the chat room already exists.

#### `get_chatroom(name)`
Fetches a chat room by name.
- **Parameter:**
  - `name` (str): The name of the chat room.
- **Returns:**
  - A dictionary with chatroom details.

#### `close()`
Closes the connection to the database.

### Example Usage
```python
from database_module import Chatroom

chatroom = Chatroom()
if chatroom.add_chatroom('room1', chatroom.hashing('secret_key')):
    print('Chatroom created successfully.')
chat = chatroom.get_chatroom('room1')
print(chat)
chatroom.close()
```

---

## Class: `User`
Handles operations related to user accounts.

### Methods

#### `__init__()`
Initializes the connection to the MongoDB server and sets up the `users` collection.

#### `check_password_strength(password)`
Checks the strength of a password.
- **Parameter:**
  - `password` (str): The password to check.
- **Returns:**
  - `True` if the password is strong, otherwise `False`.

#### `hashing(password)`
Hashes a password using SHA-512.
- **Parameter:**
  - `password` (str): The password to hash.
- **Returns:**
  - A hashed string.

#### `check_nm_pwd(username, password)`
Validates a username and password combination.
- **Parameters:**
  - `username` (str): The username.
  - `password` (str): The password.
- **Returns:**
  - A dictionary with user details if valid, otherwise `None`.

#### `add_user(username, password)`
Adds a new user to the system.
- **Parameters:**
  - `username` (str): The username.
  - `password` (str): The password.
- **Returns:**
  - `True` if added successfully, otherwise `False`.

#### `get_user(username)`
Fetches a user by username.
- **Parameter:**
  - `username` (str): The username.
- **Returns:**
  - A dictionary with user details.

### Example Usage
```python
from database_module import User

user = User()
if user.add_user('Alice', 'StrongPassword123!'):
    print('User added successfully.')
user_info = user.get_user('Alice')
print(user_info)
user.close()
```
