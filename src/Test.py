import asyncio
import websockets
import pathlib
import ssl
import logging
import json

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

        msg = await websocket.recv()

        print(f"< {msg}")
        if 'close' == msg:
            break
        greeting = None

logging.basicConfig()

STATE = {"value": 0}

USERS = set()


def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    # 註冊使用者，然後把目前線上人數更新給所有使用者
    await register(websocket)
    print('user join')
    try:
        # 對當下使用者更新數值
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            print(data)
            if data["action"] == "minus":
                STATE["value"] -= 1
                await notify_state()
            elif data["action"] == "plus":
                STATE["value"] += 1
                await notify_state()
            else:
                logging.error("unsupported event: {}", data)
    finally:
        print('user leave')
        await unregister(websocket)

# threading.Thread(target=testNewMsg).start()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = "../GenerateCACert/uPttSSL.pem"
ssl_context.load_cert_chain(localhost_pem)

start_server = websockets.serve(
    counter,
    "localhost",
    50733,
    ssl=ssl_context
)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
