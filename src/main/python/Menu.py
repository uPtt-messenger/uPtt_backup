
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Type(object):
    Login = 1
    Logout = 2
    About = 3
    Exit = 4

    Min = Login
    Max = Exit


class Menu(object):
    def __init__(self, SystemTray):

        self._SysTray = SystemTray

        self._Menu_Login = QMenu()
        self._Menu_Logout = QMenu()

        self._action_Login = QAction('登入')
        self._action_Login.triggered.connect(self._LoginFunc)

        self._action_Logout = QAction('登出')
        self._action_Logout.triggered.connect(self._LogoutFunc)

        self._action_About = QAction('關於')
        self._action_About.triggered.connect(self._AboutFunc)

        self._action_Exit = QAction('離開')
        self._action_Exit.triggered.connect(self._ExitFunc)

        self._Menu_Login.addAction(self._action_Login)
        self._Menu_Login.addAction(self._action_About)
        self._Menu_Login.addSeparator()
        self._Menu_Login.addAction(self._action_Exit)

        self._Menu_Logout.addAction(self._action_Logout)
        self._Menu_Logout.addAction(self._action_About)
        self._Menu_Logout.addSeparator()
        self._Menu_Logout.addAction(self._action_Exit)

        self._LoginFuncList = []
        self._LogoutFuncList = []
        self._AboutFuncList = []
        self._ExitFuncList = []

    def setMenu(self, inType):
        if inType != Type.Login and inType != Type.Logout:
            raise ValueError(
                f'Type error: {inType}'
            )

        if inType == Type.Login:
            print('載入登入表單')
            self._SysTray.setContextMenu(self._Menu_Login)
        if inType == Type.Logout:
            print('載入登出表單')
            self._SysTray.setContextMenu(self._Menu_Logout)

    def _LoginFunc(self):

        result = True
        for f in self._LoginFuncList:
            result &= f()

    def _LogoutFunc(self):
        result = True
        for f in self._LogoutFuncList:
            result &= f()

    def _AboutFunc(self):
        result = True
        for f in self._AboutFuncList:
            result &= f()

    def _ExitFunc(self):
        result = True
        for f in self._ExitFuncList:
            result &= f()

    def addEvent(self, inType, Func):

        if inType < Type.Min or Type.Max < inType:
            raise ValueError(
                'Menu Type error' + str(inType)
            )

        if inType == Type.Login:
            self._LoginFuncList.insert(0, Func)
        if inType == Type.Logout:
            self._LogoutFuncList.insert(0, Func)
        if inType == Type.About:
            self._AboutFuncList.insert(0, Func)
        if inType == Type.Exit:
            self._ExitFuncList.insert(0, Func)
