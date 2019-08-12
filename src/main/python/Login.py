# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 281)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 40, 341, 181))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.InputID = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.InputID.setObjectName("InputID")
        self.verticalLayout.addWidget(self.InputID)
        self.ID = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.ID.setObjectName("ID")
        self.verticalLayout.addWidget(self.ID)
        self.InputPW = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.InputPW.setObjectName("InputPW")
        self.verticalLayout.addWidget(self.InputPW)
        self.PW = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.PW.setEchoMode(QtWidgets.QLineEdit.Password)
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
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.InputID.setText(_translate("Dialog", "TextLabel"))
        self.InputPW.setText(_translate("Dialog", "TextLabel"))
        self.RemberID.setText(_translate("Dialog", "CheckBox"))
        self.Login.setText(_translate("Dialog", "PushButton"))

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
