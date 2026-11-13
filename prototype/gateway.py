import asyncio
import socket

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TCP_HOST = "127.0.0.1"
TCP_PORT = 5000


@app.get("/")
async def home():
    return FileResponse("index.html")


@app.websocket("/ws")
async def chat(websocket: WebSocket):
    username = websocket.query_params.get("username", "").strip()

    if not username or len(username) > 30:
        await websocket.close(code=1008)
        return

    await websocket.accept()

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.settimeout(None)

    try:
        await asyncio.to_thread(
            tcp.connect, (TCP_HOST, TCP_PORT)
        )

        # The existing TCP server asks for a username.
        prompt = await asyncio.to_thread(tcp.recv, 1024)

        if not prompt:
            await websocket.close()
            return

        await asyncio.to_thread(
            tcp.sendall, username.encode("utf-8")
        )

        await websocket.send_json({
            "type": "status",
            "text": f"Connected to chat server as {username}"
        })

        async def tcp_to_browser():
            while True:
                data = await asyncio.to_thread(tcp.recv, 4096)

                if not data:
                    break

                await websocket.send_json({
                    "type": "message",
                    "text": data.decode("utf-8", errors="replace")
                })

        async def browser_to_tcp():
            while True:
                data = await websocket.receive_json()

                if data.get("type") != "message":
                    continue

                message = str(data.get("text", "")).strip()

                if not message or len(message) > 2000:
                    continue

                await asyncio.to_thread(
                    tcp.sendall, message.encode("utf-8")
                )

        receiver = asyncio.create_task(tcp_to_browser())
        sender = asyncio.create_task(browser_to_tcp())

        done, pending = await asyncio.wait(
            [receiver, sender],
            return_when=asyncio.FIRST_COMPLETED
        )

        for task in pending:
            task.cancel()

        await asyncio.gather(*pending, return_exceptions=True)

        for task in done:
            if not task.cancelled() and task.exception():
                raise task.exception()

    except (OSError, WebSocketDisconnect, RuntimeError):
        pass

    finally:
        tcp.close()
        try:
            await websocket.close()
        except Exception:
            pass