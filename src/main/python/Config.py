
import os
import json
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *


class Config(object):
    def __init__(self, Appctxt):

        self.Key_ID = 'ID'

        self.TitleFont = QtGui.QFont('微軟正黑體', 14, QtGui.QFont.Bold)
        self.BasicFont = QtGui.QFont('微軟正黑體', 14, QtGui.QFont.Bold)

        self.Icon_OriImage = QtGui.QIcon(Appctxt.get_resource('OriginIcon.png'))
        self.Icon_SmallImage = QtGui.QIcon(Appctxt.get_resource('Small.png'))
        self.Icon_SmallIcon = QtGui.QIcon(Appctxt.get_resource('Icon.ico'))

        self.ConfigFileName = 'PTTPostman.txt'
        self.ConfigPath = None

        if os.name == 'nt':
            print('Windows')
            self.ConfigPath = 'C:/ProgramData/PTTPostman/'

        self.ConfigFullPath = self.ConfigPath + self.ConfigFileName

        if not os.path.exists(self.ConfigPath):
            os.makedirs(self.ConfigPath)

        self.Data = dict()
        try:
            with open(self.ConfigFullPath, encoding='utf8') as File:
                self.Data = json.load(File)
        except Exception as e:
            pass

    def getValue(self, Key):
        if Key not in self.Data:
            return None
        return self.Data[Key]

    def setValue(self, Key, Value):

        if Value is not None:
            self.Data[Key] = Value
        elif Key in self.Data:
            del self.Data[Key]

        with open(self.ConfigFullPath, 'w', encoding='utf8') as File:
            json.dump(self.Data, File, indent=4, ensure_ascii=False)
