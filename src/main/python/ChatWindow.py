# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PTTLibrary import PTT

import Config


class Ui_Dialog(object):
    def setupUi(self, Dialog, ConfigObj, PTTCoreObj, Target):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 500)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.SettingLayout = QtWidgets.QVBoxLayout()
        self.SettingLayout.setSpacing(0)
        self.SettingLayout.setObjectName("SettingLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMaximumSize(QtCore.QSize(16777215, 10))
        self.label.setText("")
        self.label.setObjectName("label")
        self.SettingLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.OnlineState = QtWidgets.QLabel(Dialog)
        self.OnlineState.setMinimumSize(QtCore.QSize(100, 0))
        self.OnlineState.setMaximumSize(QtCore.QSize(100, 16777215))
        self.OnlineState.setAlignment(QtCore.Qt.AlignCenter)
        self.OnlineState.setObjectName("OnlineState")
        self.horizontalLayout_2.addWidget(self.OnlineState)
        self.Remarks = QtWidgets.QLineEdit(Dialog)
        self.Remarks.setToolTip("")
        self.Remarks.setObjectName("Remarks")
        self.horizontalLayout_2.addWidget(self.Remarks)
        self.SettingLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(
            40, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.OptionSwitch = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.OptionSwitch.sizePolicy().hasHeightForWidth())
        self.OptionSwitch.setSizePolicy(sizePolicy)
        self.OptionSwitch.setMinimumSize(QtCore.QSize(0, 0))
        self.OptionSwitch.setMaximumSize(QtCore.QSize(16777215, 15))
        self.OptionSwitch.setObjectName("OptionSwitch")
        self.horizontalLayout_3.addWidget(self.OptionSwitch)
        self.SettingLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.NotificationSwitch = QtWidgets.QPushButton(Dialog)
        self.NotificationSwitch.setObjectName("NotificationSwitch")
        self.horizontalLayout_4.addWidget(self.NotificationSwitch)
        self.BlockSwitch = QtWidgets.QPushButton(Dialog)
        self.BlockSwitch.setObjectName("BlockSwitch")
        self.horizontalLayout_4.addWidget(self.BlockSwitch)
        self.SettingLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addLayout(self.SettingLayout)
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setEnabled(True)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Box)
        self.scrollArea.setLineWidth(1)
        self.scrollArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 297, 309))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 60))
        self.lineEdit.setFrame(False)
        self.lineEdit.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog, ConfigObj, PTTCoreObj, Target)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog, ConfigObj, PTTCoreObj, Target):

        def sendMsg():
            import Log
            global NotifiObj

            Msg = self.lineEdit.text()
            Log.showValue(
                f'Chat Window with {Target}',
                Log.Level.INFO,
                '送出訊息',
                Msg
            )

            self.lineEdit.setText('')

            ErrorMsg = PTTCoreObj.throwWaterBall(Target, Msg)
            if ErrorMsg is not None:
                NotifiObj.throw('uPTT', ErrorMsg)
                return

            SI = QtWidgets.QSpacerItem(
                0,
                0,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Minimum
            )

            Name = QtWidgets.QLabel()
            Name.setText('★')
            Name.setStyleSheet(
                'QLabel{color:rgb(255, 255, 0, 250);background:rgb(0, 128, 128, 250);}'
            )

            Content = QtWidgets.QLabel()
            Content.setText(Msg)
            Content.setStyleSheet(
                'QLabel{color:rgb(255, 255, 255, 250);background:rgb(128, 0, 128, 250);}'
            )

            H = QtWidgets.QHBoxLayout()
            H.setSpacing(0)

            H.addSpacerItem(SI)
            H.addWidget(Name)
            H.addWidget(Content)

            self.SAObj.layout().insertLayout(self._InsertIndex, H)
            self._InsertIndex += 1

        def recvMsg(Waterball):
            print(f'視窗收到水球 {Waterball.getContent()}')

            SI = QtWidgets.QSpacerItem(
                0,
                0,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Minimum
            )

            Name = QtWidgets.QLabel()
            Name.setText('★')
            Name.setStyleSheet(
                'QLabel{color:rgb(255, 255, 0, 250);background:rgb(0, 128, 128, 250);}'
            )

            Content = QtWidgets.QLabel()
            Content.setText(Waterball.getContent())
            Content.setStyleSheet(
                'QLabel{color:rgb(255, 255, 255, 250);background:rgb(128, 0, 128, 250);}'
            )

            H = QtWidgets.QHBoxLayout()
            H.setSpacing(0)

            H.addWidget(Name)
            H.addWidget(Content)
            H.addSpacerItem(SI)

            self.SAObj.layout().insertLayout(self._InsertIndex, H)
            self._InsertIndex += 1

        def blockUser():
            print('QQ block')

        self._InsertIndex = 0

        ErrorMsg, User = PTTCoreObj.getUser(Target)

        if ErrorMsg is not None:
            NotifiObj.throw('uPTT', ErrorMsg)
            return

        # BlockList = ConfigObj.getValue(
        #     Config.Type.User,
        #     Config.Key_Blacklist
        # )

        # print(BlockList)

        # BlockList = ConfigObj.setValue(
        #     Config.Type.User,
        #     Config.Key_Blacklist,
        #     [
        #         'TestUSer1',
        #         'TestUSer2',
        #         'TestUSer3',
        #     ]
        # )

        Temp = User.getID()
        Target = Temp[:Temp.find('(')].strip()

        NickName = Temp
        NickName = NickName[NickName.find('(') + 1:]
        NickName = NickName[:NickName.rfind(')')]

        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.OnlineState.setToolTip(_translate("Dialog", "上線狀態"))

        if User.getState() != '不在站上':
            self.OnlineState.setText(_translate("Dialog", '不在線上'))
        else:
            self.OnlineState.setText(_translate("Dialog", '上線中'))
        self.Remarks.setText(_translate("Dialog", NickName))
        self.OptionSwitch.setText(_translate("Dialog", "PushButton"))
        self.NotificationSwitch.setText(_translate("Dialog", "關閉提醒"))
        self.BlockSwitch.setText(_translate("Dialog", "封鎖"))

        Dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        Dialog.setWindowTitle(_translate("Dialog", Target))

        self.scrollArea.setAutoFillBackground(True)
        bar = self.scrollArea.verticalScrollBar()
        bar.rangeChanged.connect(lambda x, y: bar.setValue(y))

        self.SAObj = QtWidgets.QWidget()

        VBOX = QtWidgets.QVBoxLayout()
        VBOX.addStretch()

        self.SAObj.setLayout(VBOX)
        self.scrollArea.setWidget(self.SAObj)

        self.lineEdit.returnPressed.connect(sendMsg)
        PTTCoreObj.registerWaterball(Dialog, recvMsg, Target)


def start(SystemTray, ConfigObj, PTTCoreObj, Target=None):
    import Notification
    global NotifiObj
    NotifiObj = Notification.Notification(
        SystemTray,
        ConfigObj
    )

    if Target is None:
        import InputDialog
        OK, TargetID = InputDialog.start('請輸入水球對象帳號')
        if not OK:
            return
    else:
        TargetID = Target

    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog, ConfigObj, PTTCoreObj, TargetID)
    Dialog.show()
    return Dialog
    # Dialog.exec()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
