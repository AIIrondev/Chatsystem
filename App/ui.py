import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import crypting as cr

class UI:
    def run(self):
        self.root = tk.Tk()
        self.root.title('Crypting')
        self.root.geometry('400x400')
        self.root.resizable(False, False)
        self.chat()
        self.root.mainloop()

    def chat(self):
        tk.Label(self.root, text='Chat', font=('Arial', 12)).place(x=10, y=10)
        tk.Button(self.root, text='Create Chatroom', command=self.create_chatroom).place(x=10, y=40)
        tk.Button(self.root, text='Join Chatroom', command=self.join_chatroom).place(x=10, y=70)
        tk.Label(self.root, text='Version 0.1.0', font=('Arial', 8)).place(x=10, y=380)
        
    def create_chatroom(self):
        pass

if __name__ == '__main__':
    UI().run()