
import traceback
import asyncio
import websockets
import time

PortList = [
    49165, 50730, 61512
]


async def handler(websocket, path):
    print(path)
    while True:
        try:
            print('準備接收')
            Msg = await websocket.recv()
        except websockets.exceptions.ConnectionClosedError:
            print('連線已經關閉')
            return

        print(f"< {Msg}")

        Response = f"Echo [{Msg}]"
        print(f"> {Response}")

        await websocket.send(Response)
        await websocket.send(Response)

# async def receiver(message):
#     print(f'receive [{message}]')

# async def receiver_handler(websocket, path):
#     async for message in websocket:
#         await receiver(message)

# async def producer():
#     return None

# async def producer_handler(websocket, path):
#     while True:
#         message = await producer()
#         if message is not None:
#             await websocket.send(message)

# async def handler(websocket, path):
#     consumer_task = asyncio.ensure_future(
#         receiver_handler(websocket, path))
#     producer_task = asyncio.ensure_future(
#         producer_handler(websocket, path))
#     done, pending = await asyncio.wait(
#         [consumer_task, producer_task],
#         return_when=asyncio.FIRST_COMPLETED,
#     )
#     for task in pending:
#         task.cancel()

# https://websockets.readthedocs.io/en/stable/intro.html
for i in range(len(PortList)):
    try:
        start_server = websockets.serve(handler, "127.0.0.1", PortList[i])
        print(f'WebSocket Server 啟動成功 Port: {PortList[i]}')
        break
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(e)
        print(f'WebSocket Server 啟動失敗 Port: {PortList[i]}')

print('OKOK')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
