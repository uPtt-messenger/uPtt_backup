
import time

import PTTLibrary
from PTTLibrary import PTT

import Notification


class Core(object):
    def __init__(self, SystemTray, ID, PW):
        self._SysTray = SystemTray
        self._Notification = Notification.Notification(self._SysTray)

        self._ID = ID
        self._PW = PW

        self._ThreadRun = True

        self._PTTBot = PTT.Library()

    def TrackThread(self):
        Recover = False
        while self._ThreadRun:

            try:
                self._PTTBot.login(self._ID, self._PW)
            except PTT.Exceptions.LoginError:
                self._PTTBot.log('登入失敗')
                if Recover:
                    self._Notification.throw('PTT Postman', '重新登入失敗')
                else:
                    self._Notification.throw('PTT Postman', '登入失敗')
                self._PTTBot = None
                LoginStatus = False
                return

            if Recover:
                self._PTTBot.log('重新登入成功')
                self._Notification.throw('PTT Postman', '重新登入成功')
            else:
                self._PTTBot.log('登入成功')
                self._Notification.throw('PTT Postman', '登入成功')

            Recover = False
            LoginStatus = True

            ShowNewMail = False
            try:
                while self._ThreadRun:
                    if self._PTTBot is None:
                        break
                    if self._PTTBot.hasNewMail():
                        if not ShowNewMail:
                            print('收到新信!!')
                            self._Notification.throw('PTT Postman', '你有新信件')
                            self._SysTray.setToolTip('PTT Postman - 你有新信件')
                        ShowNewMail = True
                    else:
                        self._SysTray.setToolTip('PTT Postman - 無新信件')
                        ShowNewMail = False
                    time.sleep(2)
                self._PTTBot.logout()
            except:
                Recover = True
                for s in range(5):
                    print(f'發生錯誤! {5 - s} 秒後啟動恢復機制')
                    time.sleep(1)

            self._PTTBot = None
        self._Notification.throw('PTT Postman', '登出成功')
