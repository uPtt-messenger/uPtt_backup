# https://www.learnpyqt.com/courses/adanced-ui-features/system-tray-mac-menu-bar-applications-pyqt/
import sys
import time

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


def genMenu():

    global LoginStatus
    global Menu_Logout
    global Menu_Login

    if LoginStatus:
        SystemTray.setContextMenu(Menu_Login)
    else:
        SystemTray.setContextMenu(Menu_Logout)


def checkMailFunc():
    global PTTBot
    global ThreadRun

    while ThreadRun:
        if PTTBot.hasNewMail():
            QMessageBox.information(
                self,
                'Ttile',
                'Msg',
                QMessageBox.Yes
            )


def LoginFunc():
    global LoginStatus
    global PTTBot

    LoginStatus = False

    ID, PW = Login.start()

    if ID is None or PW is None:
        Notification.throw('PTT Postman', '登入取消')
        return
    if len(ID) < 3 or len(PW) == 0:
        Notification.throw('PTT Postman', '登入取消')
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
    Notification.throw('PTT Postman', '登入成功')
    LoginStatus = True
    genMenu()

    ThreadRun = True


def LogoutFunc():
    global LoginStatus
    global PTTBot

    LoginStatus = False

    if PTTBot is not None:
        PTTBot.logout()
        PTTBot = None
        Notification.throw('PTT Postman', '登出成功')


def AboutFunc():

    About.start()


def ExitFunc():

    LogoutFunc()
    print('Exit')
    sys.exit()


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

# msg = QMessageBox()
# # msg.setIcon(QMessageBox.Information)
# msg.setText("This is a message box")
# msg.setWindowTitle("MessageBox demo")
# msg.setWindowIcon(QIcon(Config.SmallImage))
# # msg.setInformativeText("This is additional information")
# # msg.setDetailedText("The details are as follows:")
# msg.exec_()

NewMail.start()

app.exec_()
