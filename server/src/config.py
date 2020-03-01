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
    update_cycle = 180
    port = 50732
    ptt_log_handler = None
    ptt_log_level = log.level.INFO

    feedback_port = 57983
    feedback_frequency = 60

    def __init__(self):

        # 不想給使用者改的設定值就寫在這兒
        # 想給使用者改的就透過 setValue
        # 因為會被存起來

        self.config_file_name = 'config.txt'
        self.friend_file_name = 'friend.txt'

        self.config_path = None

        if os.name == 'nt':
            log.show_value(
                'Config',
                log.level.INFO,
                '作業系統',
                'Windows'
            )
            self.config_path = 'C:/ProgramData/uPtt'

        self.user_config_path = None

        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path)

        self.user_data = dict()
        self.id = None

        log.show_value(
            'Config',
            log.level.INFO,
            '設定檔',
            '初始化'
        )

    def init_user(self, ptt_id):
        log.show_value(
            'Config',
            log.level.INFO,
            '使用者空間初始化',
            ptt_id
        )
        self.id = ptt_id
        self.user_config_path = f'{self.config_path}/{ptt_id}/{self.config_file_name}'
        if not os.path.exists(f'{self.config_path}/{ptt_id}'):
            os.makedirs(f'{self.config_path}/{ptt_id}')

            # init user config here

        log.show_value(
            'Config',
            log.level.INFO,
            '使用者設定初始化',
            ptt_id
        )

        try:
            with open(self.user_config_path, encoding='utf8') as File:
                self.user_data = json.load(File)
        except FileNotFoundError:
            pass

    def get_value(self, key):

        if key not in self.user_data:
            return None
        return self.user_data[key]

    def set_value(self, key, value):

        if value is not None:
            self.user_data[key] = value
        elif key in self.user_data:
            del self.user_data[key]

        with open(self.user_config_path, 'w', encoding='utf8') as File:
            json.dump(self.user_data, File, indent=4, ensure_ascii=False)

