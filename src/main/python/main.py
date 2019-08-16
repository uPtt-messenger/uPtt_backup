# https://www.learnpyqt.com/courses/adanced-ui-features/system-tray-mac-menu-bar-applications-pyqt/
import sys
import os
import time
import threading
import json
import traceback

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import PTTLibrary
from PTTLibrary import PTT

import Config
import About
import Login
import Notification
import NewMail

LoginStatus = False
PTTBot = None
SystemTray = None


def checkMailFunc(ID, PW):
    global PTTBot
    global ThreadRun
    global LoginStatus
    global SystemTray

    Recover = False
    while ThreadRun:

        PTTBot = PTT.Library()
        try:
            PTTBot.login(ID, PW)
        except PTT.Exceptions.LoginError:
            PTTBot.log('登入失敗')
            if Recover:
                Notification.throw(SystemTray, 'PTT Postman', '重新登入失敗')
            else:
                Notification.throw(SystemTray, 'PTT Postman', '登入失敗')
            PTTBot = None
            LoginStatus = False
            return

        if Recover:
            PTTBot.log('重新登入成功')
            Notification.throw(SystemTray, 'PTT Postman', '重新登入成功')
        else:
            PTTBot.log('登入成功')
            Notification.throw(SystemTray, 'PTT Postman', '登入成功')

        Recover = False
        LoginStatus = True
        genMenu()

        ShowNewMail = False
        try:
            while ThreadRun:
                if PTTBot is None:
                    break
                if PTTBot.hasNewMail():
                    if not ShowNewMail:
                        print('收到新信!!')
                        Notification.throw(SystemTray, 'PTT Postman', '你有新信件')
                        SystemTray.setToolTip('PTT Postman - 你有新信件')
                    ShowNewMail = True
                else:
                    SystemTray.setToolTip('PTT Postman - 無新信件')
                    ShowNewMail = False
                time.sleep(2)
            PTTBot.logout()
        except:
            Recover = True
            for s in range(5):
                print(f'發生錯誤! {5 - s} 秒後啟動恢復機制')
                time.sleep(1)

        PTTBot = None
    Notification.throw(SystemTray, 'PTT Postman', '登出成功')


def LoginFunc():
    global LoginStatus
    global PTTBot
    global ThreadRun
    global SystemTray
    global ConfigObj

    LoginStatus = False

    ID, PW, SaveID = Login.start(ConfigObj)

    if ID is None or PW is None:
        Notification.throw(SystemTray, 'PTT Postman', '登入取消')
        return

    if len(ID) < 3 or len(PW) == 0:
        Notification.throw(SystemTray, 'PTT Postman', '登入取消')
        return
    if SaveID:
        ConfigObj.setValue(Config.Key_ID, ID)
    else:
        ConfigObj.setValue(Config.Key_ID, None)

    print('ID: ' + ID)
    print('PW: ' + PW)

    ThreadRun = True

    t = threading.Thread(target=checkMailFunc, args=(ID, PW))
    t.start()


def LogoutFunc():
    global LoginStatus
    global PTTBot
    global ThreadRun

    LoginStatus = False
    ThreadRun = False

    while PTTBot is not None:
        time.sleep(0.2)

    genMenu()


def AboutFunc():

    About.start()


def ExitFunc():

    global SystemTray

    LogoutFunc()
    SystemTray.hide()
    print('Exit')
    sys.exit()

if __name__ == '__main__':
    Appctxt = ApplicationContext()

    ConfigObj = Config.Config(Appctxt)

    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    icon = QIcon(Config.SmallImage)

    SystemTray = QSystemTrayIcon(app)
    SystemTray.setIcon(icon)
    SystemTray.setVisible(True)
    SystemTray.setToolTip('PTT Postman')

    LoginFunc()

    exit_code = Appctxt.app.exec_()
    sys.exit(exit_code)
