import os
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from tkinter import messagebox

class Crypting:
    def __init__(self):
        self.key = SHA256.new(os.urandom(16)).digest()

    def encrypt(self, message):
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(message.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

    def decrypt(self, message):
        try:
            data = base64.b64decode(message)
            cipher = AES.new(self.key, AES.MODE_GCM, nonce=data[:16])
            return cipher.decrypt_and_verify(data[32:], data[16:32]).decode()
        except ValueError:
            messagebox.showerror('Error', 'Invalid key')

    def set_key(self, key):
        self.key = key

    def generate_key(self):
        self.key = SHA256.new(os.urandom(16)).digest()
        return self.key

    def get_key(self):
        return self.key