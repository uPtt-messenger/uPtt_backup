
from PyQt5 import QtCore


class Notification(QtCore.QObject):
    def __init__(self, SystemTray, ConfigObj):
        self._SysTray = SystemTray
        self._ConfigObj = ConfigObj

    def throw(self, Title, Message, Click=None):

        receiversCount = self._SysTray.receivers(self._SysTray.messageClicked)
        if receiversCount > 0:
            self._SysTray.messageClicked.disconnect()
        if Click is not None:
            self._SysTray.messageClicked.connect(Click)

        self._SysTray.showMessage(
            Title,
            Message,
            self._ConfigObj.Icon_SmallIcon,
            10000
        )
