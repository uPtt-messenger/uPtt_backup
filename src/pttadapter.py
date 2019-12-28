import time
import threading
import traceback

from PTTLibrary import PTT

import log
import command
from errorcode import ErrorCode
from msg import Msg


class PTTAdapter:
    def __init__(self, config, command):
        self.Config = config
        self.Command = command

        Thread = threading.Thread(
            target=self.run,
            daemon=True
        )
        Thread.start()

    def run(self):

        log.show(
            'PTTAdapter',
            log.Level.INFO,
            '啟動'
        )
        self.bot = PTT.Library()

        while True:

            StartTime = EndTime = time.time()
            while EndTime - StartTime < self.Config.QueryCycle:

                ID, Password = self.Command.recvlogin()
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
                    self.Command.push(ResMsg)

                if self.Command.recvlogout():

                    log.show(
                        'PTTAdapter',
                        log.Level.INFO,
                        '執行登出'
                    )

                    self.bot.logout()
                    ResMsg = Msg(
                        ErrorCode.Success,
                        '登出成功'
                    )
                    self.Command.push(ResMsg)

                time.sleep(0.05)
                EndTime = time.time()
