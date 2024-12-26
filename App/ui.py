import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import crypting as cr
from database import Database as db
from database import User as us
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
        self.register_window = tk.Toplevel(self.root)
        tk.Label(self.register_window, text='Login with username').place(x=150, y=50)
        tk.Label(self.register_window, text='Username').place(x=100, y=100)
        self.username = tk.Entry(self.register_window)
        self.username.place(x=150, y=100)
        tk.Label(self.register_window, text='Password').place(x=100, y=150)
        self.password = tk.Entry(self.register_window, show='*')
        self.password.place(x=150, y=150)
        tk.Button(self.register_window, text='Login', command=self.login_user).place(x=150, y=200)
        tk.Label(self.register_window, text='Or').place(x=150, y=250)
        tk.Button(self.register_window, text='Register', command=self.register_user).place(x=150, y=300)
    
    def login_user(self):
        username = self.username.get()
        password = self.password.get()
        if not username or not password:
            messagebox.showerror('Error', 'Please fill all the fields or register')
            return
        user = us().check_nm_pwd(username, password)
        if user:
            self.user = user['username']
            self.main_window()
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
        us().add_user(username, password)
        self.user = username
        self.main_window()

    def logout(self):
        self.user = None
        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.register()

    def main_window(self):
        self. lbl_wel = tk.Label(self.root, text=f'Welcome {self.user}').place(x=150, y=50)
        self.lbl_plc = tk.Label(self.root, text="Placeholder", font=('Arial', 12)).place(x=150, y=100)
        self.btn_logo = tk.Button(self.root, text='Logout', command=self.logout).place(x=150, y=200)