# This is a private chat room application that allows users to chat with each other in real time.

## Contents

- [Target](#target)
- [Server](#server)
  - [Linux](#linux)
  - [Windows](#windows)
  - [Database](#database)
  - [Website](#website-hosting)
- [Client](#client)
  - [Website](#website)
  - [App](#app)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contributing](#contributing)

## Target

The Target of the Repository is the easy deployment and managment of a Chatsystem for every one. So you can as a Client, just start a server or an old Computer that you dont need any more snd just fire the software up, configure the Ip and you are ready to go.

## Server

Here I will give you a overview of the Server Options you have to deploy the Chatsystem Database.

### Linux

I will User Ubuntu Server to Host the MongoDB and Website 


### Database

Mondo DB is the Database Software that I use for this Project because of the good compatability with Linux and Windows.
For more Information see [Docs](docs/Mongodb.md) or [Python Implementation](docs/database_docs.md).

### Website Hosting

## Client

The clients will interact with the MongoDB server for loging in, generating a Chatroom, writing mesages and join Chatrooms.

### Website

The website will be the most used client because of the better security. For more information read the [WEB](docs/web.md)

## Installation

### Linux Installation

### Windows Installation

## Usage

For the correct usage please read all of the docs or the User Guide.

## Security

The security of the application is very important. The following are some of the security measures that have been implemented:

- **End to End Encryption**: The messages are encrypted before they are sent to the server. The server does not have access to the encryption keys, so it cannot decrypt the messages. This ensures that even if the server is compromised, the messages cannot be read by an attacker. [Read more](docs/CRYPT.md)

- **No SQL Database**: The Database is a no SQL DB and will not be effected by a SQL Injection attack.

## License

This is under the Apache 2.0 license. See the [LICENSE](LICENSE) file for details.
