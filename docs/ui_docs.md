# Documentation for Chat Application UI Class

## Overview
This documentation provides an explanation of the `UI` class implemented using the `tkinter` module. The `UI` class is part of a chat application that supports user registration, login, chatroom creation, joining chatrooms, sending/receiving encrypted messages, and deleting messages.

## Dependencies
- `tkinter`: Used for GUI components.
- `messagebox`: Provides message dialog boxes.
- `crypting.Crypting`: Handles encryption and decryption.
- `cryptography.exceptions`: Catches decryption errors.
- `database.Database`: Manages messages and chatrooms.
- `database.User`: Handles user data.
- `database.Chatroom`: Handles chatroom data.
- `datetime.datetime`: Formats timestamps.

---

## Class: `UI`

### Methods

### `run_main_loop()`
Initializes and runs the main application loop. If a chatroom window is open, it is destroyed before the main window is launched.

---

### `register()`
Launches the registration/login window.

#### GUI Components:
- Username and password entry fields.
- Buttons for login and registration.

---

### `login_user()`
Authenticates the user using the provided credentials.

#### Behavior:
- Displays error messages for invalid credentials.
- Proceeds to the main application window on successful login.

---

### `register_user()`
Registers a new user if the username does not already exist and the password meets strength requirements.

#### Behavior:
- Displays error messages for invalid inputs.
- Saves the user and opens the main application window.

---

### `logout()`
Logs out the current user and redirects them to the login/registration window.

---

### `main_window()`
Creates the main application window.

#### Features:
- Buttons to create a new chatroom, join a chatroom, or log out.

---

### `new_chatroom()`
Opens a window to create a new chatroom.

#### GUI Components:
- Fields to input chatroom name and key.
- Button to create the chatroom.

---

### `create_chatroom()`
Creates a chatroom with the provided name and key. Encrypts a welcome message for the chatroom.

#### Behavior:
- Displays error messages for invalid inputs.
- Stores the chatroom details securely.

---

### `enter_chatroom()`
Opens a window to join an existing chatroom.

#### GUI Components:
- Fields to input chatroom name and key.
- Button to join the chatroom.

---

### `join_chatroom()`
Validates chatroom details and opens the chatroom if authentication is successful.

#### Behavior:
- Displays error messages for invalid inputs or incorrect keys.
- Opens the chat window.

---

### `Chat()`
Launches the chatroom interface, displaying messages and providing options to send or delete messages.

#### Features:
- Displays decrypted messages.
- Entry field to send new messages.
- Buttons to refresh, delete messages, or return to the main menu.

---

### `back()`
Closes the current chatroom and returns to the main menu.

---

### `update_messages()`
Fetches and decrypts messages for the current chatroom. Populates the chatroom interface with messages.

#### Behavior:
- Displays error messages if decryption fails.
- Handles encrypted and user-specific data.

---

### `refresh()`
Updates the chatroom messages by calling `update_messages()`.

---

### `send_message()`
Encrypts and sends a new message to the chatroom.

#### Behavior:
- Displays error messages for invalid inputs or failures.
- Updates the chatroom with the new message.

---

### `option_menu(message_id)`
Displays a menu to perform actions on a selected message (e.g., delete).

---

### `delete_message(message_id)`
Deletes a message from the database by its ID and refreshes the chatroom.

---

### `close()`
Closes all application windows and exits.

---

## Example Usage

### Starting the Application
```python
from ui import UI

app = UI()
app.register()  # Launches the registration/login window
```

### Creating a Chatroom
1. Log in to the application.
2. Click on "New Chatroom".
3. Enter a chatroom name and a key.
4. Click "Create" to create the chatroom.

### Joining a Chatroom
1. Log in to the application.
2. Click on "Enter Chatroom".
3. Enter the chatroom name and the key.
4. Click "Join" to join the chatroom.

### Sending Messages
1. Open a chatroom.
2. Type a message in the entry field.
3. Click "Send" to send the message.
