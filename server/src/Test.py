import asyncio
import websockets
import pathlib
import ssl
import logging
import json

import traceback
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


async def getPushMsg():
    await asyncio.sleep(5)
    return 'Push Msg'


PushMsg = None
Run = True


async def consumer_handler(ws, path):
    global Run
    try:
        RecvMsg = await ws.recv()
        print(f'recv [{RecvMsg}]')
        await ws.send(RecvMsg)
        print(f'echo complete')
    except Exception as e:
        print('Connection Clsoe')
        Run = False


async def producer_handler(ws, path):
    global PushMsg
    while True:
        if PushMsg is not None:
            print(f'push [{PushMsg}]')
            await ws.send(PushMsg)
            PushMsg = None
        else:
            # print(f'asyncio.sleep')
            # No
            await asyncio.sleep(2)


async def handler(websocket, path):
    global Run

    Run = True

    while Run:
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


# async def handler(websocket, path):
#     print(f'{path} join')
#     try:
#         while True:
#             RecvMsg = await websocket.recv()
#             PushMsg = await getPushMsg()

#             if RecvMsg is not None:
#                 await websocket.send(RecvMsg)
#             else:
#                 await websocket.send(PushMsg)

#             PushMsg = None
#             RecvMsg = None

#     finally:
#         print(f'{path} leave')


# threading.Thread(target=testNewMsg).start()

# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# localhost_pem = "../GenerateCACert/uPttSSL.pem"
# ssl_context.load_cert_chain(localhost_pem)

if __name__ == '__main__':
    # start_server = websockets.serve(
    #     handler,
    #     "localhost",
    #     50733,
    #     # ssl=ssl_context
    # )

    # asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()

    from http.server import HTTPServer, BaseHTTPRequestHandler

    index = '''
<!DOCTYPE html>
<html lang="tw">
    <head>
        <title></title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script>
        function oAuth2() {
            var URL = 'https://notify-bot.line.me/oauth/authorize?';
            URL += 'response_type=code';
            URL += '&client_id=[olcVc4l7mHNHSxij1NYMQt]';
            URL += '&redirect_uri=[http://localhost:57983/index.html]';
            URL += '&scope=notify';
            URL += '&state=NO_STATE';
            window.location.href = URL;
        }
    </script>
    </head>
    <body>
        <button onclick="oAuth2();"> 連結到 LineNotify 按鈕 </button>
    </body>
</html>
'''

    data = {'result': index}


    class Resquest(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(index.encode())


    def run(server_class=HTTPServer, handler_class=Resquest):
        server_address = ('', 57983)
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()


    run()
