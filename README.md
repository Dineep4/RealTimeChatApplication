# Real-Time Multi-User Chat Application Using TCP Socket Programming

## About the Project

The **Real-Time Multi-User Chat Application** is a networking-based project developed using Python TCP Socket Programming. It allows multiple users to communicate with each other in real time over a network.

The application uses socket communication to establish connections between clients and a server, enabling users to exchange messages efficiently.

## Objectives

- To develop a real-time multi-user chat application.
- To understand TCP socket programming.
- To establish communication between multiple clients.
- To exchange messages over a local network.
- To understand client-server architecture.

## Technologies Used

- **Python** – Backend programming and socket communication.
- **TCP Socket Programming** – Reliable communication between clients and server.
- **FastAPI** – Gateway and application communication.
- **Uvicorn** – ASGI server.
- **HTML, CSS, JavaScript** – User interface.

## System Architecture

The application follows a client-server architecture.

1. The server listens for incoming client connections.
2. Clients connect to the server through the network.
3. Users send messages through the application interface.
4. The server handles communication between connected clients.
5. Messages are delivered to the intended connected users.

## Project Structure

```text
RealTimeChatApplication/
│
├── server.py
├── gateway.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
│
└── README.md
```

*Note: Update this structure according to your actual project files.*

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/RealTimeChatApplication.git
```

### 2. Open the Project Folder

```bash
cd RealTimeChatApplication
```

### 3. Install Required Packages

```bash
pip install fastapi uvicorn
```

Install any additional dependencies used in your project.

### 4. Start the TCP Server

```bash
python server.py
```

### 5. Start the Gateway

```bash
uvicorn gateway:app --host 0.0.0.0 --port 8080
```

### 6. Open the Application

Open the following address in your browser:

```text
http://localhost:8080
```

To access the application from another device on the same network, use:

```text
http://YOUR-LAPTOP-IP:8080
```

## Features

- Real-time message communication.
- Multiple client connections.
- TCP-based communication.
- Client-server architecture.
- Network-based access through a browser.
- User-friendly interface.

## Advantages

- Enables communication between multiple users.
- Uses TCP for reliable and ordered data transmission.
- Demonstrates practical computer networking concepts.
- Can be tested using multiple devices on the same network.

## Future Enhancements

- Private one-to-one messaging.
- User authentication and registration.
- Group chat functionality.
- Message history storage.
- File sharing.
- End-to-end encryption.

## Conclusion

This project demonstrates the practical implementation of TCP Socket Programming through a real-time multi-user chat application. It provides an understanding of network communication, client-server architecture, and real-time data exchange using Python.
