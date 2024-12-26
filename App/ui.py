import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import crypting as cr
from database import Database as db
import os

class UI:
    def run(self):
        self.user = None
        self.root = tk.Tk()
        self.root.title('Crypting')
        self.root.geometry('400x400')
        self.root.resizable(False, False)
        self.register()
        self.root.mainloop()

    def register(self):
        tk.Label(self.root, text='Login with username').place(x=150, y=50)
        tk.Label(self.root, text='Username').place(x=100, y=100)
        self.username = tk.Entry(self.root)
        self.username.place(x=150, y=100)
        tk.Label(self.root, text='Password').place(x=100, y=150)
        self.password = tk.Entry(self.root, show='*')
        self.password.place(x=150, y=150)
        tk.Button(self.root, text='Login', command=self.login_user).place(x=150, y=200)
        tk.Label(self.root, text='Or').place(x=150, y=250)
        tk.Button(self.root, text='Register', command=self.register_user).place(x=150, y=300)
    
    def login_user(self):
        username = self.username.get()
        password = self.password.get()
        if not username or not password:
            messagebox.showerror('Error', 'Please fill all the fields or register')
            return
        user = db().check_nm_pwd(username, password)
        if user:
            self.user = user['username']
            self.mainwindow()
        else:
            messagebox.showerror('Error', 'Invalid credentials or register')

    def register_user(self):
        username = self.username.get()
        password = self.password.get()
        if not username or not password:
            messagebox.showerror('Error', 'Please fill all the fields')
            return
        user = db().get_user(username)
        if user:
            messagebox.showerror('Error', 'User already exists')
            return
        db().add_user(username, password)
        self.user = username
        self.mainwindow()

    def main_window(self):
        self.username.destroy()
        self.password.destroy()
        tk.Label(self.root, text=f'Welcome {self.user}').place(x=150, y=50)
        tk.Label(self.root, text="Placeholder", font=('Arial', 12)).place(x=150, y=100)
        tk.Button(self.root, text='Logout', command=self.logout).place(x=150, y=200)