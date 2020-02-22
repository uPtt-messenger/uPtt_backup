import asyncio
import websockets
import traceback
import time
import threading

import log
from msg import Msg

RunSession = True
Command = None
Config = None
ServerStart = False

Thread = None


async def consumer_handler(ws, path):
    global RunSession
    global Command

    while RunSession:
        try:
            recv_msg_str = await ws.recv()
            print(f'recv str [{recv_msg_str}]')
            recv_msg = Msg(strobj=recv_msg_str)
            Command.analyze(recv_msg)
            # await ws.send(recv_msg)
            # print(f'echo complete')
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            print('Connection Clsoe')
            RunSession = False
            break


async def producer_handler(ws, path):
    global RunSession
    global Command

    while RunSession:
        if len(Command.PushMsg) != 0:
            while len(Command.PushMsg) != 0:
                push_msg = Command.PushMsg.pop()

                print(f'push [{push_msg}]')
                await ws.send(push_msg)
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

        _, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()


def ServerSetup():
    log.showvalue(
        'WebSocket Server',
        log.Level.INFO,
        '啟動伺服器',
        f'ws://127.0.0.1:{Config.Port}'
    )

    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)

    start_server = websockets.serve(
        handler,
        "localhost",
        Config.Port,
        # ssl=ssl_context
    )

    asyncio.get_event_loop().run_until_complete(start_server)

    global ServerStart
    ServerStart = True

    asyncio.get_event_loop().run_forever()

    log.show(
        'WebSocket Server',
        log.Level.INFO,
        '關閉伺服器'
    )


def start():
    global Thread
    Thread = threading.Thread(target=ServerSetup)
    Thread.daemon = True
    Thread.start()


def stop():

    global ServerStart
    global RunSession
    global Thread

    log.show(
        'WebSocket Server',
        log.Level.INFO,
        '執行終止程序'
    )

    while not ServerStart:
        time.sleep(0.1)

    RunSession = False
    asyncio.get_event_loop().stop()

    # Thread.join()
    log.show(
        'WebSocket Server',
        log.Level.INFO,
        '終止程序完成'
    )


if __name__ == '__main__':
    start()
    # stop()

    while True:
        try:
            time.sleep(1)
        except Exception:
            stop()
            break
