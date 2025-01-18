# just a simple Template
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    # Handle client connection logic
    pass

@app.route('/logout', methods=['POST'])
def logout():
    # Handle client disconnection logic
    pass

@app.route('/send_message', methods=['POST'])
def send_message():
    # Handle message sending logic
    pass

@app.route('/receive_message', methods=['GET'])
def receive_message():
    # Handle message receiving logic
    pass

@app.route('/create_chatroom', methods=['POST'])
def create_chatroom():
    # Handle chatroom creation logic
    pass

@app.route('/list_chatrooms', methods=['GET'])
def list_chatrooms():
    # Handle chatroom listing logic
    pass

@app.route('/join_chatroom', methods=['POST'])
def join_chatroom():
    # Handle chatroom joining logic
    pass


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4999)