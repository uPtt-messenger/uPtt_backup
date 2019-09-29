
import time
import threading
import traceback

from PyQt5 import QtCore

from PTTLibrary import PTT
import Notification
import Menu
import Log
import ChatWindow
import i18n


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
        self.WaterballRecvMsgFuncList = dict()
        self.DialogList = dict()
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

    def registerWaterball(self, Dialog, RecvMsgFunc, Target):

        if Target not in self.DialogList:
            self.DialogList[Target] = Dialog
        if Target not in self.WaterballRecvMsgFuncList:
            self.WaterballRecvMsgFuncList[Target] = RecvMsgFunc

    def _CatchWaterBall(self, WaterBall):

        Target = WaterBall.getTarget()
        RecviveWaterballFrom = i18n.RecviveWaterballFrom
        RecviveWaterballFrom = i18n.replace(RecviveWaterballFrom, Target)

        print(RecviveWaterballFrom)

        def TopUI():
            Log.showValue(
                'uPTT Core',
                Log.Level.INFO,
                '啟動視窗',
                Target
            )

            if self.DialogList[Target].isMinimized():
                self.DialogList[Target].showNormal()
            # self.DialogList[Target].activateWindow()

        Dialog = None
        if Target not in self.WaterballRecvMsgFuncList:
            Dialog = ChatWindow.start(
                self._SysTray,
                self._ConfigObj,
                self,
                Target=Target
            )
        Func = self.WaterballRecvMsgFuncList[Target]
        # 112 KeyError
        Func(WaterBall)

        if Dialog is not None:
            Dialog.exec()
            del self.WaterballRecvMsgFuncList[Target]
        else:
            self._Notification.throw('uPTT', RecviveWaterballFrom, Click=TopUI)
            self.DialogList[Target].activateWindow()

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
                    self._Notification.throw('uPTT', i18n.ReLoginFail)
                else:
                    self._Notification.throw('uPTT', i18n.LoginFail)
                self._PTTBot = None
                self._LoginStatus = False
                self._MenuObj.setMenu(Menu.Type.Login)
                return
            except PTT.Exceptions.ConnectionClosed:
                self._PTTBot.log('登入失敗')
                if Recover:
                    self._Notification.throw('uPTT', i18n.ReLoginFail)
                else:
                    self._Notification.throw('uPTT', i18n.LoginFail)
                self._PTTBot = None
                self._LoginStatus = False
                self._MenuObj.setMenu(Menu.Type.Login)
                return

            self._MenuObj.setMenu(Menu.Type.Logout)
            self._PTTBot.setCallStatus(PTT.CallStatus.Off)

            if self.First:
                self.First = False

                try:
                    self._CurrentUser = self._PTTBot.getUser(
                        self._ID
                    )
                except PTT.Exceptions.NoSuchUser:
                    NoSuchUser = i18n.NoSuchUser
                    NoSuchUser = i18n.replace(NoSuchUser, self._ID)
                    self._ErrorMsg = NoSuchUser

                NickName = self._CurrentUser.getID()
                NickName = NickName[NickName.find('(') + 1:]
                NickName = NickName[:NickName.rfind(')')]

                Welcome = i18n.Welcome
                Welcome = i18n.replace(Welcome, NickName)
                self._Notification.throw('uPTT', Welcome)
            else:
                if Recover:
                    self._PTTBot.log('重新登入成功')
                    self._Notification.throw('uPTT', i18n.ReLoginSuccess)
                else:
                    self._PTTBot.log('登入成功')
                    self._Notification.throw('uPTT', i18n.LoginSuccess)

            Recover = False
            self._LoginStatus = True

            ShowNewMail = False
            try:
                while True:

                    # 以下是整個操作批踢踢的邏輯
                    StartTime = EndTime = time.time()
                    while EndTime - StartTime < self._ConfigObj.QueryCycle:
                        # 在這個 While 裡面是整個優先操作區跟等待區
                        # 一邊等待下一次倫巡比較不需要即時反應時間的功能
                        # 但是如果有需要即時回應的 API 操作，這裡依舊可以快速反應
                        #
                        # 原則上只要出現在選單又需要操作批踢踢的功能
                        # 就會出現在優先操作區
                        if not self._ThreadRun:
                            # 當使用者點了登出，就馬上給我登出!
                            Log.log(
                                'uPTT Core',
                                Log.Level.INFO,
                                i18n.Logout
                            )
                            self._MenuObj.setMenu(Menu.Type.Login)
                            self._PTTBot.logout()
                            self._PTTBot = None
                            break

                        if self._getUser:
                            # 當使用者需要查詢使用者，就馬上給我查!!!
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
                                NoSuchUser = i18n.NoSuchUser
                                NoSuchUser = i18n.replace(
                                    NoSuchUser,
                                    self._UserName
                                )
                                self._ErrorMsg = NoSuchUser

                            self._getUser = False

                        if self._throwWaterBall:
                            # 當使用者需要丟水球，就馬上給我丟!!!
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
                                NoSuchUser = i18n.NoSuchUser
                                NoSuchUser = i18n.replace(
                                    NoSuchUser,
                                    self._UserName
                                )
                                self._ErrorMsg = NoSuchUser
                            except PTT.Exceptions.UserOffline:
                                UserOffline = i18n.UserOffline
                                UserOffline = i18n.replace(
                                    UserOffline,
                                    self._UserName
                                )
                                self._ErrorMsg = UserOffline

                            self._throwWaterBall = False

                        time.sleep(0.1)
                        EndTime = time.time()
                    # 優先操作區結束

                    if self._PTTBot is None:
                        break

                    # 以下是慢速輪巡區，會每 self._ConfigObj.QueryCycle 秒檢查一次
                    if self._PTTBot.hasNewMail():
                        # 有沒有新信
                        if not ShowNewMail:
                            Log.log(
                                'uPTT Core',
                                Log.Level.INFO,
                                '你有新信件'
                            )
                            # self._Notification 是用來丟出系統通知的
                            # self._SysTray.setToolTip 是設定滑鼠移到系統列圖示上的時候顯示的文字
                            self._Notification.throw('uPTT', i18n.HaveNewMail)
                            self._SysTray.setToolTip(
                                f'uPTT - {i18n.HaveNewMail}'
                            )
                        ShowNewMail = True
                    else:
                        self._SysTray.setToolTip(f'uPTT - {i18n.HaveNoMail}')
                        ShowNewMail = False

                    # 有沒有新水球丟過來，每 self._ConfigObj.QueryCycle 秒檢查一次
                    WaterballRecvMsgFuncList = self._PTTBot.getWaterBall(
                        PTT.WaterBallOperateType.Clear
                    )
                    if WaterballRecvMsgFuncList is not None:
                        for WaterBall in WaterballRecvMsgFuncList:

                            if WaterBall.getType() != PTT.WaterBallType.Catch:
                                continue
                            else:
                                Target = WaterBall.getTarget()
                                Content = WaterBall.getContent()
                                print(f'來自 {Target} 的水球 [{Content}]')

                            print('=' * 30)

                            self.Waterball_Signal.emit(
                                WaterBall
                            )

                    # 慢速輪巡區結束
            except Exception as e:

                traceback.print_tb(e.__traceback__)
                print(e)
                Recover = True
                # for s in range(self._ConfigObj.RecoverTime):
                #     Log.showValue(
                #         'uPTT Core',
                #         Log.Level.INFO,
                #         '等待恢復機制',
                #         self._ConfigObj.RecoverTime - s
                #     )
                #     time.sleep(1)

                Log.log(
                    'uPTT Core',
                    Log.Level.INFO,
                    '啟動恢復機制'
                )

            if self._PTTBot is not None:
                self._PTTBot.logout()
                self._PTTBot = None
        self._Notification.throw('uPTT', i18n.LogoutSuccess)
