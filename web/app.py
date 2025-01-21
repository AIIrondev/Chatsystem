from flask import Flask, render_template, request, redirect, url_for, session, flash
from crypting import Crypting as cr
from database import Database as db
from database import User as us
from database import Chatroom as ch
from datetime import datetime
from cryptography.exceptions import InvalidTag
import os

app = Flask(__name__)

with open(os.path.join(os.path.dirname(__file__), "..", 'conf', 'website.conf'), 'r') as f:
    api_conf = f.read().splitlines()
    host = api_conf[0].split('=')[1]
    port = api_conf[1].split('=')[1]
    __version__ = api_conf[2].split('=')[1]
    app.secret_key = str(api_conf[3].split('=')[1])
    f.close()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('main.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Please fill all fields', 'error')
            return redirect(url_for('login'))
        print("Debug:", username, password)
        
        user_instance = us()
        user = user_instance.check_nm_pwd(username, password)

        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Please fill all fields', 'error')
            return redirect(url_for('register'))
        if us.get_user(username):
            flash('User already exists', 'error')
            return redirect(url_for('register'))
        if not us.check_password_strength(password):
            flash('Password is too weak', 'error')
            return redirect(url_for('register'))
        us.add_user(username, password)
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/new_chatroom', methods=['GET', 'POST'])
def new_chatroom():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['chatroom_name']
        key = request.form['chatroom_key']
        if not name or not key:
            flash('Please fill all fields', 'error')
            return redirect(url_for('new_chatroom'))
        hashed_key = ch.hashing(key)
        ch.add_chatroom(name, hashed_key)

        cr_instance = cr()
        cr_instance.set_key(hashed_key)
        message = cr_instance.encrypt('Welcome to the chatroom')
        db().add_message({'message': message, 'chat_room': name})
        flash('Chatroom created successfully', 'success')
        return redirect(url_for('home'))
    return render_template('new_chatroom.html')


@app.route('/enter_chatroom', methods=['GET', 'POST'])
def enter_chatroom():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        chat_name = request.form.get('chatroom_name')
        key = request.form.get('chatroom_key')

        if not chat_name or not key:
            flash('Please fill all fields', 'error')
            return redirect(url_for('enter_chatroom'))

        chatroom_instance = ch()
        chatroom = chatroom_instance.get_chatroom(chat_name)

        if not chatroom:
            flash('Chatroom does not exist', 'error')
            return redirect(url_for('enter_chatroom'))

        if chatroom['key'] != chatroom_instance.hashing(key):
            flash('Invalid key', 'error')
            return redirect(url_for('enter_chatroom'))

        session['chat_name'] = chat_name
        session['chat_key'] = key
        return redirect(url_for('chat'))
    return render_template('enter_chatroom.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session or 'chat_name' not in session:
        return redirect(url_for('login'))
    chat_name = session['chat_name']
    key = session['chat_key']

    cr_instance = cr()
    hashed_key = ch.hashing(key)
    cr_instance.set_key(hashed_key)

    if request.method == 'POST':
        message = request.form['message']
        if not message:
            flash('Message cannot be empty', 'error')
            return redirect(url_for('chat'))
        try:
            encrypted_message = cr_instance.encrypt(message)
            db().add_message({
                'message': encrypted_message,
                'chat_room': chat_name,
                'user': session['username'],
                'Date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
        except Exception as e:
            flash(f'Failed to send message: {e}', 'error')

    messages = db().get_messages(chat_name)
    decrypted_messages = []
    for message in messages:
        try:
            if message['chat_room'] == chat_name:
                decrypted_message = cr_instance.decrypt(message['message'])
                decrypted_messages.append({
                    'user': message['user'],
                    'content': decrypted_message,
                    'date': message['Date'],
                })
        except InvalidTag:
            decrypted_messages.append({'user': 'System', 'content': 'Error decrypting message', 'date': ''})
    return render_template('chat.html', messages=decrypted_messages, chat_name=chat_name)

@app.route('/send_message/<chatroom_name>', methods=['POST'])
def send_message(chatroom_name):
    if 'username' not in session or 'chat_name' not in session:
        return redirect(url_for('login'))
    
    message = request.form['message']
    key = session.get('chat_key')
    
    if not message:
        flash('Message cannot be empty', 'error')
        return redirect(url_for('chat'))

    try:
        cr_instance = cr()
        hashed_key = ch.hashing(key)
        cr_instance.set_key(hashed_key)
        encrypted_message = cr_instance.encrypt(message)
        
        db().add_message({
            'message': encrypted_message,
            'chat_room': chatroom_name,
            'user': session['username'],
            'Date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        flash('Message sent successfully', 'success')
    except Exception as e:
        flash(f'Failed to send message: {e}', 'error')

    return redirect(url_for('chat', chat_name=chatroom_name))


if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
