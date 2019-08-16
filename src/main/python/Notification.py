
from PyQt5.QtGui import *
import Config


class Notification(object):
    def __init__(self, SystemTray):
        self._SysTray = SystemTray

    def throw(self, Title, Message):

        self._SysTray.showMessage(
            Title,
            Message,
            QIcon(Config.SmallImage),
            3000
        )
