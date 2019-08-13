# https://www.learnpyqt.com/courses/adanced-ui-features/system-tray-mac-menu-bar-applications-pyqt/
import sys
import os
import time
import threading
import json
import traceback

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

Menu_Login = None
Menu_Logout = None

ThreadRun = False
ConfigObj = None


def genMenu():

    global LoginStatus
    global Menu_Logout
    global Menu_Login
    global SystemTray

    if LoginStatus:
        print('Menu_Login is None: ' + str(Menu_Login is None))
        SystemTray.setContextMenu(Menu_Login)
    else:
        print('Menu_Logout is None: ' + str(Menu_Logout is None))
        SystemTray.setContextMenu(Menu_Logout)


def checkMailFunc(ID, PW):
    global PTTBot
    global ThreadRun
    global LoginStatus
    global SystemTray

    PTTBot = PTT.Library()
    try:
        PTTBot.login(ID, PW)
    except PTT.Exceptions.LoginError:
        PTTBot.log('登入失敗')
        Notification.throw(SystemTray, 'PTT Postman', '登入失敗')
        PTTBot = None
        return

    PTTBot.log('登入成功')
    Notification.throw(SystemTray, 'PTT Postman', '登入成功')
    LoginStatus = True
    genMenu()

    ShowNewMail = False
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


ConfigObj = Config.Config()

app = QApplication([])
app.setQuitOnLastWindowClosed(False)
icon = QIcon(Config.SmallImage)

SystemTray = QSystemTrayIcon(app)
SystemTray.setIcon(icon)
SystemTray.setVisible(True)
SystemTray.setToolTip('PTT Postman')

Menu_Login = QMenu()
Menu_Logout = QMenu()

action_Login = QAction('登入')
action_Login.triggered.connect(LoginFunc)

action_Logout = QAction('登出')
action_Logout.triggered.connect(LogoutFunc)

action_About = QAction('關於')
action_About.triggered.connect(AboutFunc)

action_Exit = QAction('離開')
action_Exit.triggered.connect(ExitFunc)

Menu_Login.addAction(action_Logout)
Menu_Login.addAction(action_About)
Menu_Login.addSeparator()
Menu_Login.addAction(action_Exit)

Menu_Logout.addAction(action_Login)
Menu_Logout.addAction(action_About)
Menu_Logout.addSeparator()
Menu_Logout.addAction(action_Exit)

genMenu()
LoginFunc()

app.exec_()
