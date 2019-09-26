
import time
import threading
import traceback

# from PyQt5.QtCore import QThread
from PyQt5 import QtCore

from PTTLibrary import PTT
import Notification
import Menu
import Log
import ChatWindow


class Core(QtCore.QThread):
    Waterball_Signal = QtCore.pyqtSignal(PTT.DataType.WaterBallInfo)

    def __init__(
        self,
        SystemTray,
        ConfigObj,
        MenuObj,
        ID,
        PW
    ):
        super(Core, self).__init__(None)

        self._SysTray = SystemTray
        self._Notification = Notification.Notification(
            SystemTray,
            ConfigObj
        )
        self._ConfigObj = ConfigObj
        self._MenuObj = MenuObj

        self._ID = ID
        self._PW = PW

        self._ThreadRun = True
        self._LoginStatus = False

        self._getUser = False
        self._throwWaterBall = False

        self.Waterball_Signal.connect(self._CatchWaterBall)
        self.WaterballList = dict()
        self.First = True

    def start(self):
        Thread = threading.Thread(
            target=self.TrackThread,
            daemon=True
        )
        Thread.start()

    def stop(self):
        self._ThreadRun = False

    def isStop(self):
        return self._PTTBot is None

    def getUser(self, Name):

        self._result = None
        self._UserName = Name

        self._ErrorMsg = None
        self._getUser = True

        while self._getUser:
            time.sleep(0.1)

        return self._ErrorMsg, self._result

    def throwWaterBall(self, Target, Content):

        self._Target = Target
        self._Content = Content

        self._ErrorMsg = None
        self._throwWaterBall = True

        while self._throwWaterBall:
            time.sleep(0.1)

        return self._ErrorMsg

    def registerWaterballList(self, Target, Func):

        if Target not in self.WaterballList:
            self.WaterballList[Target] = Func

    def _CatchWaterBall(self, WaterBall):
        Target = WaterBall.getTarget()

        print(f'收到水球 [{WaterBall.getContent()}]')

        self._Notification.throw('uPTT', '收到來自 {Target} 的水球')

        Dialog = None
        if Target not in self.WaterballList:
            Dialog = ChatWindow.start(
                self._SysTray,
                self._ConfigObj,
                self,
                Target=Target
            )
        Func = self.WaterballList[Target]
        Func(WaterBall)

        if Dialog is not None:
            Dialog.exec()
            del self.WaterballList[Target]

    def TrackThread(self):
        Recover = False
        while self._ThreadRun:

            self._PTTBot = PTT.Library()
            try:
                self._PTTBot.login(
                    self._ID,
                    self._PW,
                    KickOtherLogin=True
                )
            except PTT.Exceptions.LoginError:
                self._PTTBot.log('登入失敗')
                if Recover:
                    self._Notification.throw('uPTT', '重新登入失敗')
                else:
                    self._Notification.throw('uPTT', '登入失敗')
                self._PTTBot = None
                self._LoginStatus = False
                self._MenuObj.setMenu(Menu.Type.Login)
                return

            self._MenuObj.setMenu(Menu.Type.Logout)

            if Recover:
                self._PTTBot.log('重新登入成功')
                self._Notification.throw('uPTT', '重新登入成功')
            else:
                self._PTTBot.log('登入成功')
                self._Notification.throw('uPTT', '登入成功')

            if self.First:
                self.First = False

                try:
                    self._CurrentUser = self._PTTBot.getUser(
                        self._ID
                    )
                except PTT.Exceptions.NoSuchUser:
                    self._ErrorMsg = f'無此使用者: {self._ID}'

                NickName = self._CurrentUser.getID()
                NickName = NickName[NickName.find('(') + 1:]
                NickName = NickName[:NickName.rfind(')')]

                self._Notification.throw('uPTT', f'{NickName}! 歡迎您!')

            Recover = False
            self._LoginStatus = True

            ShowNewMail = False
            try:
                while True:

                    # Log.log(
                    #     'uPTT Core',
                    #     Log.Level.INFO,
                    #     '進入等待區'
                    # )
                    StartTime = EndTime = time.time()
                    while EndTime - StartTime < self._ConfigObj.QueryCycle:
                        # 優先操作層
                        if not self._ThreadRun:
                            Log.log(
                                'uPTT Core',
                                Log.Level.INFO,
                                '登出'
                            )
                            self._MenuObj.setMenu(Menu.Type.Login)
                            self._PTTBot.logout()
                            self._PTTBot = None
                            break

                        if self._getUser:
                            Log.showValue(
                                'uPTT Core',
                                Log.Level.INFO,
                                '查詢使用者',
                                self._UserName
                            )
                            try:
                                self._result = self._PTTBot.getUser(
                                    self._UserName
                                )
                            except PTT.Exceptions.NoSuchUser:
                                self._ErrorMsg = f'無此使用者: {self._UserName}'

                            self._getUser = False

                        if self._throwWaterBall:
                            Log.showValue(
                                'uPTT Core',
                                Log.Level.INFO,
                                '丟水球給',
                                self._Target
                            )
                            Log.showValue(
                                'uPTT Core',
                                Log.Level.INFO,
                                '水球內容',
                                self._Content
                            )

                            try:
                                self._PTTBot.throwWaterBall(
                                    self._Target,
                                    self._Content
                                )
                                self._PTTBot.setCallStatus(PTT.CallStatus.Off)
                            except PTT.Exceptions.NoSuchUser:
                                self._ErrorMsg = f'無此使用者: {self._UserName}'
                            except PTT.Exceptions.UserOffline:
                                self._ErrorMsg = f'使用者離線: {self._UserName}'

                            self._throwWaterBall = False

                        time.sleep(0.1)
                        EndTime = time.time()

                    # Log.log(
                    #     'uPTT Core',
                    #     Log.Level.INFO,
                    #     '等待區結束'
                    # )
                    if self._PTTBot is None:
                        break

                    if self._PTTBot.hasNewMail():
                        if not ShowNewMail:
                            Log.log(
                                'uPTT Core',
                                Log.Level.INFO,
                                '你有新信件'
                            )
                            self._Notification.throw('uPTT', '你有新信件')
                            self._SysTray.setToolTip('uPTT - 你有新信件')
                        ShowNewMail = True
                    else:
                        self._SysTray.setToolTip('uPTT - 無新信件')
                        ShowNewMail = False

                    WaterBallList = self._PTTBot.getWaterBall(
                        PTT.WaterBallOperateType.Clear
                    )

                    if WaterBallList is not None:
                        for WaterBall in WaterBallList:

                            if not WaterBall.getType() == PTT.WaterBallType.Catch:
                                continue

                            Target = WaterBall.getTarget()
                            Content = WaterBall.getContent()
                            print(f'來自 {Target} 的水球 [{Content}]')

                            print('=' * 30)

                            self.Waterball_Signal.emit(
                                WaterBall
                            )
            except Exception as e:

                traceback.print_tb(e.__traceback__)
                print(e)
                Recover = True
                for s in range(5):
                    Log.showValue(
                        'uPTT Core',
                        Log.Level.INFO,
                        '啟動恢復機制',
                        5 - s
                    )
                    time.sleep(1)

            if self._PTTBot is not None:
                self._PTTBot.logout()
                self._PTTBot = None
        self._Notification.throw('uPTT', '登出成功')
