import asyncio
import websockets
import traceback
import time
import threading

import log
from msg import Msg

run_session = True
command = None
config = None
console = None
server_start = False

thread = None


async def consumer_handler(ws, path):
    global run_session
    global command
    global console

    while run_session:
        try:
            try:
                recv_msg_str = await ws.recv()
            except Exception as e:
                print('Connection Close: recv fail')
                run_session = False
                break

            log.show_value(
                'WebSocket Server',
                log.level.INFO,
                '收到字串',
                recv_msg_str
            )
            log.show_value(
                'WebSocket Server',
                log.level.INFO,
                '路徑',
                path
            )

            recv_msg = Msg(strobj=recv_msg_str)

            if 'token=' in path:
                token = path[path.find('token=') + len('token='):]
                if '&' in token:
                    token = token[:token.find('&')]
                log.show_value(
                    'WebSocket Server',
                    log.level.INFO,
                    '收到權杖',
                    token
                )
                recv_msg.add(Msg.key_token, token)

            # print(str(recv_msg))
            command.analyze(recv_msg)
            # await ws.send(recv_msg)
            # print(f'echo complete')
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            print('Connection Close')
            run_session = False
            break


async def producer_handler(ws, path):
    global run_session
    global command

    while run_session:
        if len(command.push_msg) != 0:
            while len(command.push_msg) != 0:
                push_msg = command.push_msg.pop()

                print(f'push [{push_msg}]')
                try:
                    await ws.send(push_msg)
                except websockets.exceptions.ConnectionClosedOK:
                    print(f'push fail')
                    break
        else:
            # print(f'asyncio.sleep')
            # No
            await asyncio.sleep(0.1)


async def handler(websocket, path):
    global run_session

    run_session = True
    while run_session:
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


def server_setup():
    log.show_value(
        'WebSocket Server',
        log.level.INFO,
        '啟動伺服器',
        f'ws://127.0.0.1:{config.port}'
    )

    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)

    start_server = websockets.serve(
        handler,
        "localhost",
        config.port,
        # ssl=ssl_context
    )

    asyncio.get_event_loop().run_until_complete(start_server)

    global server_start
    server_start = True

    asyncio.get_event_loop().run_forever()

    log.show(
        'WebSocket Server',
        log.level.INFO,
        '關閉伺服器'
    )


def start():
    global thread
    thread = threading.Thread(
        target=server_setup,
        daemon=True
    )
    thread.start()
    time.sleep(0.5)


def stop():
    global server_start
    global run_session
    global thread

    log.show(
        'WebSocket Server',
        log.level.INFO,
        '執行終止程序'
    )

    while not server_start:
        time.sleep(0.1)

    run_session = False
    # thread.join()
    log.show(
        'WebSocket Server',
        log.level.INFO,
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
