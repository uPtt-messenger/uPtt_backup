import asyncio
import websockets

import time
import threading


greeting = None


def testNewMsg():

    global greeting

    for _ in range(10):
        time.sleep(2)
        greeting = 'New Msg'


async def hello(websocket, path):

    global greeting

    name = await websocket.recv()
    print(f"< {path} {name}")

    greeting = f"Hello {name}!"

    while True:
        if greeting is None:
            time.sleep(0.05)
            continue
        await websocket.send(greeting)
        print(f"> {greeting}")
        greeting = None

threading.Thread(target=testNewMsg).start()

start_server = websockets.serve(hello, "localhost", 50730)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
