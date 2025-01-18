# just a simple Template
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/connect', methods=['POST'])
def connect():
    # Handle client connection logic
    return jsonify({"status": "connected"})

@app.route('/send_message', methods=['POST'])
def send_message():
    # Handle message sending logic
    return jsonify({"status": "message sent"})

@app.route('/receive_message', methods=['GET'])
def receive_message():
    # Handle message receiving logic
    return jsonify({"messages": ["message1", "message2"]})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)