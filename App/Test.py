from crypting import Crypting

# Initialize the Crypting class
crypto = Crypting()

# Set a key
crypto.set_key("my_secret_password")

# Encrypt a message
original_message = "This is a secret message."
encrypted_message = crypto.encrypt(original_message)
print(f"Encrypted Message: {encrypted_message}")

# Decrypt the message
decrypted_message = crypto.decrypt(encrypted_message)
print(f"Decrypted Message: {decrypted_message}")

# Verify the decryption
if original_message == decrypted_message:
    print("Success: Decrypted message matches the original.")
else:
    print("Error: Decrypted message does not match.")


#Encryption Key: Password
# e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221a
#Decryption Key: Password 
# e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221a