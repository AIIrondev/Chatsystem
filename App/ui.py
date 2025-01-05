import tkinter as tk
from tkinter import messagebox
from crypting import Crypting as cr
import cryptography.exceptions
from database import Database as db
from database import User as us
from database import Chatroom as ch
from datetime import datetime

class UI:
    def run_main_loop(self):
        self.ch = None
        if self.ch is not None:
            self.ch.destroy()
        self.root = tk.Tk()
        self.root.title('Chat')
        self.root.geometry('400x400')
        self.root.resizable(False, False)
        self.main_window()
        self.root.mainloop()

    def register(self):
        self.user = None
        self.reg = tk.Tk()
        self.reg.title('Login/Register')
        self.reg.geometry('400x400')
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
        self.reg.mainloop()
    
    def login_user(self):
        username = self.username.get()
        password = self.password.get()
        if not username or not password:
            messagebox.showerror('Error', 'Please fill all the fields or register')
            return
        user = us().check_nm_pwd(username, password)
        if user:
            self.user = user['Username']
            self.reg.destroy()
            self.run_main_loop()
        else:
            messagebox.showerror('Error', 'Invalid credentials or register')

    def register_user(self):
        username = self.username.get()
        password = self.password.get()
        if not username or not password:
            messagebox.showerror('Error', 'Please fill all the fields')
            return
        user = us().get_user(username)
        if user:
            messagebox.showerror('Error', 'User already exists')
            return
        if not us().check_password_strength(password):
            return
        us().add_user(username, password)
        self.user = username
        self.reg.destroy()
        self.run_main_loop()

    def logout(self):
        self.user = None
        if self.ch is not None:
            self.ch.destroy()
        if self.root is not None:
            self.root.destroy()
        self.register()

    def main_window(self):
        tk.Label(self.root, text='Welcome to the chat').place(x=150, y=50)
        tk.Button(self.root, text='New Chatroom', command=self.new_chatroom).place(x=150, y=100)
        tk.Button(self.root, text='Enter Chatroom', command=self.enter_chatroom).place(x=150, y=150)
        tk.Button(self.root, text='Logout', command=self.logout).place(x=150, y=200)

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
        if not name or not key:
            messagebox.showerror('Error', 'Please fill all the fields')
            return
        ch().add_chatroom(name, ch().hashing(key))
        messagebox.showinfo('Success', 'Chatroom created')
        cr_instance = cr()
        cr_instance.set_key(ch().hashing(key))
        message = cr_instance.encrypt('Welcome to the chatroom')
        db().add_message({'message': message, 'chat_room': name})
        self.key_chatroom = key
        self.nc.destroy()
        self.Chat()

    def enter_chatroom(self):
        self.ec = tk.Tk()
        self.ec.title('Join Chatroom')
        self.ec.geometry('400x400')
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
        if not self.chat_name or not key:
            messagebox.showerror('Error', 'Please fill all the fields')
            return
        chatroom = ch().get_chatroom(self.chat_name)
        if not chatroom:
            messagebox.showerror('Error', 'Chatroom does not exist')
            return
        if chatroom['key'] != ch().hashing(key):
            messagebox.showerror('Error', 'Invalid key')
            return
        self.key_chatroom = key
        self.ec.destroy()
        self.Chat()

    def Chat(self):
        if self.root is not None:
            self.root.destroy()
            self.root = None
        self.ch = tk.Tk()
        self.ch.title(self.chat_name)
        self.ch.geometry('600x600')
        self.ch.resizable(True, True)
        tk.Label(self.ch, text=f'Welcome {self.user}').place(x=150, y=50)
        tk.Label(self.ch, text='Messages: ').place(x=10, y=75)
        frame = tk.Frame(self.ch)
        frame.place(x=20, y=110, width=580, height=200)
        canvas = tk.Canvas(frame)
        v_scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")

        messages = db().get_messages(self.chat_name)
        cr_instance = cr()
        cr_instance.set_key(ch().hashing(self.key_chatroom))
        for message in messages:
            try:
                if message["chat_room"] == self.chat_name:
                    decrypted_message = cr_instance.decrypt(message["message"])
                    message_frame = tk.Frame(scrollable_frame)
                    message_frame.pack(fill="x", pady=5)
                    message_label = tk.Label(message_frame, text=f"{message['user']} | {decrypted_message} | {message['Date']}", wraplength=500)
                    message_label.pack(side="left", anchor="w")
                    reply_button = tk.Button(message_frame, text="...", command=lambda: self.option_menu(message['_id']))
                    reply_button.pack(side="right", anchor="e")
                else:
                    print("Message from false chatroom")
                    continue
            except cryptography.exceptions.InvalidTag:
                tk.Label(scrollable_frame, text="Error decrypting message").pack(anchor="w")

        tk.Label(self.ch, text='Message').place(x=100, y=325)
        self.message_user = tk.Entry(self.ch)
        self.message_user.place(x=175, y=325)
        tk.Button(self.ch, text="Send", command=self.send_message).place(x=150, y=350)
        tk.Button(self.ch, text='Refresh', command=self.refresh).place(x=150, y=375)
        tk.Button(self.ch, text='Main Menu', command=self.run_main_loop).place(x=150, y=400)
        db().close()

    def refresh(self):
        self.ch.destroy()
        self.Chat()

    def send_message(self):
        message = self.message_user.get()
        if not message:
            messagebox.showerror('Error', 'Please fill the message')
            return
        try:
            cr_instance = cr()
            cr_instance.set_key(ch().hashing(self.key_chatroom))
            encrypted_message = cr_instance.encrypt(message)
            db().add_message({'message': encrypted_message, 'chat_room': self.chat_name, 'user': self.user, 'Date': datetime.now().strftime("%Y-%m-%d %H:%M")})
            messagebox.showinfo('Success', 'Message sent')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to send message: {e}')
        finally:
            self.message_user.delete(0, tk.END)
            self.refresh()

    def option_menu(self, message_id):
        messagebox.askokcancel("Option", "Delete this message", command=lambda: self.delete_message(message_id))

    def delete_message(self, message_id):
        db().delete_message(message_id)
        self.refresh()

    def close(self):
        self.root.destroy()
        self.ch.destroy()
        self.reg.destroy()
        self.nc.destroy()
        self.ec.destroy()