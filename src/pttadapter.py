import time
import threading
import traceback

from PTTLibrary import PTT

import log
import command
from errorcode import ErrorCode
from msg import Msg
from dialogue import Dialogue


class PTTAdapter:
    def __init__(self, config, command):
        self.config = config
        self.command = command

        self.RunServer = True
        self.login = False
        self.dialog = Dialogue()

        self.thread = threading.Thread(
            target=self.run,
            daemon=True
        )
        self.thread.start()

    def logout(self):
        log.show(
            'PTTAdapter',
            log.Level.INFO,
            '執行登出'
        )

        self.bot.logout()

    def stop(self):
        log.show(
            'PTTAdapter',
            log.Level.INFO,
            '執行終止程序'
        )
        # self.logout()
        self.RunServer = False
        self.thread.join()
        log.show(
            'PTTAdapter',
            log.Level.INFO,
            '終止程序完成'
        )

    def run(self):

        log.show(
            'PTTAdapter',
            log.Level.INFO,
            '啟動'
        )

        self.bot = PTT.Library(
            LogHandler=self.config.PttLogHandler,
            LogLevel=self.config.PttLogLevel
        )

        while self.RunServer:

            # 快速反應區
            StartTime = EndTime = time.time()
            while EndTime - StartTime < self.config.QueryCycle:

                ID, Password = self.command.recvlogin()
                if (ID, Password) != (None, None):
                    log.show(
                        'PTTAdapter',
                        log.Level.INFO,
                        '執行登入'
                    )
                    try:
                        self.bot.login(
                            ID,
                            Password,
                            KickOtherLogin=True
                        )
                        self.login = True
                        self.bot.setCallStatus(PTT.CallStatus.Off)

                        ResMsg = Msg(
                            ErrorCode.Success,
                            '登入成功'
                        )

                    except PTT.Exceptions.LoginError:
                        ResMsg = Msg(
                            ErrorCode.LoginFail,
                            '登入失敗'
                        )
                    except PTT.Exceptions.WrongIDorPassword:
                        ResMsg = Msg(
                            ErrorCode.LoginFail,
                            '帳號密碼錯誤'
                        )
                    except PTT.Exceptions.LoginTooOften:
                        ResMsg = Msg(
                            ErrorCode.LoginFail,
                            '請稍等一下再登入'
                        )
                    self.command.push(ResMsg)

                if self.command.recvlogout():
                    self.login = False
                    self.logout()

                    ResMsg = Msg(
                        ErrorCode.Success,
                        '登出成功'
                    )

                    self.command.push(ResMsg)

                SendID, SendContent = self.command.sendWaterBall()
                if (SendID, SendContent) != (None, None):

                    try:
                        self.bot.throwWaterBall(SendID, SendContent)
                        self.dialog.send(SendID, SendContent)

                        ResMsg = Msg(
                            ErrorCode.Success,
                            '丟水球成功'
                        )
                    except PTT.Exceptions.NoSuchUser:
                        ResMsg = Msg(
                            ErrorCode.NoSuchUser,
                            '無此使用者'
                        )
                    except PTT.Exceptions.UserOffline:
                        ResMsg = Msg(
                            ErrorCode.UserOffLine,
                            '使用者離線'
                        )
                    self.command.push(ResMsg)

                time.sleep(0.05)
                EndTime = time.time()

            # 慢速輪巡區
            log.show(
                'PTTAdapter',
                log.Level.INFO,
                '慢速輪巡'
            )

            if not self.login:
                continue
            WaterBallList = self.bot.getWaterBall(
                PTT.WaterBallOperateType.Clear
            )

            if WaterBallList is not None:
                for WaterBall in WaterBallList:
                    if not WaterBall.getType() == PTT.WaterBallType.Catch:
                        continue

                    Target = WaterBall.getTarget()
                    Content = WaterBall.getContent()
                    Date = WaterBall.getDate()

                    log.showvalue(
                        'PTTAdapter',
                        log.Level.INFO,
                        f'收到來自 {Target} 的水球',
                        f'[{Content}][{Date}]'
                    )

                    # print(f'收到來自 {Target} 的水球 [{Content}][{Date}]')

                    payload = Msg()
                    payload.add(Msg.Key_PttID, Target)
                    payload.add(Msg.Key_Content, Content)
                    payload.add(Msg.Key_Date, Date)

                    PushMsg = Msg(opt='recvwaterball')
                    PushMsg.add(Msg.Key_Payload, payload)

                    self.dialog.recv(Target, Content, Date)

                    self.command.push(PushMsg)

        self.logout()
