
import traceback
import asyncio
import websockets
import time
import json
import threading
import Log


IP = '104.154.219.183:59277'
# IP = '127.0.0.1:59277'

async def UpdateFunc():
    global IP
    url = f"ws://{IP}"
    # print(f'取得線上人數:{url}')
    async with websockets.connect(url) as websocket:
        Msg = dict()
        Msg['purpose'] = 'CountOnline'
        MsgStr = json.dumps(Msg)
        await websocket.send(MsgStr)
        ReceMsg = await websocket.recv()
        # print(ReceMsg)
        ReceMsg = json.loads(ReceMsg)
        Online = ReceMsg['Online']
        MaxOnline = ReceMsg['MaxOnline']
        Buffer = f'線上人數 [{Online}] 最高人數 [{MaxOnline}]'
        Log.log(
            'Online Viewer',
            Log.Level.INFO,
            Buffer
        )


def Update():
    try:
        asyncio.get_event_loop().run_until_complete(
            UpdateFunc()
        )
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(e)
        Log.log(
            'Online Viewer',
            Log.Level.INFO,
            '線上人數取得錯誤'
        )

while True:
    Update()
    time.sleep(1)