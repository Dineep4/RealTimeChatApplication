import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox


SERVER_IP = "127.0.0.1"
PORT = 5000


class ChatClient:

    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Chat Application")
        self.root.geometry("600x650")

        self.username = simpledialog.askstring(
            "Login",
            "Enter your username:",
            parent=root
        )

        if not self.username:
            root.destroy()
            return

        try:
            self.sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.sock.connect((SERVER_IP, PORT))

            # Server asks for username
            self.sock.recv(1024)
            self.sock.send(self.username.encode())

        except Exception as e:
            messagebox.showerror(
                "Connection Error",
                f"Could not connect to server.\n\n{e}"
            )
            root.destroy()
            return

        self.create_ui()

        threading.Thread(
            target=self.receive_messages,
            daemon=True
        ).start()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def create_ui(self):

        # Header
        header = tk.Frame(
            self.root,
            bg="#075E54",
            height=60
        )

        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text=f"💬 ChatApp     {self.username}",
            bg="#075E54",
            fg="white",
            font=("Arial", 16, "bold")
        )

        title.pack(side=tk.LEFT, padx=15, pady=15)

        users_button = tk.Button(
            header,
            text="Users",
            command=self.show_users
        )

        users_button.pack(
            side=tk.RIGHT,
            padx=10
        )

        # Chat area
        self.chat_area = tk.Text(
            self.root,
            state=tk.DISABLED,
            font=("Arial", 12),
            wrap=tk.WORD
        )

        self.chat_area.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        # Bottom area
        bottom = tk.Frame(self.root)

        bottom.pack(
            fill=tk.X,
            padx=10,
            pady=10
        )

        self.message_entry = tk.Entry(
            bottom,
            font=("Arial", 12)
        )

        self.message_entry.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            ipady=8
        )

        self.message_entry.bind(
            "<Return>",
            lambda event: self.send_message()
        )

        send_button = tk.Button(
            bottom,
            text="Send ➤",
            command=self.send_message,
            bg="#128C7E",
            fg="white",
            font=("Arial", 11, "bold")
        )

        send_button.pack(
            side=tk.RIGHT,
            padx=(10, 0)
        )

    def send_message(self):

        message = self.message_entry.get().strip()

        if not message:
            return

        try:
            self.sock.send(message.encode())

            self.display_message(
                f"You: {message}"
            )

            self.message_entry.delete(0, tk.END)

        except:
            messagebox.showerror(
                "Error",
                "Message could not be sent."
            )

    def receive_messages(self):

        while True:

            try:
                data = self.sock.recv(4096)

                if not data:
                    break

                message = data.decode()

                if message.startswith("USERS:"):
                    continue

                self.display_message(message)

            except:
                break

    def display_message(self, message):

        self.chat_area.config(state=tk.NORMAL)

        self.chat_area.insert(
            tk.END,
            message + "\n\n"
        )

        self.chat_area.see(tk.END)

        self.chat_area.config(state=tk.DISABLED)

    def show_users(self):

        try:
            self.sock.send("/users".encode())

            data = self.sock.recv(4096).decode()

            if data.startswith("USERS:"):
                users = data[6:]

                messagebox.showinfo(
                    "Online Users",
                    users if users else "No users online."
                )

        except:
            messagebox.showerror(
                "Error",
                "Could not get users."
            )

    def close_app(self):

        try:
            self.sock.close()
        except:
            pass

        self.root.destroy()


if __name__ == "__main__":

    root = tk.Tk()

    app = ChatClient(root)

    root.mainloop()