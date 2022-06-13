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


async def serve(websocket):
    client = state.create_user("user1")
    async for message in websocket:
        keys = []
        if message == "connect":
            await websocket.send(create_status({
                "action": "connect"
            }))
        else:
            keys = [key for key in message] # looks like no change, but bytes iterate weirdly
        # if message:
        #     print([byte for byte in message])
        client.got_keys(keys)
        response = client.consume_frame()
        if response:
            #print(response)
            packet = create_packet(
                response
            )
            # print(shortsocket.decode(packet[1:]))
            # print(len(shortsocket.encode(response)), len(str(response)))
            await websocket.send(packet)
        else:
            await websocket.send("F") # in the chat


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
