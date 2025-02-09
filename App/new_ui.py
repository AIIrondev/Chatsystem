import tkinter as tk
from tkinter import messagebox
import requests
import hashlib
from cryptography.exceptions import InvalidTag
from crypting import Crypting as cr
import sys


class UI:
    def __init__(self):
        self.user = None
        self.chat_name = None
        self.key_chatroom = None
        self.root = tk.Tk()
        self.root.title('Chat')
        self.root.geometry('600x500')
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.first = None
        self.register()
        self.root.mainloop()

    def clear_window(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
    def on_close(self):
        self.root.destroy()
        sys.exit(0)

    def register(self):
        if self.first:
            self.clear_window()
        else:
            self.first = True
            self.frame = tk.Frame(self.root)
            self.frame.pack(fill="both", expand=True)
        
        self.user = None
        self.root.title('Login/Register')
        tk.Label(self.frame, text='Login with username').place(x=150, y=50)
        tk.Label(self.frame, text='Username').place(x=70, y=100)
        self.username = tk.Entry(self.frame)
        self.username.place(x=150, y=100)
        tk.Label(self.frame, text='Password').place(x=70, y=150)
        self.password = tk.Entry(self.frame, show='*')
        self.password.place(x=150, y=150)
        tk.Button(self.frame, text='Login', command=self.login_user).place(x=150, y=200)
        tk.Label(self.frame, text='Or').place(x=150, y=250)
        tk.Button(self.frame, text='Register', command=self.register_user).place(x=150, y=300)


    def login_user(self):
        username = self.username.get()
        password = self.password.get()
        try:
            response = request('/login', 'POST', {'username': username, 'password': password})
            request_return = response.json()
            if request_return.get('success'):
                self.user = request_return['user']
                self.main_window()
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
                self.main_window()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to register: {e}')

    def logout(self):
        self.user = None
        self.register()

    def main_window(self):
        self.clear_window()
        self.root.title('Chat')
        tk.Label(self.frame, text='Welcome to the chat').place(x=150, y=50)
        tk.Button(self.frame, text='New Chatroom', command=self.new_chatroom).place(x=150, y=100)
        tk.Button(self.frame, text='Enter Chatroom', command=self.enter_chatroom).place(x=150, y=150)
        tk.Button(self.frame, text='Logout', command=self.logout).place(x=150, y=200)

    def new_chatroom(self):
        self.clear_window()
        self.root.title('Create Chatroom')
        tk.Label(self.frame, text='Create Chatroom').place(x=150, y=50)
        tk.Label(self.frame, text='Name').place(x=70, y=100)
        self.name = tk.Entry(self.frame)
        self.name.place(x=120, y=100)
        tk.Label(self.frame, text='Key').place(x=70, y=150)
        self.key = tk.Entry(self.frame)
        self.key.place(x=120, y=150)
        tk.Button(self.frame, text='Create', command=self.create_chatroom).place(x=150, y=200)
        tk.Button(self.frame, text='Main Menu', command=self.main_window).place(x=150, y=250)

    def create_chatroom(self):
        name = self.name.get()
        key = self.key.get()
        try:
            response = request('/create_chatroom', 'POST', {'name': name, 'key': key})
            request_return = response.json()
            if request_return.get('success'):
                self.key_chatroom = key
                self.chat_name = name
                self.Chat()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to create chatroom: {e}')

    def enter_chatroom(self):
        self.root.title('Enter Chatroom')
        self.clear_window()
        tk.Label(self.frame, text='Join Chatroom').place(x=150, y=50)
        tk.Label(self.frame, text='Name').place(x=100, y=100)
        self.name = tk.Entry(self.frame)
        self.name.place(x=150, y=100)
        tk.Label(self.frame, text='Key').place(x=100, y=150)
        self.key = tk.Entry(self.frame, show='*')
        self.key.place(x=150, y=150)
        tk.Button(self.frame, text='Join', command=self.join_chatroom).place(x=150, y=200)
        tk.Button(self.frame, text='Main Menu', command=self.main_window).place(x=150, y=250)

    def join_chatroom(self):
        self.chat_name = self.name.get()
        key = self.key.get()
        try:
            response = request('/join_chatroom', 'POST', {'chat_name': self.chat_name, 'key': key})
            request_return = response.json()
            if request_return.get('success'):
                self.key_chatroom = key
                self.Chat()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to join chatroom: {e}')

    def Chat(self):
        self.clear_window()
        self.root.title('Chat')

        tk.Label(self.frame, text=f'Welcome {self.user}').place(x=150, y=50)
        tk.Label(self.frame, text='Messages: ').place(x=10, y=75)

        self.frame_1 = tk.Frame(self.frame)
        self.frame_1.place(x=20, y=110, width=580, height=200)
        self.canvas = tk.Canvas(self.frame_1)
        self.v_scrollbar = tk.Scrollbar(self.frame_1, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")

        tk.Label(self.frame, text='Message').place(x=100, y=325)
        self.message_user = tk.Entry(self.frame)
        self.message_user.place(x=175, y=325)
        tk.Button(self.frame, text="Send", command=self.send_message).place(x=150, y=350)
        tk.Button(self.frame, text='Refresh', command=self.update_messages).place(x=150, y=375)
        tk.Button(self.frame, text='Main Menu', command=self.main_window).place(x=150, y=400)

        self.update_messages()
    
    def update_messages(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            response = request('/receive_message', 'GET', {'chat_room': self.chat_name})
            messages = response.json().get('message', [])
            cr_instance = cr()
            cr_instance.set_key(hashing(self.key_chatroom))

            for message in reversed(messages):  
                try:
                    if message.get("chat_room") == self.chat_name:
                        decrypted_message = cr_instance.decrypt(message["message"])
                        message_frame = tk.Frame(self.scrollable_frame)
                        message_frame.pack(fill="x", pady=5, side="top", anchor="w")

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
            self.update_messages()

    def option_menu(self, message_id):
        response = messagebox.askokcancel("Option", "Delete this message")
        if response:
            self.delete_message(message_id)

    def delete_message(self, message_id):
        try:
            request('/delete_message', 'POST', {'message_id': message_id})
            self.update_messages()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to delete message: {e}')


def request(endpoint, method, data):
    url = 'http://127.0.0.1:4999'
    full_url = url + endpoint
    try:
        if method == 'POST':
            response = requests.post(full_url, json=data)
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
        return response.json()


def hashing(key):
    return hashlib.sha256(key.encode()).hexdigest()

if __name__ == '__main__':
    UI()