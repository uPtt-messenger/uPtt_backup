# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog, PTTCoreObj, Target):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 500)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setEnabled(True)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 298, 430))
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

        self.retranslateUi(Dialog, PTTCoreObj, Target)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog, PTTCoreObj, Target):

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
                'QLabel{color:rgb(255, 255, 0, 250);background:rgb(0, 128, 128, 250);}')

            Content = QtWidgets.QLabel()
            Content.setText(Msg)
            Content.setStyleSheet(
                'QLabel{color:rgb(255, 255, 255, 250);background:rgb(128, 0, 128, 250);}')

            H = QtWidgets.QHBoxLayout()
            H.setSpacing(0)

            H.addSpacerItem(SI)
            H.addWidget(Name)
            H.addWidget(Content)

            # self.SAObj.layout().addLayout(H)
            # insertLayout
            self.SAObj.layout().insertLayout(self._InsertIndex, H)
            self._InsertIndex += 1

        self._InsertIndex = 0

        _translate = QtCore.QCoreApplication.translate
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

        # for i in range(40):
        #     H = QtWidgets.QHBoxLayout()
        #     H.setSpacing(0)

        #     Name = QtWidgets.QLabel()
        #     Name.setText('★')
        #     Name.setStyleSheet(
        #         'QLabel{color:rgb(255, 255, 0, 250);background:rgb(0, 128, 128, 250);}')

        #     Content = QtWidgets.QLabel()
        #     Content.setText(f'測試水球')
        #     Content.setStyleSheet(
        #         'QLabel{color:rgb(255, 255, 255, 250);background:rgb(128, 0, 128, 250);}')

        #     SI = QtWidgets.QSpacerItem(
        #         0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        #     if i % 2 == 0:
        #         H.addWidget(Name)
        #         H.addWidget(Content)
        #         H.addSpacerItem(SI)
        #     else:
        #         H.addSpacerItem(SI)
        #         H.addWidget(Name)
        #         H.addWidget(Content)

        #     self.SAObj.layout().addLayout(H)


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

        ErrorMsg, User = PTTCoreObj.getUser(TargetID)

        if ErrorMsg is not None:
            NotifiObj.throw('uPTT', ErrorMsg)
            return

        TargetID = User.getID()

        if '不在站上' in User.getState():
            NotifiObj.throw('uPTT', f'{TargetID} 不在站上')
            return

        TargetID = TargetID[:TargetID.find('(')].strip()

        print(f'TargetID [{TargetID}]')
    else:
        TargetID = Target

    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog, PTTCoreObj, TargetID)
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
