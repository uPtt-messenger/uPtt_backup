
import traceback
import asyncio
import websockets
import time
import json
import threading
import Log

PortList = [
    59277
]


class Console:
    def __init__(self):
        self._Lock = threading.Lock()
        self._OnlineList = dict()

        self._MaxLiveTime = 30 * 60
        self._RecycleTime = 10 * 60

        self._Key_MaxOnline = 'MaxOnline'

        try:
            with open('Data.txt', encoding='utf8') as File:
                self._Data = json.load(File)
        except Exception as e:

            traceback.print_tb(e.__traceback__)
            print(e)
            print('無法讀取 Data.txt')
            self._Data = dict()
            self._Data[self._Key_MaxOnline] = 0

        RecycleT = threading.Thread(target=self._recycle)
        RecycleT.daemon = True
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

    def getOnline(self):
        self._Lock.acquire()
        try:
            Online = len(self._OnlineList)
            MaxOnline = self._Data[self._Key_MaxOnline]
        finally:
            self._Lock.release()

        return Online, MaxOnline

    def _saveData(self):
        with open('Data.txt', 'w', encoding='utf8') as File:
            json.dump(self._Data, File, indent=4, ensure_ascii=False)

    def _update(self):

        CurrentOnline = len(self._OnlineList)

        if self._Key_MaxOnline not in self._Data:
            self._Data[self._Key_MaxOnline] = 0

        if CurrentOnline > self._Data[self._Key_MaxOnline]:
            self._Data[self._Key_MaxOnline] = CurrentOnline
            self._saveData()

        Buffer = f'目前人數 [{CurrentOnline}] 最高人數[{self._Data[self._Key_MaxOnline]}]'
        Log.log(
            'OnLine Server',
            Log.Level.INFO,
            Buffer
        )

    def _recycle(self):
        while True:
            Log.log(
                'OnLine Server',
                Log.Level.INFO,
                '回收器等待'
            )
            # 每十分鐘回收一次
            time.sleep(self._RecycleTime)
            Log.log(
                'OnLine Server',
                Log.Level.INFO,
                '回收器啟動'
            )
            self._Lock.acquire()
            try:
                CurrentTime = time.time()
                RemoveKey = []
                for Key in self._OnlineList:
                    if CurrentTime - self._OnlineList[Key] >= \
                            self._MaxLiveTime:
                        RemoveKey.append(Key)

                for Key in RemoveKey:
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
        elif Purpose == 'CountOnline':
            Online, MaxOnline = ConsoleObj.getOnline()

            ResMsg = dict()
            ResMsg['state'] = '0'
            ResMsg['Online'] = str(Online)
            ResMsg['MaxOnline'] = str(MaxOnline)

            ResMsgStr = json.dumps(ResMsg)
            await websocket.send(ResMsgStr)

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
