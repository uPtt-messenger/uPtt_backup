import os
from os import walk
# from datetime import datetime
# import json

import log
from msg import Msg
from config import Config
import rijndael

class Dialogue:
    def __init__(self, console_obj):
        self.console = console_obj
        self.path = f'{self.console.config.config_path}/{self.console.ptt_id}/dialogue'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        else:
            self.data = dict()

            aes_key = self.console.config.get_value(Config.key_aes_key)

            log.show(
                'Dialogue',
                log.level.INFO,
                '載入對話紀錄'
            )

            dialogue_file_list = []
            for (dirpath, dirnames, filenames) in walk(self.path):
                dialogue_file_list.extend(filenames)
                break

            dialogue_file_list = [x for x in dialogue_file_list if x.endswith('.txt')]

            for dialogue_file in dialogue_file_list:
                log.show_value(
                    'Dialogue',
                    log.level.INFO,
                    '載入對話紀錄',
                    dialogue_file
                )

                current_path = f'{self.path}/{dialogue_file}'
                with open(current_path, 'r') as fp:
                    all_lines = fp.readlines()

                if not all_lines:
                    continue

                target_id = dialogue_file[:-4]

                for line in all_lines:
                    # print(line)
                    current_msg = Msg(strobj=line)
                    print(current_msg)

                    if target_id not in self.data:
                        self.data[target_id] = []

                    self.data[target_id].append(current_msg)

            log.show(
                'Dialogue',
                log.level.INFO,
                '對話紀錄載入完成'
            )

    def save(self, current_msg: Msg):
        target_id = current_msg.get(Msg.key_ptt_id)

        log.show_value(
            'Dialogue',
            log.level.INFO,
            '儲存對話紀錄',
            target_id
        )
        if target_id not in self.data:
            self.data[target_id] = []

        self.data[target_id].append(current_msg)

        file_name = f'{target_id}.txt'
        current_path = f'{self.path}/{file_name}'

        aes_key = self.console.config.get_value(Config.key_aes_key)
        if aes_key is None:
            aes_key = rijndael.gen_key()
            self.console.config.set_value(Config.key_aes_key, aes_key)
        # print(aes_key)

        with open(current_path, 'a') as fp:
            fp.write(str(current_msg) + '\n')

    def get(self, target_id: str, count: int, index: int = 0):
        if target_id not in self.data:
            return []
        if count == 0:
            return []
        if index == 0:
            return self.data[target_id][-count:]

        if index >= len(self.data[target_id]):
            return []

        current_data = self.data[target_id][:(index + 1)]
        return current_data[-count:]
