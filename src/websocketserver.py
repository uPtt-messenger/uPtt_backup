import asyncio
import websockets
import pathlib
import ssl
import logging
import json

import traceback
import time
import threading

import Log

RunSession = True
PushMsgList = []
EventLoop = None
ServerStart = False


async def consumer_handler(ws, path):
    global RunSession

    while RunSession:
        try:
            RecvMsg = await ws.recv()
            print(f'recv [{RecvMsg}]')
            await ws.send(RecvMsg)
            print(f'echo complete')
        except Exception as e:
            print('Connection Clsoe')
            RunSession = False
            break


async def producer_handler(ws, path):
    global RunSession
    global PushMsgList

    while RunSession:
        if len(PushMsgList) != 0:
            while len(PushMsgList) != 0:
                PushMsg = PushMsgList.pop()

                print(f'push [{PushMsg}]')
                await ws.send(PushMsg)
        else:
            # print(f'asyncio.sleep')
            # No
            await asyncio.sleep(0.1)


async def handler(websocket, path):
    global RunSession

    RunSession = True
    while RunSession:
        consumer_task = asyncio.ensure_future(
            consumer_handler(websocket, path))

        producer_task = asyncio.ensure_future(
            producer_handler(websocket, path))

        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()


def ServerSetup():
    Log.showValue(
        'WebSocket Server',
        Log.Level.INFO,
        '啟動伺服器',
        50733
    )

    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)

    start_server = websockets.serve(
        handler,
        "localhost",
        50733,
        # ssl=ssl_context
    )

    asyncio.get_event_loop().run_until_complete(start_server)

    global ServerStart
    ServerStart = True

    asyncio.get_event_loop().run_forever()

    Log.show(
        'WebSocket Server',
        Log.Level.INFO,
        '關閉伺服器'
    )


def start():
    t = threading.Thread(target=ServerSetup)
    t.daemon = True
    t.start()


def stop():

    global EventLoop
    global ServerStart
    global RunSession

    while not ServerStart:
        time.sleep(0.1)

    RunSession = False
    asyncio.get_event_loop().stop()


if __name__ == '__main__':
    start()
    # stop()

    while True:
        try:
            time.sleep(1)
        except:
            stop()
            break
        
