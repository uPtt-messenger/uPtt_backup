# https://www.learnpyqt.com/courses/adanced-ui-features/system-tray-mac-menu-bar-applications-pyqt/
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def Exit():
    sys.exit()


app = QApplication([])
app.setQuitOnLastWindowClosed(False)

# Create the icon
icon = QIcon("./src/res/Small.PNG")

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Create the menu
menu = QMenu()
action = QAction('Exit')
action.triggered.connect(Exit)

menu.addAction(action)

# Add the menu to the tray
tray.setContextMenu(menu)

app.exec_()
