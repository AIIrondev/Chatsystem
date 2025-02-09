# User Guide

This text will guide you thrue the hole deployment process.

## First: The Maschine

For minimum specs I would recomend ... .
For a good performing and relativly cheap option the HP ProDesk G1 / G2 used will takle this easyli. But you can always just use any PC or old Laptop that you have lieing around.

## Second: The Operating System

I just used [Ubuntu Server 24.04.1 LTS](https://ubuntu.com/download/server#how-to-install-lts) and installed it on my maschine, now you have to set it up as you like.

## Third: Installing the Chatsystem

Herefore if you use Linux you can just run the [Installing Script](../Installation-Linux.sh) with `source Installing-Linux.sh`. This should install all de depedenses and start the DeploymentCenter.

## Fourth: The Deployment Center 

The Deployment Center is a App that I programmed to start the Website and the Api easy this will work for Linux and Windows, to start the Services just press Deploy. For a further deep dive look at the [Dokumentation](../DeploymentCenter/README_DEPLOY.md).

## Fift: Chatting on the Web

Now you can open the Browser and just type in the app Ip and start by creating a User, when you generated a User Acount you can create a Chatroom to chat with your friends. To chat with your friends give them the Name of the Chatroom and the Password and start interacting with them like in any other Chatsystem you have used.

## Fift(A Second Time): Chatting on the Client app

You can now also start the client app and configure it in the [config Files](../conf/api.conf) to access the right ip. The Process stays the same as the web app.

## Last: Limitations and Security

### Limitations

This app has a few Limitation, because of its focus on the Security aspekt therefore if you would like another feature please just write me at iron.ai.dev@gmail.com or just create a new issue.

### Security

The Security is one of the key parts of this projects, because of this you as the Server owner / deployer can't access the Data that is written on the Data Base without changing the Code at wich point you are completly on your own.

Also Note, this project is under the Apache 2.0 License so read it before doing anything.

[Back](../README.md)