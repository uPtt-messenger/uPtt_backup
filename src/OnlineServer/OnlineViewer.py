
import traceback
import asyncio
import websockets
import time
import json
import threading
import Log

OnlineServerPortList = [
    59277
]


async def UpdateFunc():
    url = f"ws://104.154.219.183:{59277}"
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
    global OnlineServerPortList
    for port in OnlineServerPortList:
        try:
            asyncio.get_event_loop().run_until_complete(
                UpdateFunc()
            )

            # Log.log(
            #     'Server',
            #     Log.Level.INFO,
            #     '線上人數取得成功'
            # )
            break
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            Log.log(
                'Server',
                Log.Level.INFO,
                '線上人數取得錯誤'
            )
    # Log.log(
    #     'Server',
    #     Log.Level.INFO,
    #     '線上人數取得結束'
    # )

while True:
    Update()
    time.sleep(10)