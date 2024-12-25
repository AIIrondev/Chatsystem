# This is the main file for the encryption and decryption of the messages that is done with the end to end encryption describet in the CRYPT.md file
import os
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
