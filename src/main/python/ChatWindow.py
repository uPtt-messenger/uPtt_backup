# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog, Target):
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

        self.retranslateUi(Dialog, Target)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog, Target):

        def sendMsg():
            import Log

            Msg = self.lineEdit.text()
            Log.showValue(
                f'Chat Window with {Target}',
                Log.Level.INFO,
                '送出訊息',
                Msg
            )

            self.lineEdit.setText('')

            SI = QtWidgets.QSpacerItem(
                0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

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

            self.SAObj.layout().addLayout(H)

        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", Target))

        self.SAObj = QtWidgets.QWidget(self.scrollArea)
        self.SAObj.setLayout(QtWidgets.QVBoxLayout())

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


def start(ConfigObj, Target=None):

    if Target is None:
        import InputDialog
        OK, TargetID = InputDialog.start('請輸入水球對象帳號')
        if not OK:
            return
        print(f'TargetID [{TargetID}]')
    else:
        TargetID = Target

    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog, TargetID)
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
