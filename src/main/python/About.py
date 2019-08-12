# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *

import Ver


class Ui(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(590, 340)
        Dialog.setMinimumSize(QtCore.QSize(590, 340))
        Dialog.setMaximumSize(QtCore.QSize(590, 340))
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(300, 290, 261, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(350, 20, 221, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Version = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Version.setObjectName("Version")
        self.verticalLayout.addWidget(self.Version)
        self.Developer = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Developer.setObjectName("Developer")
        self.verticalLayout.addWidget(self.Developer)
        self.Issue = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Issue.setTextFormat(QtCore.Qt.AutoText)
        self.Issue.setObjectName("Issue")
        self.verticalLayout.addWidget(self.Issue)
        self.SourceCode = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.SourceCode.setTextFormat(QtCore.Qt.AutoText)
        self.SourceCode.setObjectName("SourceCode")
        self.verticalLayout.addWidget(self.SourceCode)
        self.IconDisplay = QtWidgets.QLabel(Dialog)
        self.IconDisplay.setGeometry(QtCore.QRect(20, 20, 300, 300))
        self.IconDisplay.setObjectName("IconDisplay")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowIcon(QIcon('./src/res/Small.PNG'))
        Dialog.setWindowTitle(_translate("Dialog", " 關於 PTT Postman"))

        Font = QtGui.QFont('微軟正黑體', 14, QtGui.QFont.Bold) 

        self.Version.setText(_translate("Dialog", "PTT Postman v " + Ver.V))
        self.Version.setFont(Font)

        self.Developer.setText(_translate(
            "Dialog", "Developer: CodingMan"))
        self.Developer.setFont(Font)

        self.Issue.setText(_translate(
            "Dialog", "<a href=\"https://github.com/Truth0906/PTTPostman/issues/new\">回報問題</a>"))
        self.Issue.setOpenExternalLinks(True)
        self.Issue.setFont(Font)

        self.SourceCode.setText(_translate(
            "Dialog", "<a href=\"https://github.com/Truth0906/PTTPostman\">原始碼</a>"))
        self.SourceCode.setOpenExternalLinks(True)
        self.SourceCode.setFont(Font)

        self.IconDisplay.setText(_translate("Dialog", "TextLabel"))

        IconImage = QPixmap('./src/res/OriginIcon.PNG')
        IconImage = IconImage.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        self.IconDisplay.setPixmap(IconImage)

        
        

def start(app):

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

