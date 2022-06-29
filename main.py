import asyncio
import websockets
import json
import shortsocket
from state import State
from threading import Thread
from uuid import uuid4
from websockets.exceptions import WebSocketException
from http import HTTPStatus
import struct
# from timer import Stopwatch
# from shortsocket import Array


state = None

tick_thread = None


def create_status(data):
    return "S" + json.dumps(data)


def create_packet(data, response):
    return (b"R" if response else b"N") + shortsocket.encode(data)


async def serve(websocket):
    try:
        client = state.create_user(uuid4())
        keys = []
        mouseX = 0
        mouseY = 0
        async for message in websocket:
            if isinstance(message, str):
                message = message.encode("UTF-8")
            if message == b"connect":
                await websocket.send(create_status({
                    "action": "connect"
                }))
            elif message == b"exit":
                await websocket.close()
            else:
                msg_type = message[0]
                message = message[1:]
                if msg_type == ord("K"): # Keys
                    keys = [key for key in message] # looks like no change, but bytes iterate weirdly
                elif msg_type == ord("M"):
                    mouseX, mouseY = struct.unpack("ff", message)
            for i in range(5):
                client.client_frame(set(keys))
                response = client.render_frame()
                if response:
                    packet = create_packet(
                        response, i == 0
                    )
                    await websocket.send(packet)
                else:
                    await websocket.send("F") # in the chat
    except WebSocketException:
        await websocket.close()


def ticking():
    global state
    while True:
        state.tick()


async def health_check(path, request_headers):
    if path != "/ws":
        return HTTPStatus.FOUND, {"Location": "https://puffio.repl.co" + path}, b""


async def start_server():
    async with websockets.serve(
        serve, 
        "0.0.0.0", 
        80,
        process_request=health_check,
    ):
        await asyncio.Future()


def main():
    global state, tick_thread
    try:
        state = State()
        
        tick_thread = Thread(target=ticking)
        tick_thread.start()
        
        asyncio.run(start_server())
    except Exception as e:
        del state
        raise e


if __name__ == "__main__":
    main()
