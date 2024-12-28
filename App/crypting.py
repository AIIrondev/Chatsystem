# This is the main file for the encryption and decryption of the messages that is done with the end to end encryption describet in the CRYPT.md file
import os
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

class Crypting:
    def __init__(self):
        self.key = SHA256.new(os.urandom(16)).digest()

    def encrypt(self, message):
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(message.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

    def decrypt(self, message):
        data = base64.b64decode(message)
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=data[:16])
        return cipher.decrypt_and_verify(data[32:], data[16:32]).decode()

    def set_key(self, key):
        self.key = base64.b64decode(key)

    def generate_key(self):
        self.key = base64.b64encode(SHA256.new(os.urandom(16)).digest()).decode()
        self.set_key(self.key)
        return self.key