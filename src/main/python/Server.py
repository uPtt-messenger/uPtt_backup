
import traceback
import asyncio
import websockets
import time

PortList = [
    49165, 50730, 61512
]

# Type 1
async def handler(websocket, path):
    print(path)
    while True:
        try:
            print('準備接收')
            Msg = await websocket.recv()
        except websockets.exceptions.ConnectionClosedError:
            print('連線已經關閉')
            return
        except websockets.exceptions.ConnectionClosedOK:
            print('連線已經關閉')
            return
        print(f"< {Msg}")
        if Msg == 'close':
            return
        Response = f"Echo [{Msg}]"
        print(f"> {Response}")

        await websocket.send(Response)

# type 2
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

# @asyncio.coroutine
# async def handler(websocket, path):
#     consumer_task = asyncio.ensure_future(
#         receiver_handler(websocket, path)
#     )
#     producer_task = asyncio.ensure_future(
#         producer_handler(websocket, path)
#     )
#     _, pending = await asyncio.wait(
#         [consumer_task, producer_task],
#         return_when=asyncio.FIRST_COMPLETED,
#     )
#     for task in pending:
#         task.cancel()
    
#     print('Finish')

# Type 3
# connected = set()

# async def handler(websocket, path):
#     # Register.
#     connected.add(websocket)
#     try:
#         # Implement logic here.
#         # await asyncio.wait([ws.send("Hello!") for ws in connected])

#         print(path)
#         while True:
#             try:
#                 print('準備接收')
#                 Msg = await websocket.recv()
#             except websockets.exceptions.ConnectionClosedError:
#                 print('連線已經關閉')
#                 return
#             except websockets.exceptions.ConnectionClosedOK:
#                 print('連線已經關閉')
#                 return
#             print(f"< {Msg}")
#             if Msg == 'close':
#                 return
#             Response = f"Echo [{Msg}]"
#             print(f"> {Response}")
#     finally:
#         # Unregister.
#         connected.remove(websocket)

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
