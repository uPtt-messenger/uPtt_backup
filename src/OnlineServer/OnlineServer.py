
import traceback
import asyncio
import websockets
import time
import json
import threading
import Log

PortList = [
    59277, 56885, 62750
]


class Console:
    def __init__(self):
        self._Lock = threading.Lock()
        self._OnlineList = dict()

        self._MaxLiveTime = 30 * 60

        RecycleT = threading.Thread(target=self._recycle)
        RecycleT.start()

    def add(self, UID):

        self._Lock.acquire()
        try:
            self._OnlineList[UID] = time.time()
        finally:
            self._update()
            self._Lock.release()

    def remove(self, UID):

        self._Lock.acquire()
        try:
            if UID in self._OnlineList:
                del self._OnlineList[UID]
        finally:
            self._update()
            self._Lock.release()

    def _update(self):
        Log.showValue(
            'OnLine Server',
            Log.Level.INFO,
            '目前人數',
            len(self._OnlineList)
        )

    def _recycle(self):
        while True:
            Log.log(
                'OnLine Server',
                Log.Level.INFO,
                '回收器等待'
            )
            # 每十分鐘回收一次
            time.sleep(10 * 60)
            Log.log(
                'OnLine Server',
                Log.Level.INFO,
                '回收器啟動'
            )
            self._Lock.acquire()
            try:
                CurrentTime = time.time()
                for Key in self._OnlineList:
                    if CurrentTime - self._OnlineList[Key] >= \
                            self._MaxLiveTime:
                        del self._OnlineList[Key]
            finally:
                self._update()
                self._Lock.release()


# {"purpose": "CountOnline_Join", "uid": "QQQ_UID"}
# {"purpose": "CountOnline_Leave", "uid": "QQQ_UID"}


async def handler(websocket, path):
    global ConsoleObj
    while True:
        try:
            MsgStr = await websocket.recv()
        except websockets.exceptions.ConnectionClosedError:
            return
        except websockets.exceptions.ConnectionClosedOK:
            return
        
        Msg = json.loads(MsgStr)
        Purpose = Msg['purpose']

        if Purpose == 'CountOnline_Join':
            UID = Msg['uid']
            print(f'UID [{UID}]')
            ConsoleObj.add(UID)
        elif Purpose == 'CountOnline_Leave':
            UID = Msg['uid']
            print(f'UID [{UID}]')
            ConsoleObj.remove(UID)

for i in range(len(PortList)):
    try:
        start_server = websockets.serve(handler, "0.0.0.0", PortList[i])
        Log.showValue(
            'OnLine Server',
            Log.Level.INFO,
            'WebSocket Server 啟動成功',
            PortList[i]
        )
        break
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(e)
        Log.showValue(
            'OnLine Server',
            Log.Level.INFO,
            'WebSocket Server 啟動失敗',
            PortList[i]
        )

ConsoleObj = Console()

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
