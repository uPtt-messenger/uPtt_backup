# https://www.learnpyqt.com/courses/adanced-ui-features/system-tray-mac-menu-bar-applications-pyqt/
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

try:
    from . import About
except ImportError:
    import About


def AboutFunc():

    About.start(app)


def ExitFunc():
    print('Exit')
    sys.exit()


app = QApplication([])
app.setQuitOnLastWindowClosed(False)

# Create the icon
icon = QIcon("./src/res/Small.PNG")

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)
tray.setToolTip('PTT Postman')

# Create the menu
menu = QMenu()

action_Login = QAction('登入 PTT')
action_Login.triggered.connect(ExitFunc)

action_About = QAction('關於')
action_About.triggered.connect(AboutFunc)

action_Exit = QAction('離開')
action_Exit.triggered.connect(ExitFunc)

menu.addAction(action_Login)
menu.addAction(action_About)
menu.addSeparator()
menu.addAction(action_Exit)

# Add the menu to the tray
tray.setContextMenu(menu)

app.exec_()
