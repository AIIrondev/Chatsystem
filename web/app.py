from flask import Flask, render_template, request, redirect, url_for, session, flash
from crypting import Crypting as cr
from database import Database as db
from database import User as us
from database import Chatroom as ch
from datetime import datetime
from cryptography.exceptions import InvalidTag

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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
        user = us.check_nm_pwd(username, password)
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
        name = request.form['name']
        key = request.form['key']
        if not name or not key:
            flash('Please fill all fields', 'error')
            return redirect(url_for('new_chatroom'))
        ch.add_chatroom(name, ch.hashing(key))
        cr_instance = cr()
        cr_instance.set_key(ch.hashing(key))
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
        chat_name = request.form['name']
        key = request.form['key']
        if not chat_name or not key:
            flash('Please fill all fields', 'error')
            return redirect(url_for('enter_chatroom'))
        chatroom = ch().get_chatroom(chat_name)
        if not chatroom:
            flash('Chatroom does not exist', 'error')
            return redirect(url_for('enter_chatroom'))
        if chatroom['key'] != ch.hashing(key):
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
    if request.method == 'POST':
        message = request.form['message']
        if not message:
            flash('Message cannot be empty', 'error')
            return redirect(url_for('chat'))
        try:
            cr_instance = cr()
            cr_instance.set_key(ch.hashing(key))
            encrypted_message = cr_instance.encrypt(message)
            db().add_message({'message': encrypted_message, 'chat_room': chat_name, 'user': session['username'], 'Date': datetime.now().strftime("%Y-%m-%d %H:%M")})
        except Exception as e:
            flash(f'Failed to send message: {e}', 'error')
    messages = db().get_messages(chat_name)
    cr_instance = cr()
    cr_instance.set_key(ch.hashing(key))
    decrypted_messages = []
    for message in messages:
        try:
            if message['chat_room'] == chat_name:
                decrypted_message = cr_instance.decrypt(message['message'])
                decrypted_messages.append({
                    'user': message['user'],
                    'content': decrypted_message,
                    'date': message['Date']
                })
        except InvalidTag:
            decrypted_messages.append({'user': 'System', 'content': 'Error decrypting message', 'date': ''})
    return render_template('chat.html', messages=decrypted_messages, chat_name=chat_name)

if __name__ == '__main__':
    app.run(debug=True)
