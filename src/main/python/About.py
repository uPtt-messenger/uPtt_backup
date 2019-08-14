# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *

import Ver
import Config


class Ui(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(590, 340)
        Dialog.setMinimumSize(QtCore.QSize(590, 340))
        Dialog.setMaximumSize(QtCore.QSize(590, 340))
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(300, 300, 261, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(350, 20, 221, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Name = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Name.setObjectName("Name")
        self.verticalLayout.addWidget(self.Name)
        self.Version = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Version.setObjectName("Version")
        self.verticalLayout.addWidget(self.Version)
        self.Developer = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Developer.setObjectName("Developer")
        self.verticalLayout.addWidget(self.Developer)
        self.SourceCode = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.SourceCode.setTextFormat(QtCore.Qt.AutoText)
        self.SourceCode.setObjectName("SourceCode")
        self.verticalLayout.addWidget(self.SourceCode)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.IfhasQuestion = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.IfhasQuestion.setObjectName("IfhasQuestion")
        self.verticalLayout.addWidget(self.IfhasQuestion)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.OneQuestion = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.OneQuestion.setObjectName("OneQuestion")
        self.horizontalLayout.addWidget(self.OneQuestion)
        self.Issue = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Issue.setTextFormat(QtCore.Qt.AutoText)
        self.Issue.setObjectName("Issue")
        self.horizontalLayout.addWidget(self.Issue)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.TwoQuestion = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.TwoQuestion.setObjectName("TwoQuestion")
        self.horizontalLayout.addWidget(self.TwoQuestion)
        self.Gitter = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Gitter.setObjectName("Gitter")
        self.horizontalLayout.addWidget(self.Gitter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.IconDisplay = QtWidgets.QLabel(Dialog)
        self.IconDisplay.setGeometry(QtCore.QRect(20, 20, 300, 300))
        self.IconDisplay.setObjectName("IconDisplay")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowIcon(QIcon(Config.SmallImage))
        Dialog.setWindowTitle(_translate("Dialog", " 關於 PTT Postman"))
        Dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.Name.setText(_translate("Dialog", "PTT Postman"))
        self.Name.setFont(Config.TitleFont)

        self.Version.setText(_translate("Dialog", "版本: " + Ver.V))
        self.Version.setFont(Config.BasicFont)

        self.Developer.setText(_translate(
            "Dialog", "開發: CodingMan"))
        self.Developer.setFont(Config.BasicFont)

        self.IfhasQuestion.setText(_translate(
            "Dialog", "如果你有任何問題"))
        self.IfhasQuestion.setFont(Config.BasicFont)

        self.OneQuestion.setText(_translate(
            "Dialog", "1."))
        self.OneQuestion.setFont(Config.BasicFont)

        self.TwoQuestion.setText(_translate(
            "Dialog", "2."))
        self.TwoQuestion.setFont(Config.BasicFont)

        self.Issue.setText(_translate(
            "Dialog", "<a href=\"https://github.com/Truth0906/PTTPostman/issues/new\">填寫問題單</a>"))
        self.Issue.setOpenExternalLinks(True)
        self.Issue.setFont(Config.BasicFont)

        self.Gitter.setText(_translate(
            "Dialog", "<a href=\"https://gitter.im/PTTPostman/TalkingRoom\">線上找我</a>"))
        self.Gitter.setOpenExternalLinks(True)
        self.Gitter.setFont(Config.BasicFont)

        self.SourceCode.setText(_translate(
            "Dialog", "<a href=\"https://github.com/Truth0906/PTTPostman\">原始碼</a>"))
        self.SourceCode.setOpenExternalLinks(True)
        self.SourceCode.setFont(Config.BasicFont)

        self.IconDisplay.setText(_translate("Dialog", "TextLabel"))

        IconImage = QPixmap(Config.OriImage)
        IconImage = IconImage.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        self.IconDisplay.setPixmap(IconImage)


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
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

