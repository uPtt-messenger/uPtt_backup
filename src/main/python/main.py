# https://www.learnpyqt.com/courses/adanced-ui-features/system-tray-mac-menu-bar-applications-pyqt/
import sys
import os
import time
import threading
import json
import traceback

from fbs_runtime.application_context.PyQt5 import ApplicationContext

from PyQt5 import QtCore
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
import Log


def LoginFunc():

    global MenuObj
    global PTTCoreObj
    global ID

    ID, PW, SaveID = Login.start(ConfigObj)

    if ID is None or PW is None:
        NotifiObj.throw('uPTT', '登入取消')
        MenuObj.setMenu(Menu.Type.Login)
        return True
    if len(ID) < 3 or len(PW) == 0:
        NotifiObj.throw('uPTT', '登入取消')
        MenuObj.setMenu(Menu.Type.Login)
        return True

    if SaveID:
        ConfigObj.setValue(ConfigObj.Key_ID, ID)
    else:
        ConfigObj.setValue(ConfigObj.Key_ID, None)

    Log.showValue(
        'uPTT Main',
        Log.Level.INFO,
        '帳號',
        ID
    )
    Log.showValue(
        'uPTT Main',
        Log.Level.INFO,
        '密碼',
        PW
    )

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
    global PTTCoreObj
    if PTTCoreObj is not None:
        if not PTTCoreObj.isStop():
            PTTCoreObj.stop()
            while not PTTCoreObj.isStop():
                time.sleep(0.1)

    return True


def StartChatWindowFunc():
    global SystemTray
    global ConfigObj
    global PTTCoreObj
    ChatWindow.start(SystemTray, ConfigObj, PTTCoreObj)
    return True


def AboutFunc():
    About.start(ConfigObj)

    return True


def ExitFunc():
    global SystemTray

    SystemTray.hide()
    LogoutFunc()
    Log.log(
        'uPTT Main',
        Log.Level.INFO,
        '離開程式'
    )
    NotifiObj.throw('uPTT', '程式結束')
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

    NotifiObj = Notification.Notification(SystemTray, ConfigObj)
    MenuObj = Menu.Menu(SystemTray)
    MenuObj.addEvent(Menu.Type.Login, LoginFunc)
    MenuObj.addEvent(Menu.Type.Logout, LogoutFunc)
    MenuObj.addEvent(Menu.Type.About, AboutFunc)
    MenuObj.addEvent(Menu.Type.ThrowWaterBall, StartChatWindowFunc)
    MenuObj.addEvent(Menu.Type.Exit, ExitFunc)
    MenuObj.setMenu(Menu.Type.Login)

    NotifiObj.throw('uPTT', '啟動成功')
    # ChatWindow.start(ConfigObj)
    # LoginFunc()
    # ExitFunc()
    LoginFunc()

    exit_code = Appctxt.app.exec_()
    sys.exit(Appctxt.app.exec_())
