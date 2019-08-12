# https://www.learnpyqt.com/courses/adanced-ui-features/system-tray-mac-menu-bar-applications-pyqt/
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import PTTLibrary
from PTTLibrary import PTT

import About
import Login

LoginStatus = False
PTTBot = None
SystemTray = None

Menu_Login = None
Menu_Logout = None


def LoginFunc():
    global LoginStatus
    global PTTBot

    LoginStatus = False

    ID, PW = Login.start()

    if ID is None or PW is None:
        return

    print('ID: ' + ID)
    print('PW: ' + PW)

    PTTBot = PTT.Library()
    try:
        PTTBot.login(ID, PW)
    except PTT.Exceptions.LoginError:
        PTTBot.log('登入失敗')
        return

    PTTBot.log('登入成功')
    LoginStatus = True


def LogoutFunc():
    global LoginStatus
    global PTTBot

    LoginStatus = False
    PTTBot.logout()


def AboutFunc():

    About.start()


def ExitFunc():
    print('Exit')
    sys.exit()


def genMenu():

    SystemTray.setContextMenu(Menu_Login)


app = QApplication([])
app.setQuitOnLastWindowClosed(False)
icon = QIcon("./src/res/Small.PNG")

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

# SystemTray.setContextMenu(Menu_Logout)
genMenu()
app.exec_()
