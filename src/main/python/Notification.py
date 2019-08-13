
from PyQt5.QtGui import *
import Config


def throw(SystemTray, Title, Message):

    SystemTray.showMessage(
        Title,
        Message,
        QIcon(Config.SmallImage),
        3000
    )
