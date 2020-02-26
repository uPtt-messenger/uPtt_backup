import os
from os import listdir
from os.path import isfile, join
import json

import log

LogPath = None


class Type:
    System = 1
    User = 2


class Config:
    version = '0.0.1'
    quick_response_time = 0.05
    query_cycle = 3.0 + quick_response_time
    port = 50732
    ptt_log_handler = None
    ptt_log_level = log.level.INFO

    feedback_port = 57983
    feedback_frequency = 60

    def __init__(self):

        # 不想給使用者改的設定值就寫在這兒
        # 想給使用者改的就透過 setValue
        # 因為會被存起來

        self.ConfigFileName = 'config.txt'
        self.FriendFileName = 'friend.txt'

        self.ConfigPath = None
        self.friendlist = None

        if os.name == 'nt':
            log.show_value(
                'Config',
                log.level.INFO,
                '作業系統',
                'Windows'
            )
            self.ConfigPath = 'C:/ProgramData/uPtt'

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

        log.show_value(
            'Config',
            log.level.INFO,
            '設定檔',
            '初始化'
        )

    def init_user(self, ptt_id):
        self.id = ptt_id
        self.UserConfigPath = f'{self.ConfigPath}/{ptt_id}/{self.ConfigFileName}'
        if not os.path.exists(f'{self.ConfigPath}/{ptt_id}'):
            os.makedirs(f'{self.ConfigPath}/{ptt_id}')
        else:
            if os.path.exists(f'{self.ConfigPath}/{self.id}/dialogue/'):
                dialogpath = f'{self.ConfigPath}/{self.id}/dialogue/'
                self.dialogfiles = [join(dialogpath, f) for f in listdir(
                    dialogpath) if isfile(join(dialogpath, f))]

                self.dialogfiles = [
                    x for x in self.dialogfiles if x.endswith('.txt')]

                log.show_value(
                    'Config',
                    log.level.INFO,
                    '對話紀錄檔案',
                    self.dialogfiles
                )

            fname = f'{self.ConfigPath}/{self.id}/{self.FriendFileName}'
            if os.path.exists(fname):
                log.show_value(
                    'Config',
                    log.level.INFO,
                    '載入朋友清單',
                    self.dialogfiles
                )

                try:
                    with open(fname, encoding='utf8') as f:
                        self.friendlist = json.load(f)
                except Exception as e:

                    log.show(
                        'Config',
                        log.level.INFO,
                        e.__traceback__.__str__()
                    )
                    log.show(
                        'Config',
                        log.level.INFO,
                        e.__str__()
                    )

                    log.show(
                        'Config',
                        log.level.INFO,
                        f'無法讀取 {fname}'
                    )
                    self.friendlist = None

        try:
            with open(self.UserConfigPath, encoding='utf8') as File:
                self.UserData = json.load(File)
        except FileNotFoundError:
            pass

    def get_value(self, input_type, key):

        if input_type == Type.System:
            if key not in self.SystemData:
                return None
            return self.SystemData[key]
        elif input_type == Type.User:
            if key not in self.UserData:
                return None
            return self.UserData[key]

    def set_value(self, input_type, key, value):

        if input_type == Type.System:
            if value is not None:
                self.SystemData[key] = value
            elif key in self.SystemData:
                del self.SystemData[key]

            with open(self.ConfigFullPath, 'w', encoding='utf8') as File:
                json.dump(self.SystemData, File, indent=4, ensure_ascii=False)

        if input_type == Type.User:
            if value is not None:
                self.UserData[key] = value
            elif key in self.UserData:
                del self.UserData[key]

            with open(self.UserConfigPath, 'w', encoding='utf8') as File:
                json.dump(self.UserData, File, indent=4, ensure_ascii=False)

    def save_dialogue(self, target, msg_list):
        filepath = f'{self.ConfigPath}/{self.id}/dialogue/{target}.txt'
        if not os.path.exists(f'{self.ConfigPath}/{self.id}/dialogue/'):
            os.makedirs(f'{self.ConfigPath}/{self.id}/dialogue/')

        with open(filepath, 'w', encoding='utf8') as f:
            json.dump(
                msg_list,
                f,
                indent=4,
                ensure_ascii=False
            )
