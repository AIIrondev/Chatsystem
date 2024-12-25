import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import crypting as cr
from database import Database as db

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
    
    def join_chatroom(self):
        self.chatroom = tk.Toplevel(self.root)
        self.chatroom.title('Join Chatroom')
        self.chatroom.geometry('200x100')
        self.chatroom.resizable(False, False)
        tk.Label(self.chatroom, text='Chatroom Name:').place(x=10, y=10)
        tk.Label(self.chatroom, text='Chatroom Key:').place(x=10, y=40)
        self.chatroom_name = tk.Entry(self.chatroom)
        self.chatroom_name.place(x=10, y=30)
        self.chatroom_key = tk.Entry(self.chatroom)
        tk.Button(self.chatroom, text='Join', command=self.join).place(x=10, y=60)
    
    def join(self):
        self.chatroom.destroy()
        self.chatroom = tk.Toplevel(self.root)
        self.chatroom.title('Chatroom')
        self.chatroom.geometry('400x400')
        self.chatroom.resizable(False, False)
        self.messages = tk.Text(self.chatroom)
        self.messages.place(x=10, y=10, width=380, height=300)
        self.message = tk.Entry(self.chatroom)
        self.message.place(x=10, y=320, width=300)
        tk.Button(self.chatroom, text='Send', command=self.send).place(x=320, y=320, width=70)
        tk.Button(self.chatroom, text='Attach', command=self.attach).place(x=320, y=350, width=70)
    
    def create_chatroom(self):
        self.chatroom = tk.Toplevel(self.root)
        self.chatroom.title('Create Chatroom')
        self.chatroom.geometry('200x100')
        self.chatroom.resizable(False, False)
        tk.Label(self.chatroom, text='Chatroom Name:').place(x=10, y=10)
        self.chatroom_name = tk.Entry(self.chatroom)
        self.chatroom_name.place(x=10, y=30)
        tk.Button(self.chatroom, text='Create', command=self.create).place(x=10, y=60)
        generated_key = cr.Crypting().generate_key()
        print(generated_key)
        with open('key.txt', 'w') as f:
            f.write(generated_key)
        messagebox.showwarning('Wichtig', 'The encryption key is now generated: ' + generated_key)
        cr.Crypting().set_key(generated_key)
        
    def create(self):
        self.chatroom.destroy()
        self.chatroom = tk.Toplevel(self.root)
        self.chatroom.title('Chatroom')
        self.chatroom.geometry('400x400')
        self.chatroom.resizable(False, False)
        self.messages = tk.Text(self.chatroom)
        self.messages.place(x=10, y=10, width=380, height=300)
        self.message = tk.Entry(self.chatroom)
        self.message.place(x=10, y=320, width=300)
        tk.Button(self.chatroom, text='Send', command=self.send).place(x=320, y=320, width=70)
        tk.Button(self.chatroom, text='Attach', command=self.attach).place(x=320, y=350, width=70)
    
    def send(self):
        # add encryption here for the message
        cr.Crypting().encrypt(message)
        db().add_message({'name': 'You', 'message': message, 'chat_room': self.chatroom_name.get()})
        message = self.message.get()
        self.message.delete(0, tk.END)
        self.messages.insert(tk.END, 'You: ' + message + '\n')
        self.messages.see(tk.END)

    def attach(self):
        messagebox.showinfo('Info', 'This feature is not implemented yet.')
        pass


if __name__ == '__main__':
    UI().run()