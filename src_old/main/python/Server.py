
import traceback
import asyncio
import websockets
import time
import sys
import json
import subprocess
import threading

import Log


PortList = [
    49165, 50730, 61512
]

OnlineServerPortList = [
    59277
    # , 56885, 62750
]

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


async def CountOnline_JoinFunc(port):
    url = f"ws://104.154.219.183:{port}"
    print(f'更新線上人數:{url}')
    async with websockets.connect(url) as websocket:
        process = subprocess.Popen(
            'wmic csproduct get uuid'.split(' '),
            stdout=subprocess.PIPE
        )
        out, err = process.communicate()
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


def CountOnline_Join():
    global OnlineServerPortList
    for port in OnlineServerPortList:
        try:
            asyncio.get_event_loop().run_until_complete(
                CountOnline_JoinFunc(port)
            )

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
                '線上人數更新錯誤'
            )
    Log.log(
        'Server',
        Log.Level.INFO,
        '線上人數更新結束'
    )
    # 每 25 分鐘更新一次
    timer = threading.Timer(25 * 60, CountOnline_Join)
    timer.daemon = True
    timer.start()


async def CountOnline_LeaveFunc(port):
    url = f"ws://104.154.219.183:{port}"
    print(f'更新線上人數:{url}')
    async with websockets.connect(url) as websocket:
        process = subprocess.Popen(
            'wmic csproduct get uuid'.split(' '),
            stdout=subprocess.PIPE
        )
        out, err = process.communicate()
        MachineID = out.decode("cp950")
        MachineID = MachineID[4:].strip()
        Log.showValue(
            'Server',
            Log.Level.INFO,
            'MachineID',
            MachineID
        )
        Msg = dict()
        Msg['purpose'] = 'CountOnline_Leave'
        Msg['uid'] = MachineID
        MsgStr = json.dumps(Msg)
        await websocket.send(MsgStr)


def CountOnline_Leave():
    global OnlineServerPortList
    for port in OnlineServerPortList:
        try:
            asyncio.get_event_loop().run_until_complete(
                CountOnline_LeaveFunc(port)
            )

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
                '線上人數更新錯誤'
            )
    Log.log(
        'Server',
        Log.Level.INFO,
        '線上人數更新結束'
    )

if __name__ == '__main__':
    # https://websockets.readthedocs.io/en/stable/intro.html
    # for i in range(len(PortList)):
    #     try:
    #         start_server = websockets.serve(handler, "127.0.0.1", PortList[i])
    #         print(f'WebSocket Server 啟動成功 Port: {PortList[i]}')
    #         break
    #     except Exception as e:
    #         traceback.print_tb(e.__traceback__)
    #         print(e)
    #         print(f'WebSocket Server 啟動失敗 Port: {PortList[i]}')

    # print('OKOK')
    # asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()

    CountOnline_Join()
    CountOnline_Leave()