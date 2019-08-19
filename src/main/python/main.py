# https://www.learnpyqt.com/courses/adanced-ui-features/system-tray-mac-menu-bar-applications-pyqt/
import sys
import os
import time
import threading
import json
import traceback

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtGui
from PyQt5 import QtWidgets


import PTTLibrary
from PTTLibrary import PTT

import Config
import About
import Login
import Notification
import NewMail
import Menu


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

    global MenuObj

    ID, PW, SaveID = Login.start(ConfigObj)

    if ID is None or PW is None:
        NotificationObj.throw('PTT Postman', '登入取消')
        MenuObj.setMenu(Menu.Type.Login)
        return True
    if len(ID) < 3 or len(PW) == 0:
        NotificationObj.throw('PTT Postman', '登入取消')
        MenuObj.setMenu(Menu.Type.Login)
        return True

    if SaveID:
        ConfigObj.setValue(ConfigObj.Key_ID, ID)
    else:
        ConfigObj.setValue(ConfigObj.Key_ID, None)

    print('ID: ' + ID)
    print('PW: ' + PW)

    # t = threading.Thread(target=checkMailFunc, args=(ID, PW))
    # t.start()

    return True


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
    About.start(ConfigObj)

    return True


def ExitFunc():

    SystemTray.hide()
    print('Exit')
    sys.exit()


if __name__ == '__main__':
    Appctxt = ApplicationContext()
    ConfigObj = Config.Config(Appctxt)

    app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)

    SystemTray = QtWidgets.QSystemTrayIcon(app)
    SystemTray.setIcon(ConfigObj.Icon_SmallImage)
    SystemTray.setVisible(True)
    SystemTray.setToolTip('uPTT')

    NotificationObj = Notification.Notification(SystemTray, ConfigObj)
    MenuObj = Menu.Menu(SystemTray)
    MenuObj.addEvent(Menu.Type.Login, LoginFunc)
    MenuObj.addEvent(Menu.Type.About, AboutFunc)
    MenuObj.addEvent(Menu.Type.Exit, ExitFunc)

    LoginFunc()

    exit_code = Appctxt.app.exec_()
    sys.exit(Appctxt.app.exec_())
