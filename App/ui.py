import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import hashlib
from cryptography.exceptions import InvalidTag
from crypting import Crypting as cr


class UI:
    def __init__(self):
        self.ch = None
        self.root = None
        self.reg = None
        self.nc = None
        self.ec = None
        self.user = None
        self.chat_name = None
        self.key_chatroom = None
        self.register()

    def run_main_loop(self):
        if not self.user:
            self.register()
        else:
            self.main_window()
        self.root = tk.Tk()
        self.root.title('Chat')
        self.root.geometry('400x400')
        self.root.iconbitmap('icon.ico')
        self.root.resizable(False, False)
        self.main_window()
        self.root.mainloop()

    def register(self):
        self.user = None
        self.reg = tk.Tk()
        self.reg.title('Login/Register')
        self.reg.geometry('400x400')
        self.reg.iconbitmap('icon.ico')
        self.reg.resizable(False, False)
        tk.Label(self.reg, text='Login with username').place(x=150, y=50)
        tk.Label(self.reg, text='Username').place(x=70, y=100)
        self.username = tk.Entry(self.reg)
        self.username.place(x=150, y=100)
        tk.Label(self.reg, text='Password').place(x=70, y=150)
        self.password = tk.Entry(self.reg, show='*')
        self.password.place(x=150, y=150)
        tk.Button(self.reg, text='Login', command=self.login_user).place(x=150, y=200)
        tk.Label(self.reg, text='Or').place(x=150, y=250)
        tk.Button(self.reg, text='Register', command=self.register_user).place(x=150, y=300)
        self.reg.protocol("WM_DELETE_WINDOW", self.on_close_register)
        self.reg.mainloop()

    def on_close_register(self):
        self.reg.destroy()
        SystemExit(0)


    def login_user(self):
        username = self.username.get()
        password = self.password.get()
        try:
            response = request('/login', 'POST', {'username': username, 'password': password})
            request_return = response.json()
            if request_return.get('success'):
                self.user = request_return['user']
                self.reg.destroy()
                self.run_main_loop()
            else:
                messagebox.showerror('Error', 'Invalid credentials or register')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to login: {e}')

    def register_user(self):
        username = self.username.get()
        password = self.password.get()
        try:
            response = request('/register', 'POST', {'username': username, 'password': password})
            request_return = response.json()
            if request_return.get('success'):
                self.user = username
                self.reg.destroy()
                self.run_main_loop()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to register: {e}')

    def logout(self):
        self.user = None
        if self.ch:
            self.ch.destroy()
        if self.root:
            self.root.destroy()
        self.register()

    def main_window(self):
        if self.ch:
            self.ch.destroy()
        self.root = tk.Tk()
        self.root.title('Chat')
        self.root.geometry('400x400')
        self.root.iconbitmap('icon.ico')
        self.root.resizable(False, False)

        tk.Label(self.root, text='Welcome to the chat').place(x=150, y=50)
        tk.Button(self.root, text='New Chatroom', command=self.new_chatroom).place(x=150, y=100)
        tk.Button(self.root, text='Enter Chatroom', command=self.enter_chatroom).place(x=150, y=150)
        tk.Button(self.root, text='Logout', command=self.logout).place(x=150, y=200)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close_main)
        self.root.mainloop()

    def on_close_main(self):
        if self.root:
            self.root.destroy()


    def new_chatroom(self):
        self.nc = tk.Tk()
        self.nc.title('Create Chatroom')
        self.nc.geometry('400x400')
        self.nc.resizable(False, False)
        tk.Label(self.nc, text='Create Chatroom').place(x=150, y=50)
        tk.Label(self.nc, text='Name').place(x=70, y=100)
        self.name = tk.Entry(self.nc)
        self.name.place(x=120, y=100)
        tk.Label(self.nc, text='Key').place(x=70, y=150)
        self.key = tk.Entry(self.nc)
        self.key.place(x=120, y=150)
        tk.Button(self.nc, text='Create', command=self.create_chatroom).place(x=150, y=200)

    def create_chatroom(self):
        name = self.name.get()
        key = self.key.get()
        try:
            response = request('/create_chatroom', 'POST', {'name': name, 'key': key})
            request_return = response.json()
            if request_return.get('success'):
                self.nc.destroy()
                self.Chat()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to create chatroom: {e}')

    def enter_chatroom(self):
        self.ec = tk.Tk()
        self.ec.title('Join Chatroom')
        self.ec.geometry('400x400')
        self.ec.iconbitmap('icon.ico')
        self.ec.resizable(False, False)
        tk.Label(self.ec, text='Join Chatroom').place(x=150, y=50)
        tk.Label(self.ec, text='Name').place(x=100, y=100)
        self.name = tk.Entry(self.ec)
        self.name.place(x=150, y=100)
        tk.Label(self.ec, text='Key').place(x=100, y=150)
        self.key = tk.Entry(self.ec)
        self.key.place(x=150, y=150)
        tk.Button(self.ec, text='Join', command=self.join_chatroom).place(x=150, y=200)

    def join_chatroom(self):
        self.chat_name = self.name.get()
        key = self.key.get()
        try:
            response = request('/join_chatroom', 'POST', {'chat_name': self.chat_name, 'key': key})
            request_return = response.json()
            if request_return.get('success'):
                self.key_chatroom = key
                self.ec.destroy()
                self.Chat()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to join chatroom: {e}')

    def Chat(self):
        if self.root:
            self.root.destroy()
            self.root = None
        self.ch = tk.Tk()
        self.ch.title(self.chat_name)
        self.ch.geometry('600x600')
        self.ch.iconbitmap('icon.ico')
        self.ch.resizable(True, True)

        tk.Label(self.ch, text=f'Welcome {self.user}').place(x=150, y=50)
        tk.Label(self.ch, text='Messages: ').place(x=10, y=75)

        self.frame = tk.Frame(self.ch)
        self.frame.place(x=20, y=110, width=580, height=200)
        self.canvas = tk.Canvas(self.frame)
        self.v_scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")

        tk.Label(self.ch, text='Message').place(x=100, y=325)
        self.message_user = tk.Entry(self.ch)
        self.message_user.place(x=175, y=325)
        tk.Button(self.ch, text="Send", command=self.send_message).place(x=150, y=350)
        tk.Button(self.ch, text='Refresh', command=self.refresh).place(x=150, y=375)
        tk.Button(self.ch, text='Main Menu', command=self.back).place(x=150, y=400)

        try:
            self.update_messages()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to update messages: {e}')

    def back(self):
        if self.ch:
            self.ch.destroy()
        self.run_main_loop()

    def update_messages(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            response = request('/receive_message', 'GET', {'chat_room': self.chat_name})
            messages = response.json().get('message', [])
            cr_instance = cr()
            cr_instance.set_key(hashing(self.key_chatroom))
            for message in messages:
                try:
                    if message.get("chat_room") == self.chat_name:
                        decrypted_message = cr_instance.decrypt(message["message"])
                        message_frame = tk.Frame(self.scrollable_frame)
                        message_frame.pack(fill="x", pady=5)
                        message_label = tk.Label(
                            message_frame,
                            text=f"{message['user']} | {decrypted_message} | {message['Date']}",
                            wraplength=500
                        )
                        message_label.pack(side="left", anchor="w")
                        reply_button = tk.Button(
                            message_frame,
                            text="...",
                            command=lambda msg_id=message['_id']: self.option_menu(msg_id)
                        )
                        reply_button.pack(side="right", anchor="e")
                except InvalidTag:
                    tk.Label(self.scrollable_frame, text="Error decrypting message").pack(anchor="w")
        except Exception as e:
            messagebox.showerror('Error', f'Failed to retrieve messages: {e}')

    def refresh(self):
        self.update_messages()

    def send_message(self):
        message = self.message_user.get()
        if not message:
            messagebox.showerror('Error', 'Please fill the message')
            return
        try:
            cr_instance = cr()
            cr_instance.set_key(hashing(self.key_chatroom))
            encrypted_message = cr_instance.encrypt(message)
            request('/send_message', 'POST', {
                'chat_name': self.chat_name,
                'key': self.key_chatroom,
                'message': encrypted_message,
                'user': self.user
            })
        except Exception as e:
            messagebox.showerror('Error', f'Failed to send message: {e}')
        finally:
            self.message_user.delete(0, tk.END)
            self.refresh()

    def option_menu(self, message_id):
        response = messagebox.askokcancel("Option", "Delete this message")
        if response:
            self.delete_message(message_id)

    def delete_message(self, message_id):
        try:
            request('/delete_message', 'POST', {'message_id': message_id})
            self.refresh()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to delete message: {e}')


def request(endpoint, method, data):
    url = 'http://127.0.0.1:4999'
    full_url = url + endpoint
    try:
        if method == 'POST':
            response = requests.post(full_url, data=data)
        elif method == 'GET':
            response = requests.get(full_url, params=data)
        else:
            raise ValueError("Unsupported HTTP method")
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Request failed: {e}")
        raise


class test_api:
    def __init__(self):
        self.url = 'http://127.0.0.1:4999'
        self.endpoint = '/test_connection'
        self.method = 'GET'
        self.test_connection()
        
    def test_connection(self):
        response = requests.get(self.url + self.endpoint)
        print(response.json())
        return response.json()


def hashing(key):
    return hashlib.sha256(key.encode()).hexdigest()
