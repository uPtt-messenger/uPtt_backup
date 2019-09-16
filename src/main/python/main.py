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

import Config
import About
import Login
import Notification
import NewMail
import Menu
import ChatWindow
import PTTCore


def LoginFunc():

    global MenuObj
    global PTTCoreObj

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

    PTTCoreObj = PTTCore.Core(
        SystemTray,
        ConfigObj,
        MenuObj,
        ID,
        PW
    )

    PTTCoreObj.start()

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
    PTTCoreObj = None

    app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)

    SystemTray = QtWidgets.QSystemTrayIcon(app)
    SystemTray.setIcon(ConfigObj.Icon_SmallImage)
    SystemTray.setVisible(True)
    SystemTray.setToolTip('uPTT')

    # NotificationObj = Notification.Notification(SystemTray, ConfigObj)
    MenuObj = Menu.Menu(SystemTray)
    MenuObj.addEvent(Menu.Type.Login, LoginFunc)
    MenuObj.addEvent(Menu.Type.About, AboutFunc)
    MenuObj.addEvent(Menu.Type.Exit, ExitFunc)

    # ChatWindow.start(ConfigObj)
    # LoginFunc()
    # ExitFunc()
    LoginFunc()

    exit_code = Appctxt.app.exec_()
    sys.exit(Appctxt.app.exec_())
