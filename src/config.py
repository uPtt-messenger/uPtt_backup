
import os
import json

import log


class Type:
    System = 1
    User = 2


Key_CurrentUser = 'CurrentUser'
Key_ID = 'ID'
Key_Password = 'Password'
Key_Blacklist = 'Blacklist'


class Config:

    def __init__(self):
        # 不想給使用者改的設定值就寫在這兒
        # 想給使用者改的就透過 setValue
        # 因為會被存起來
        self.Version = '0.1.0'
        self.QueryCycle = 3.1
        self.RecoverTime = 2
        self.Port = 50730

        self.ConfigFileName = 'Config.txt'
        self.ConfigPath = None

        if os.name == 'nt':
            log.showValue(
                'Config',
                log.Level.INFO,
                '作業系統',
                'Windows'
            )
            self.ConfigPath = 'C:/ProgramData/uPtt/'

        self.ConfigFullPath = self.ConfigPath + self.ConfigFileName
        self.UserConfigPath = None

        if not os.path.exists(self.ConfigPath):
            os.makedirs(self.ConfigPath)

        try:
            with open(self.ConfigFullPath, encoding='utf8') as File:
                self.SystemData = json.load(File)
        except FileNotFoundError:
            self.SystemData = dict()

        self.UserData = dict()

        log.showValue(
            'Config',
            log.Level.INFO,
            '設定檔',
            '初始化'
        )

    def initUser(self, ID):
        self.UserConfigPath = f'{self.ConfigPath}{ID}/{self.ConfigFileName}'
        if not os.path.exists(f'{self.ConfigPath}{ID}'):
            os.makedirs(f'{self.ConfigPath}{ID}')

        try:
            with open(self.UserConfigPath, encoding='utf8') as File:
                self.UserData = json.load(File)
        except FileNotFoundError:
            pass

    def getValue(self, inputType, Key):

        if inputType == Type.System:
            if Key not in self.SystemData:
                return None
            return self.SystemData[Key]
        elif inputType == Type.User:
            if Key not in self.UserData:
                return None
            return self.UserData[Key]

    def setValue(self, inputType, Key, Value):

        if inputType == Type.System:
            if Value is not None:
                self.SystemData[Key] = Value
            elif Key in self.SystemData:
                del self.SystemData[Key]

            with open(self.ConfigFullPath, 'w', encoding='utf8') as File:
                json.dump(self.SystemData, File, indent=4, ensure_ascii=False)

        if inputType == Type.User:
            if Value is not None:
                self.UserData[Key] = Value
            elif Key in self.UserData:
                del self.UserData[Key]

            with open(self.UserConfigPath, 'w', encoding='utf8') as File:
                json.dump(self.UserData, File, indent=4, ensure_ascii=False)