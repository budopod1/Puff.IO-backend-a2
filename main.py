import asyncio
import websockets
import json
import shortsocket
from state import State
from threading import Thread
from uuid import uuid4
from websockets.exceptions import WebSocketException
# from http import HTTPStatus
# from timer import Time
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
        async for message in websocket:
            keys = []
            if message == "connect":
                await websocket.send(create_status({
                    "action": "connect"
                }))
            else:
                keys = [key for key in message] # looks like no change, but bytes iterate weirdly
            for i in range(5):
                # time = Time()
                # time.step("Proccess message")
                client.client_frame(set(keys))
                # time.step("Proccess keys")
                response = client.render_frame()
                # time.step("Create response")
                if response:
                    #print(response)
                    packet = create_packet(
                        response, i == 0
                    )
                    # time.step("Serialize it")
                    await websocket.send(packet)
                    # time.step("Send it")
                else:
                    await websocket.send("F") # in the chat
    except WebSocketException:
        await websocket.close()


def ticking():
    global state
    while True:
        state.tick()


"""
async def health_check(path, request_headers):
    if path != "/ws":
        return HTTPStatus.FOUND, {"Location": "https://puffio.repl.co" + path}, b""
"""


async def start():
    async with websockets.serve(
        serve, 
        "0.0.0.0", 
        80,
        # process_request=health_check,
    ):
        await asyncio.Future()


def main():
    global state, tick_thread
    try:
        state = State()
        
        tick_thread = Thread(target=ticking)
        tick_thread.start()
        
        asyncio.run(start())
    except Exception as e:
        del state
        raise e


if __name__ == "__main__":
    main()
