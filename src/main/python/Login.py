# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *

import Config

class Ui(object):
    def setupUi(self, Dialog):
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
        self.Login.setObjectName("Login")
        self.verticalLayout.addWidget(self.Login)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PTT Postman - 登入"))
        Dialog.setWindowIcon(QIcon('./src/res/Small.PNG'))
        self.InputID.setText(_translate("Dialog", "請輸入帳號"))
        self.InputID.setFont(Config.BasicFont)
        self.InputPW.setText(_translate("Dialog", "請輸入密碼"))
        self.InputPW.setFont(Config.BasicFont)
        self.RemberID.setText(_translate("Dialog", "記住密碼"))
        self.Login.setText(_translate("Dialog", "登入"))
        self.Login.setFont(Config.BasicFont)

    def getIDPW(self):
        return self.ID.getText(), self.PW.getText()


def start():
    Dialog = QtWidgets.QDialog()
    ui = Ui()
    ui.setupUi(Dialog)
    Dialog.show()
    Dialog.exec()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

