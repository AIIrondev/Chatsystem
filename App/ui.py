import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from crypting import Crypting as cr
from database import Database as db
from database import User as us
from database import Chatroom as ch
import os

class UI:
    def run_main_loop(self):
        self.root = tk.Tk()
        self.root.title('Crypting')
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

    def get_key(self):
        file = filedialog.askopenfilename()
        with open(file, 'r') as f:
            key = f.read()
        cr().set_key(key)

    def logout(self):
        self.user = None
        self.root.destroy()
        self.register()

    def main_window(self):
        tk.Label(self.root, text='Welcome to the chat').place(x=150, y=50)
        tk.Button(self.root, text='New Chatroom', command=self.new_chatroom).place(x=150, y=100)
        tk.Button(self.root, text='Enter Chatroom', command=self.enter_chatroom).place(x=150, y=150)
        tk.Button(self.root, text='Logout', command=self.logout).place(x=150, y=200)

    def new_chatroom(self):
        self.key_chatroom = cr().generate_key()
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
        tk.Button(self.nc, text='Generate Key', command=self.generate_key_file).place(x=290, y=150)
        tk.Button(self.nc, text='Create', command=self.create_chatroom).place(x=150, y=200)

    def generate_key_file(self):
        file = filedialog.asksaveasfilename()
        with open(file, 'w') as f:
            f.write(str(self.key_chatroom))
        self.key.delete(0, tk.END)
        self.key.insert(0, self.key_chatroom)

    def create_chatroom(self):
        name = self.name.get()
        key = self.key.get()
        if not name or not key:
            messagebox.showerror('Error', 'Please fill all the fields')
            return
        ch().add_chatroom(name, key)
        messagebox.showinfo('Success', 'Chatroom created')
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
        tk.Button(self.ec, text='Enter Key', command=self.select_key_file).place(x=220, y=150)
        tk.Button(self.ec, text='Join', command=self.join_chatroom).place(x=150, y=200)
    
    def join_chatroom(self):
        name = self.name.get()
        key = self.key.get()
        if not name or not key:
            messagebox.showerror('Error', 'Please fill all the fields')
            return
        chatroom = ch().get_chatroom(name)
        if not chatroom:
            messagebox.showerror('Error', 'Chatroom does not exist')
            return
        if chatroom['key'] != key:
            messagebox.showerror('Error', 'Invalid key')
            return
        self.ec.destroy()
        self.Chat()

    def select_key_file(self):
        file = filedialog.askopenfilename()
        with open(file, 'r') as f:
            self.key_chatroom = f.read()
        self.key.delete(0, tk.END)
        self.key.insert(0, self.key_chatroom)

    def Chat(self):
        tk.Label(self.root, text=f'Welcome {self.user}').place(x=150, y=50)
        tk.Label(self.root, text='Messages').place(x=100, y=75)
        messages = db().get_messages(self.user)
        y = 100
        for message in messages:
            message = cr().decrypt(message)
            tk.Label(self.root, text=message).place(x=100, y=y)
            y += 25
        tk.Label(self.root, text='Message').place(x=100, y=100)
        self.message_user = tk.Entry(self.root).place(x=150, y=100)
        tk.Button(self.root, text="Send", command=self.send_message).place(x=150, y=150)
        tk.Button(self.root, text='Logout', command=self.logout).place(x=150, y=200)

    def send_message(self):
        message = self.message_user.get()
        if not message:
            messagebox.showerror('Error', 'Please fill the message')
            return
        message = cr().encrypt(message)
        db().add_message(self.user, message)
        messagebox.showinfo('Success', 'Message sent')