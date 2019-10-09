
import traceback
import asyncio
import websockets
import time
import sys
import json
import subprocess

import Log


PortList = [
    49165, 50730, 61512
]
MachineID = None


async def handler(websocket, path):
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

async def CountOnline_Join(port):
    url = f"ws://localhost:{port}"
    print(f'更新線上人數:{url}')
    async with websockets.connect(url) as websocket:
        process = subprocess.Popen(
            'wmic csproduct get uuid'.split(' '),
            stdout=subprocess.PIPE
        )
        out, err = process.communicate()
        global MachineID
        MachineID = out.decode("cp950")
        MachineID = MachineID[4:].strip()
        Log.showValue(
            'Server',
            Log.Level.INFO,
            'MachineID',
            MachineID
        )
        Msg = dict()
        Msg['purpose'] = 'CountOnline_Join'
        Msg['uid'] = MachineID
        MsgStr = json.dumps(Msg)
        await websocket.send(MsgStr)


async def CountOnline_Leave(port):
    url = f"ws://localhost:{port}"
    print(f'更新線上人數:{url}')
    async with websockets.connect(url) as websocket:
        Msg = dict()
        Msg['purpose'] = 'CountOnline_Leave'
        global MachineID
        Msg['uid'] = MachineID
        MsgStr = json.dumps(Msg)
        await websocket.send(MsgStr)


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

OnlineServerPortList = [
    59277, 56885, 62750
]
for port in OnlineServerPortList:
    try:
        asyncio.get_event_loop().run_until_complete(CountOnline_Join(port))

        Log.log(
            'Server',
            Log.Level.INFO,
            '線上人數更新成功'
        )
        break
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(e)
        Log.log(
            'Server',
            Log.Level.INFO,
            'CountOnline_Join error'
        )
Log.log(
    'Server',
    Log.Level.INFO,
    '線上人數更新結束'
)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
