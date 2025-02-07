# This should be reachable wth the URl: https://127.0.0.1:4999/enter_chatroom
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))
from flask import Flask, request, jsonify
from database import User as us
from database import Chatroom as ch
from database import Database as db
from datetime import datetime
from crypting import Crypting as cr
app = Flask(__name__)

with open(os.path.join(os.path.dirname(__file__), "..", "..", 'conf', 'api.conf'), 'r') as f:
    api_conf = f.read().splitlines()
    host = api_conf[0].split('=')[1]
    port = api_conf[1].split('=')[1]
    __version__ = api_conf[2].split('=')[1]
    f.close()

@app.route('/login', methods=['POST'])
def login():
    """
    Handles user login by verifying the username and password.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Please fill all the fields or register'}), 400

    user = us.check_nm_pwd(username, password)
    if user:
        return jsonify({'success': 'User logged in', 'user': user['Username']})
    else:
        return jsonify({'error': 'Invalid credentials or register'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    """
    Logs the user out of the system.
    """
    return jsonify({'success': 'User logged out'})

@app.route('/register', methods=['POST'])
def register():
    """
    Handles user registration by adding new users to the database after validation.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Please fill all the fields or register'}), 400

    user = us.get_user(username)
    if user:
        return jsonify({'error': 'User already exists'}), 409

    if not us.check_password_strength(password):
        return jsonify({'error': 'Password is too weak'}), 400

    us.add_user(username, password)
    return jsonify({'success': 'User added'}), 201


@app.route('/send_message', methods=['POST'])
def send_message():
    """
    Sends a message to a specified chatroom after encrypting it with a key.
    """
    data = request.get_json()
    chat_name = data.get('chat_name')
    key = data.get('key')
    message = data.get('message')
    user = data.get('user')

    if not chat_name or not key or not message or not user:
        return jsonify({'error': 'Please fill all the fields'}), 400

    try:
        cr_instance = cr()
        cr_instance.set_key(ch().hashing(key))
        encrypted_message = cr_instance.encrypt(message)

        db().add_message({
            'message': encrypted_message,
            'chat_room': chat_name,
            'user': user,
            'Date': datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        return jsonify({'success': 'Message sent'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_message', methods=['POST'])
def delete_message(message_id):
    """
    Deletes a message from the database based on the provided message ID.
    """
    db().delete_message(message_id)
    return jsonify({'success': 'Message deleted'})

@app.route('/receive_message', methods=['GET'])
def receive_message(chat_room):
    """
    Retrieves all messages from a specified chatroom.
    """
    return jsonify({'message': db.get_messages(chat_room)})

@app.route('/create_chatroom', methods=['POST'])
def create_chatroom():
    """
    Creates a new chatroom with the specified name and key.
    """
    data = request.get_json()
    name = data.get('name')
    key = data.get('key')

    if not name or not key:
        return jsonify({'error': 'Please fill all the fields'}), 400

    ch.add_chatroom(name, ch.hashing(key))
    return jsonify({'success': 'Chatroom created'}), 201

@app.route('/list_chatrooms', methods=['GET'])
def list_chatrooms():
    chatrooms = ch.get_chatrooms()
    return jsonify({'chatrooms': chatrooms})

@app.route('/join_chatroom', methods=['POST'])
def join_chatroom():
    """
    Allows a user to join a specified chatroom if the correct key is provided.
    """
    data = request.get_json()
    chat_name = data.get('chat_name')
    key = data.get('key')

    if not chat_name or not key:
        return jsonify({'error': 'Please fill all the fields'}), 400

    chatroom = ch().get_chatroom(chat_name)
    if not chatroom:
        return jsonify({'error': 'Chatroom does not exist'}), 404

    if chatroom['key'] != ch.hashing(key):
        return jsonify({'error': 'Invalid key'}), 403

    return jsonify({'success': 'Chatroom joined'}), 200

@app.route('/test_connection', methods=['GET'])
def test_connection():
    return jsonify({'success': 'Connection established'})


def run_main():
    app.run(host=host, port=port)# '127.0.0.1', 4999

if __name__ == '__main__':
    run_main()