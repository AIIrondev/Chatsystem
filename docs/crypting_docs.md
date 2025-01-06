# Crypting Class Documentation

This document provides an overview of the `Crypting` class for encryption and decryption using AES-GCM mode. The `Crypting` class enables secure message handling by encrypting and decrypting data with a symmetric key.

## Requirements

The `Crypting` class depends on the following Python libraries:

- `os`
- `base64`
- `hashlib`
- `cryptography`

Make sure to install the `cryptography` library before using this class:

```bash
pip install cryptography
```

## Class Overview

### `Crypting`

#### Methods

- `__init__(self)`
  Initializes the `Crypting` class. Sets the encryption key to `None`.

- `set_key(self, key)`
  Sets the encryption key for the instance.
  - **Parameters**:
    - `key` (str): The string key to be used for encryption and decryption. Internally, it is hashed using SHA-256 to produce a 256-bit key.

- `get_key(self)`
  Retrieves the current encryption key (hashed).
  - **Returns**:
    - `bytes`: The hashed key as a 256-bit byte array.

- `encrypt(self, message)`
  Encrypts a message using AES-GCM.
  - **Parameters**:
    - `message` (str): The plaintext message to be encrypted.
  - **Returns**:
    - `str`: The base64-encoded string containing the nonce, authentication tag, and ciphertext.
  - **Raises**:
    - `ValueError`: If the encryption key has not been set.

- `decrypt(self, message)`
  Decrypts a message previously encrypted with `encrypt`.
  - **Parameters**:
    - `message` (str): The base64-encoded encrypted message.
  - **Returns**:
    - `str`: The decrypted plaintext message.
  - **Raises**:
    - `ValueError`: If the encryption key has not been set.

## Usage Examples

### Importing and Initializing

```python
from crypting import Crypting

# Initialize Crypting class
crypt = Crypting()
```

### Setting the Key

```python
# Set a key (shared secret)
crypt.set_key("my_secret_password")

# Get the hashed key (optional)
hashed_key = crypt.get_key()
print(f"Hashed Key: {hashed_key}")
```

### Encrypting a Message

```python
# Encrypt a message
plaintext = "Hello, secure world!"
encrypted_message = crypt.encrypt(plaintext)
print(f"Encrypted Message: {encrypted_message}")
```

### Decrypting a Message

```python
# Decrypt the previously encrypted message
decrypted_message = crypt.decrypt(encrypted_message)
print(f"Decrypted Message: {decrypted_message}")
```

### Full Example

```python
from crypting import Crypting

# Initialize and set the key
crypt = Crypting()
crypt.set_key("super_secret")

# Encrypt a message
original_message = "This is a confidential message."
encrypted = crypt.encrypt(original_message)
print(f"Encrypted: {encrypted}")

# Decrypt the message
decrypted = crypt.decrypt(encrypted)
print(f"Decrypted: {decrypted}")

# Ensure the original and decrypted messages match
assert original_message == decrypted
```

## Error Handling

### Key Not Set
If you attempt to call `encrypt` or `decrypt` without setting a key, a `ValueError` will be raised:

```python
ValueError: Key must be set before encryption
```

Ensure you set the key using `set_key` before performing encryption or decryption.

## Security Notes

1. **Key Management**: Use a strong, randomly generated key and ensure it is kept secret.
2. **AES-GCM Mode**: This mode provides both encryption and message authentication. The tag ensures the integrity of the encrypted message.
3. **Nonces**: A new random nonce is generated for every encryption. Never reuse a nonce with the same key.

## Dependencies

- Python 3.6 or higher
- `cryptography` library

For more details on AES-GCM and cryptographic practices, refer to the [Cryptography documentation](https://cryptography.io/).

