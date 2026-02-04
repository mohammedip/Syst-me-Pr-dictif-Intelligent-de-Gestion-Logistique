import asyncio
import websockets
import socket

HOST = "127.0.0.1"
TCP_PORT = 9009
WS_URL = "ws://fastapi_stream:8000/ws/data"

async def bridge():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, TCP_PORT))
    s.listen(1)
    print(f"TCP Server listening on {HOST}:{TCP_PORT} ...")
    conn, _ = s.accept()

    async with websockets.connect(WS_URL) as websocket:
        while True:
            msg = await websocket.recv()
            conn.send((msg + "\n").encode("utf-8"))

asyncio.run(bridge())
