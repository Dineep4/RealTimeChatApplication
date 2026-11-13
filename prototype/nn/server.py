import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = {}
lock = threading.Lock()


def broadcast(message, sender=None):
    with lock:
        for username, conn in clients.items():
            if username != sender:
                try:
                    conn.send(message.encode())
                except:
                    pass


def handle_client(conn, addr):
    username = None

    try:
        conn.send("USERNAME".encode())
        username = conn.recv(1024).decode().strip()

        with lock:
            clients[username] = conn

        print(f"{username} connected from {addr}")

        broadcast(f"SYSTEM:{username} joined the chat.", username)

        while True:
            data = conn.recv(1024)

            if not data:
                break

            message = data.decode()

            if message == "/users":
                with lock:
                    users = ", ".join(clients.keys())

                conn.send(f"USERS:{users}".encode())

            else:
                print(f"{username}: {message}")
                broadcast(f"{username}: {message}", username)

    except Exception as e:
        print("Error:", e)

    finally:
        if username:
            with lock:
                clients.pop(username, None)

            broadcast(f"SYSTEM:{username} left the chat.", username)

        conn.close()
        print(f"{username} disconnected")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen()

    print(f"Server running on port {PORT}...")
    print("Waiting for users...")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        )

        thread.start()


if __name__ == "__main__":
    start_server()