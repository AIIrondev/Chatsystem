from flask import Blueprint, render_template, jsonify

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/')
def index():
    return render_template('index.html')

@chat_bp.route('/fetch_messages')
def fetch_messages():
    # This is a placeholder for message fetching logic
    messages = ["Hello!", "Welcome to the chat!", "How can I help you?"]
    return jsonify({'messages': messages})