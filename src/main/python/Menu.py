
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MenuType(object):
    Login = 1
    Logout = 2
    Exit = 3

    Min = Login
    Max = Exit


class Menu(object):
    def __init__(self, SystemTray):

        self._SysTray = SystemTray

        self._Menu_Login = QMenu()
        self._Menu_Logout = QMenu()

        action_Login = QAction('登入')
        action_Login.triggered.connect(self._LoginFunc)

        action_Logout = QAction('登出')
        action_Logout.triggered.connect(self._LogoutFunc)

        action_About = QAction('關於')
        action_About.triggered.connect(self._AboutFunc)

        action_Exit = QAction('離開')
        action_Exit.triggered.connect(self._ExitFunc)

        self._Menu_Login.addAction(action_Logout)
        self._Menu_Login.addAction(action_About)
        self._Menu_Login.addSeparator()
        self._Menu_Login.addAction(action_Exit)

        self._Menu_Logout.addAction(action_Login)
        self._Menu_Logout.addAction(action_About)
        self._Menu_Logout.addSeparator()
        self._Menu_Logout.addAction(action_Exit)

        self._SysTray.setContextMenu(self._Menu_Logout)

        self._LoginFuncList = []
        self._LogoutFuncList = []
        self._ExitFuncList = []

    def _LoginFunc(self):

        result = True
        for f in self._LoginFuncList:
            result &= f()

    def _LogoutFunc(self):
        result = True
        for f in self._LogoutFuncList:
            result &= f()

    def _ExitFunc(self):
        result = True
        for f in self._ExitFuncList:
            result &= f()

    def addEvent(self, Type, Func):

        if Type > MenuType.Min or MenuType.Max < Type:
            raise ValueError(
                'Menu Type error' + Type
            )

        if Type == MenuType.Login:
            self._LoginFuncList.append(Func)
        if Type == MenuType.Logout:
            self._LogoutFuncList.append(Func)
        if Type == MenuType.Exit:
            self._ExitFuncList.append(Func)
