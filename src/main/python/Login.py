# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(442, 290)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 20, 341, 181))
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

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.InputID.setText(_translate("Form", "TextLabel"))
        self.InputPW.setText(_translate("Form", "TextLabel"))
        self.RemberID.setText(_translate("Form", "CheckBox"))
        self.Login.setText(_translate("Form", "PushButton"))
    
    def getIDPW(self):
        return self.ID.getText(), self.PW.getText()


def start():
    Form = QtWidgets.QWidget()
    ui = Ui()
    ui.setupUi(Form)
    Form.show()
    Form.exec()

    return ui.getIDPW()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

