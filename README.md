# Private Chat Room Application

This is a private chat room application that allows users to chat with each other in real time.

## Contents

- [Target](#target)
- [Server](#server)
  - [Linux](#linux)
  - [Windows](#windows)
  - [Database](#database)
  - [Website Hosting](#website-hosting)
- [Client](#client)
  - [Website](#website)
  - [App](#app)
- [Installation](#installation)
  - [Linux Installation](#linux-installation)
  - [Windows Installation](#windows-installation)
- [Usage](#usage)
- [Security](#security)
- [License](#license)

## Target

The primary goal of this repository is to provide an easy-to-deploy and manage chat system. As a client, you can start a server on an old computer or any machine you no longer need, configure the IP, and you’re ready to go.

## Server

Here, I provide an overview of the server options available for deploying the chat system and its database.

### Linux

I use **Ubuntu Server** to host MongoDB, the website, and the API. To assist with deployment, I have created a tool called the [Deployment Center](DeploymentCenter/README_DEPLOY.md) to help streamline the process.

### Windows

You can also deploy the server on Windows using the same tool, though additional steps may be required to install and configure MongoDB.

### Database

This application uses **MongoDB** as the database because of its excellent compatibility with both Linux and Windows environments. For more information on how the database is used, refer to the [MongoDB Documentation](docs/Mongodb.md) or the [Python Database Implementation](docs/database_docs.md).

### Website Hosting

The website is a **Flask** application that interacts with the database and serves the web app. 

## Client

Clients will interact with the MongoDB server to log in, generate chatrooms, send messages, and join chatrooms. For further details, refer to the [Client App Documentation](App/README_APP.md).

### Website

The website will be the most commonly used client because it offers enhanced security. For more information on setting up and using the website client, refer to the [Web Client Documentation](DeploymentCenter/web/README_WEB.md).

## Installation

To get the application up and running, follow these steps for installation.

### Linux Installation

1. **Install Dependencies**: 
    - Ensure that you have Python 3 and pip installed. You can install them using:
      ```bash
      sudo apt update
      sudo apt install python3 python3-pip
      ```
    - Install MongoDB:
      ```bash
      sudo apt install mongodb
      ```
    - Install Flask (for the website server):
      ```bash
      pip install Flask
      ```

2. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/chat-room.git
    cd chat-room
    ```

3. **Configure the Server**:
    - Follow the [Deployment Center](DeploymentCenter/README_DEPLOY.md) instructions to set up the server and MongoDB on your machine.
    - Update configuration files to set the correct IP address for the server.

4. **Start the Server**:
    - Run the MongoDB service:
      ```bash
      sudo service mongodb start
      ```
    - Launch the Flask website:
      ```bash
      python3 app.py
      ```

5. **Access the Website**:
    - Open a web browser and navigate to `http://<your-server-ip>:5000`.

OR just run the Installation-Linux.sh file as `$ source Installation-Linux.sh`.

### Windows Installation

1. **Install Dependencies**:
    - Install Python 3 and pip from the [official Python website](https://www.python.org/downloads/).
    - Install MongoDB following the [MongoDB installation guide for Windows](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/).
    - Install Flask:
      ```bash
      pip install Flask
      ```

2. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/chat-room.git
    cd chat-room
    ```

3. **Configure the Server**:
    - Follow the [Deployment Center](DeploymentCenter/README_DEPLOY.md) instructions to set up the server and MongoDB on your Windows machine.
    - Update the configuration files to set the correct IP address for the server.

4. **Start the Server**:
    - Run MongoDB manually if necessary (using `mongod` in the command prompt).
    - Start the Flask website by running:
      ```bash
      python app.py
      ```

5. **Access the Website**:
    - Open a web browser and navigate to `http://<your-server-ip>:5000`.

## Usage

For proper usage, please read through all of the documentation, or refer to the [User Guide](docs/user_guide.md).

## Security

The security of the application is a top priority. Below are some of the key security measures implemented:

- **End-to-End Encryption**: Messages are encrypted before being sent to the server, ensuring that even if the server is compromised, the messages remain unreadable by attackers. The server does not have access to the encryption keys. [Learn more about encryption](docs/crypting_docs.md).

- **NoSQL Database**: MongoDB is used as the database, which mitigates the risk of SQL injection attacks.

## License

This project is licensed under the Apache 2.0 license. See the [LICENSE](LICENSE) file for more details.
