# Website Client

This is a simple web application built using Flask that includes a chat box functionality. Users can send and receive messages in real-time.

## Project Structure

```
website
├── templates
│   ├── base.html
|   ├── chat.html
|   ├── enter_chatroom.html
|   ├── login.html
|   ├── main.html
|   ├── new_chatroom.html
|   └── register.html
├── static
│   ├── css
│   │   └── styles.css
│   └── js
│       └── scripts.js
├── app.py
├── crypting.py
├── database.py
└── requirements.txt
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd website
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To start the Flask application, run the following command:

```
python app.py
```

The application will be accessible at `http://127.0.0.1:5000`.

## Usage

Once the application is running, you can open your web browser and navigate to the provided URL to access the chat box. Messages can be sent and received in real-time.

## License

This project is licensed under the MIT License.