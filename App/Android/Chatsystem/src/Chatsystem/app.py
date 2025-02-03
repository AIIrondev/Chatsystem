import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, LEFT
import requests


class ChatApp(toga.App):
    def startup(self):
        """Initializes the app and sets up the main window."""
        self.user = None
        self.chat_name = None
        self.key_chatroom = None
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.main_window = toga.MainWindow(title=self.name)
        self.main_window.content = self.main_box
        self.login_view()
        self.main_window.show()

    def clear_main_box(self):
        """Clears the main box's children."""
        for child in self.main_box.children:
            self.main_box.remove(child)

    def login_view(self):
        """Displays the login/register screen."""
        self.clear_main_box()

        # Centered Title
        self.main_box.add(toga.Label("Login/Register", style=Pack(padding=10, font_size=16, text_align=CENTER)))

        # Input fields for username and password
        self.username_input = toga.TextInput(placeholder="Username", style=Pack(padding=5, flex=1))
        self.password_input = toga.PasswordInput(placeholder="Password", style=Pack(padding=5, flex=1))

        # Buttons for Login and Register
        button_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding_top=10))
        self.login_button = toga.Button("Login", on_press=self.login_user, style=Pack(padding=5))
        self.register_button = toga.Button("Register", on_press=self.register_user, style=Pack(padding=5))
        button_box.add(self.login_button)
        button_box.add(self.register_button)

        # Add inputs and buttons to the main box
        self.main_box.add(self.username_input)
        self.main_box.add(self.password_input)
        self.main_box.add(button_box)

    def chat_view(self):
        """Displays the chat menu."""
        self.clear_main_box()

        self.main_box.add(toga.Label(f"Welcome {self.user}!", style=Pack(padding=5, font_size=16, text_align=CENTER)))
        
        # Buttons for chatroom options
        self.main_box.add(toga.Button("New Chatroom", on_press=self.new_chatroom, style=Pack(padding=5)))
        self.main_box.add(toga.Button("Enter Chatroom", on_press=self.enter_chatroom, style=Pack(padding=5)))
        self.main_box.add(toga.Button("Logout", on_press=self.logout, style=Pack(padding=5)))

    def new_chatroom(self, widget):
        """Handles new chatroom creation."""
        self.clear_main_box()
        self.main_box.add(toga.Label("Create Chatroom", style=Pack(padding=5, font_size=16)))

        # Input for chatroom name and key
        self.chatroom_name_input = toga.TextInput(placeholder="Chatroom Name", style=Pack(padding=5, flex=1))
        self.chatroom_key_input = toga.TextInput(placeholder="Key", style=Pack(padding=5, flex=1))
        create_button = toga.Button("Create", on_press=self.create_chatroom, style=Pack(padding=5))

        # Add inputs and button
        self.main_box.add(self.chatroom_name_input)
        self.main_box.add(self.chatroom_key_input)
        self.main_box.add(create_button)

    def enter_chatroom(self, widget):
        """Handles entering an existing chatroom."""
        self.clear_main_box()
        self.main_box.add(toga.Label("Enter Chatroom", style=Pack(padding=5, font_size=16)))

        # Input for chatroom name and key
        self.chatroom_name_input = toga.TextInput(placeholder="Chatroom Name", style=Pack(padding=5, flex=1))
        self.chatroom_key_input = toga.TextInput(placeholder="Key", style=Pack(padding=5, flex=1))
        join_button = toga.Button("Join", on_press=self.join_chatroom, style=Pack(padding=5))

        # Add inputs and button
        self.main_box.add(self.chatroom_name_input)
        self.main_box.add(self.chatroom_key_input)
        self.main_box.add(join_button)

    def chatroom_view(self):
        """Displays the chatroom interface."""
        self.clear_main_box()

        self.main_box.add(toga.Label(f"Chatroom: {self.chat_name}", style=Pack(padding=10, font_size=16, text_align=CENTER)))

        # Messages display
        self.messages_container = toga.ScrollContainer(style=Pack(flex=1, padding=5))
        self.messages_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        self.messages_container.content = self.messages_box

        # Input and Buttons for Sending/Refreshing
        input_box = toga.Box(style=Pack(direction=ROW, padding=5))
        self.message_input = toga.TextInput(placeholder="Enter your message", style=Pack(flex=1, padding_right=5))
        send_button = toga.Button("Send", on_press=self.send_message, style=Pack(padding=5))
        input_box.add(self.message_input)
        input_box.add(send_button)

        self.main_box.add(self.messages_container)
        self.main_box.add(input_box)
        self.main_box.add(toga.Button("Back", on_press=self.chat_view, style=Pack(padding=5)))

        # Load messages
        self.update_messages()

    def update_messages(self, widget=None):
        """Updates the chatroom messages."""
        self.clear_main_box()
        try:
            response = self.request('/receive_message', 'GET', {'chat_room': self.chat_name})
            messages = response.get('message', [])
            for msg in messages:
                self.messages_box.add(
                    toga.Label(f"{msg['user']}: {msg['message']} ({msg['Date']})", style=Pack(padding=2, text_align=LEFT))
                )
        except Exception as e:
            self.show_error(f"Failed to load messages: {e}")

    def send_message(self, widget):
        """Sends a message."""
        message = self.message_input.value
        if not message:
            self.show_error("Message cannot be empty!")
            return
        try:
            response = self.request('/send_message', 'POST', {
                'chat_name': self.chat_name,
                'key': self.key_chatroom,
                'message': message,
                'user': self.user
            })
            self.update_messages()
            self.message_input.value = ""
        except Exception as e:
            self.show_error(f"Failed to send message: {e}")

    def login_user(self, widget):
        """Logs in the user."""
        username = self.username_input.value
        password = self.password_input.value
        try:
            if not username or not password:
                self.show_error("Please fill all the fields or register")
                return
            response = self.request('/login', 'POST', {'username': username, 'password': password})
            if response.get('success'):
                self.user = response['user']
                self.chat_view()
            else:
                self.show_error("Invalid credentials or register")
        except Exception as e:
            self.show_error(f"Failed to login: {e}")

    def register_user(self, widget):
        """Registers a new user."""
        username = self.username_input.value
        password = self.password_input.value
        try:
            response = self.request('/register', 'POST', {'username': username, 'password': password})
            if response.get('success'):
                self.user = username
                self.chat_view()
            else:
                self.show_error("Failed to register.")
        except Exception as e:
            self.show_error(f"Failed to register: {e}")

    def create_chatroom(self, widget):
        """Creates a new chatroom."""
        name = self.chatroom_name_input.value
        key = self.chatroom_key_input.value
        try:
            response = self.request('/create_chatroom', 'POST', {'name': name, 'key': key})
            if response.get('success'):
                self.show_info("Chatroom created successfully.")
                self.chat_view()
            else:
                self.show_error("Failed to create chatroom.")
        except Exception as e:
            self.show_error(f"Failed to create chatroom: {e}")

    def join_chatroom(self, widget):
        """Joins an existing chatroom."""
        name = self.chatroom_name_input.value
        key = self.chatroom_key_input.value
        try:
            response = self.request('/join_chatroom', 'POST', {'chat_name': name, 'key': key})
            if response.get('success'):
                self.chat_name = name
                self.key_chatroom = key
                self.chatroom_view()
            else:
                self.show_error("Failed to join chatroom.")
        except Exception as e:
            self.show_error(f"Failed to join chatroom: {e}")

    def logout(self, widget):
        """Logs out the user."""
        self.user = None
        self.login_view()

    def show_error(self, message):
        """Display an error message to the user."""
        self.main_window.info_dialog("Error", message)

    def show_info(self, message):
        """Displays an informational message."""
        self.main_window.info_dialog("Info", message)

    def request(self, endpoint, method, data=None):
        """Send a request to the server."""
        try:
            url = f"http://127.0.0.1:4999{endpoint}"
            response = requests.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.show_error(f"Request failed: {e}")
            raise

class TestAPI:
    def __init__(self):
        self.url = 'http://127.0.0.1:4999'
        self.endpoint = '/test_connection'
        self.method = 'GET'
        self.test_connection()
        
    def test_connection(self):
        try:
            response = requests.get(self.url + self.endpoint)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            print(response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Connection test failed: {e}")
            return {"error": str(e)}


def main():
    return ChatApp("Chat Application", "org.example.chatapp")
