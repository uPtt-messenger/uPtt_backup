# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import os
import json

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *

import Config


class Ui(object):
    def setupUi(self, Dialog, ConfigObj, FinishFunc):
        Dialog.setObjectName("Dialog")
        Dialog.resize(271, 220)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 231, 181))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.InputID = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.InputID.setAlignment(QtCore.Qt.AlignCenter)
        self.InputID.setObjectName("InputID")
        self.verticalLayout.addWidget(self.InputID)
        self.ID = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.ID.setAlignment(QtCore.Qt.AlignCenter)
        self.ID.setObjectName("ID")
        self.verticalLayout.addWidget(self.ID)
        self.InputPW = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.InputPW.setAlignment(QtCore.Qt.AlignCenter)
        self.InputPW.setObjectName("InputPW")
        self.verticalLayout.addWidget(self.InputPW)
        self.PW = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.PW.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PW.setAlignment(QtCore.Qt.AlignCenter)
        self.PW.setObjectName("PW")
        self.verticalLayout.addWidget(self.PW)
        self.RemberID = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.RemberID.setObjectName("RemberID")
        self.verticalLayout.addWidget(self.RemberID)
        self.Login = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Login.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Login.setObjectName("Login")
        self.verticalLayout.addWidget(self.Login)

        self.retranslateUi(Dialog, ConfigObj, FinishFunc)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog, ConfigObj, FinishFunc):
        def setPWFocus():
            self.PW.setFocus()
            print('設定關注到密碼視窗')

        def setLoginFocus():
            self.Login.setFocus()
            print('設定關注到登入按鈕')

        ID = ConfigObj.getValue(Config.Key_ID)
        if ID is not None:
            self.ID.setText(ID)
            self.RemberID.setChecked(True)

        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PTT Postman 登入"))
        Dialog.setWindowIcon(QIcon(Config.SmallImage))
        Dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        
        self.InputID.setText(_translate("Dialog", "請輸入帳號"))
        self.InputID.setFont(Config.BasicFont)
        self.InputPW.setText(_translate("Dialog", "請輸入密碼"))
        self.InputPW.setFont(Config.BasicFont)
        self.RemberID.setText(_translate("Dialog", "記住帳號"))
        self.Login.setText(_translate("Dialog", "登入"))
        self.Login.setFont(Config.BasicFont)
        self.Login.clicked.connect(FinishFunc)

        self.ID.returnPressed.connect(setPWFocus)
        self.PW.returnPressed.connect(setLoginFocus)
        self.PW.editingFinished.connect(setLoginFocus)
        # self.RemberID.stateChanged.connect(RemberID_StateChanged)

    def getIDPW(self):
        return self.ID.text(), self.PW.text(), self.RemberID.isChecked()


PressLogin = False


def start(ConfigObj):

    global PressLogin
    PressLogin = False

    Dialog = QtWidgets.QDialog()
    ui = Ui()

    def finish():
        global PressLogin
        PressLogin = True
        print('Login finish')
        Dialog.close()

    ui.setupUi(Dialog, ConfigObj, finish)
    Dialog.show()
    Dialog.exec()

    if PressLogin:
        return ui.getIDPW()
    return None, None, None


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
