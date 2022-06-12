import asyncio
import websockets
import json
import shortsocket
from state import State
from threading import Thread
# from http import HTTPStatus
# from timer import Time
# from shortsocket import Array


state = None

tick_thread = None


def create_status(data):
    return "S" + json.dumps(data)


def create_packet(data):
    return b"P" + shortsocket.encode(data)


async def main(websocket):
    user = state.create_user("user1")
    client = state.create_client(user)
    async for message in websocket:
        if message == "connect":
            await websocket.send(create_status({
                "action": "connect"
            }))
        if message:
            print([byte for byte in message])
        response = client.render()
        #print(response)
        packet = create_packet(
            response
        )
        # print(shortsocket.decode(packet[1:]))
        # print(len(shortsocket.encode(response)), len(str(response)))
        await websocket.send(packet)


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
        main, 
        "0.0.0.0", 
        80,
        # process_request=health_check,
    ):
        await asyncio.Future()


def setup():
    global state, tick_thread
    state = State()
    
    tick_thread = Thread(target=ticking)
    tick_thread.start()
    
    asyncio.run(start())


if __name__ == "__main__":
    try:
        setup()
    except Exception as e:
        del state
        raise e
