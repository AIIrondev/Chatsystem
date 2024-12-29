import os
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

class Crypting:
    def __init__(self):
        self.key = None
    
    def encrypt(self, message):
        if self.key is None:
            raise ValueError("Key must be set before encryption")
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(message.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

    def decrypt(self, message):
        if self.key is None:
            raise ValueError("Key must be set before decryption")
        data = base64.b64decode(message)
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=data[:16])
        return cipher.decrypt_and_verify(data[32:], data[16:32]).decode()

    def set_key(self, key):
        self.key = SHA256.new(key.encode()).digest()

    def generate_key(self):
        self.key = SHA256.new(os.urandom(16)).digest()
        return self.key

    def get_key(self):
        return self.key