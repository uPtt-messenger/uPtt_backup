
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import Log


class Type(object):
    Login = 1
    Logout = 2
    ThrowWaterBall = 3
    About = 4
    Exit = 5

    Min = Login
    Max = Exit


class Menu(object):
    def __init__(self, SystemTray):

        self._SysTray = SystemTray

        self._Menu_Login = QtWidgets.QMenu()
        self._Menu_Logout = QtWidgets.QMenu()

        self._action_Login = QtWidgets.QAction('登入')
        self._action_Login.triggered.connect(self._LoginFunc)

        self._action_Logout = QtWidgets.QAction('登出')
        self._action_Logout.triggered.connect(self._LogoutFunc)

        self._action_ThrowWaterBall = QtWidgets.QAction('丟水球')
        self._action_ThrowWaterBall.triggered.connect(self._ThrowWaterBallFunc)

        self._action_About = QtWidgets.QAction('關於')
        self._action_About.triggered.connect(self._AboutFunc)

        self._action_Exit = QtWidgets. QAction('離開')
        self._action_Exit.triggered.connect(self._ExitFunc)

        self._Menu_Login.addAction(self._action_Login)
        self._Menu_Login.addAction(self._action_About)
        self._Menu_Login.addSeparator()
        self._Menu_Login.addAction(self._action_Exit)

        self._Menu_Logout.addAction(self._action_Logout)
        self._Menu_Logout.addAction(self._action_ThrowWaterBall)
        self._Menu_Logout.addAction(self._action_About)
        self._Menu_Logout.addSeparator()
        self._Menu_Logout.addAction(self._action_Exit)

        self._LoginFuncList = []
        self._LogoutFuncList = []
        self._ThrowWaterBallFuncList = []
        self._AboutFuncList = []
        self._ExitFuncList = []

    def setMenu(self, inType):
        if inType != Type.Login and inType != Type.Logout:
            raise ValueError(
                f'Type error: {inType}'
            )

        if inType == Type.Login:
            Log.log(
                'uPTT Menu',
                Log.Level.INFO,
                '載入登入表單'
            )
            self._SysTray.setContextMenu(self._Menu_Login)
        if inType == Type.Logout:
            Log.log(
                'uPTT Menu',
                Log.Level.INFO,
                '載入登出表單'
            )
            self._SysTray.setContextMenu(self._Menu_Logout)

    def _LoginFunc(self):

        result = True
        for f in self._LoginFuncList:
            result &= f()

        Log.log(
            'uPTT Menu',
            Log.Level.INFO,
            '所有登入事件執行完畢'
        )

    def _LogoutFunc(self):
        result = True
        for f in self._LogoutFuncList:
            result &= f()

        Log.log(
            'uPTT Menu',
            Log.Level.INFO,
            '所有登出事件執行完畢'
        )

    def _ThrowWaterBallFunc(self):
        result = True
        for f in self._ThrowWaterBallFuncList:
            result &= f()

        Log.log(
            'uPTT Menu',
            Log.Level.INFO,
            '所有啟動丟水球事件執行完畢'
        )

    def _AboutFunc(self):
        result = True
        for f in self._AboutFuncList:
            result &= f()

        Log.log(
            'uPTT Menu',
            Log.Level.INFO,
            '所有關於事件執行完畢'
        )

    def _AboutFunc(self):
        result = True
        for f in self._AboutFuncList:
            result &= f()

        Log.log(
            'uPTT Menu',
            Log.Level.INFO,
            '所有關於事件執行完畢'
        )

    def _ExitFunc(self):
        result = True
        for f in self._ExitFuncList:
            result &= f()

        Log.log(
            'uPTT Menu',
            Log.Level.INFO,
            '所有離開事件執行完畢'
        )

    def addEvent(self, inType, Func):

        if inType < Type.Min or Type.Max < inType:
            raise ValueError(
                'Menu Type error' + str(inType)
            )

        if inType == Type.Login:
            self._LoginFuncList.insert(0, Func)
        if inType == Type.Logout:
            self._LogoutFuncList.insert(0, Func)
        if inType == Type.ThrowWaterBall:
            self._ThrowWaterBallFuncList.insert(0, Func)
        if inType == Type.About:
            self._AboutFuncList.insert(0, Func)
        if inType == Type.Exit:
            self._ExitFuncList.insert(0, Func)
