import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class Crypting:
    def __init__(self):
        self.key = None

    def encrypt(self, message):
        if self.key is None:
            raise ValueError("Key must be set before encryption")
        nonce = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
        tag = encryptor.tag
        return base64.b64encode(nonce + tag + ciphertext).decode()

    def decrypt(self, message):
        if self.key is None:
            raise ValueError("Key must be set before decryption")
        data = base64.b64decode(message)
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        return (decryptor.update(ciphertext) + decryptor.finalize()).decode()

    def set_key(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def get_key(self):
        return self.key
