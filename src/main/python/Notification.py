
from PyQt5.QtGui import *


class Notification(object):
    def __init__(self, SystemTray, ConfigObj):
        self._SysTray = SystemTray
        self._ConfigObj = ConfigObj

    def throw(self, Title, Message):

        self._SysTray.showMessage(
            Title,
            Message,
            self._ConfigObj.Icon_SmallIcon,
            3000
        )
