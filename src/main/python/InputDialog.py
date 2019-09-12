# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inputdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

Input = None


class Ui_Dialog(object):
    def setupUi(self, Dialog, Display):
        Dialog.setObjectName("Dialog")
        Dialog.resize(240, 161)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.InputEdit = QtWidgets.QLineEdit(Dialog)
        self.InputEdit.setMinimumSize(QtCore.QSize(20, 30))
        self.InputEdit.setObjectName("InputEdit")
        self.verticalLayout.addWidget(self.InputEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.OK = QtWidgets.QPushButton(Dialog)
        self.OK.setObjectName("OK")
        self.horizontalLayout.addWidget(self.OK)
        self.Cancel = QtWidgets.QPushButton(Dialog)
        self.Cancel.setObjectName("Cancel")
        self.horizontalLayout.addWidget(self.Cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog, Display)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog, Display):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", Display))
        self.OK.setText(_translate("Dialog", "確認"))
        self.Cancel.setText(_translate("Dialog", "取消"))

        self.InputEdit.textChanged.connect(self.EditChanged)
    
    def EditChanged(self, text):
        # print(f'=>{text}')
        global Input
        Input = text


def start(Display):
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog, Display)
    Dialog.show()
    Dialog.exec()

    global Input
    return Input

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

