import os
from os import walk
from datetime import datetime
import json

import log
from msg import Msg


class Dialogue:
    def __init__(self, console_obj):
        self.console = console_obj
        self.path = f'{self.console.config.config_path}/{self.console.ptt_id}/dialogue'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.data = dict()

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
            log.show(
                'Dialogue',
                log.level.INFO,
                '載入對話紀錄',
                dialogue_file
            )

            with open(dialogue_file, 'r') as fp:
                all_lines = fp.readlines()

            if not all_lines:
                continue

            target_id = dialogue_file[:-4]

            for line in all_lines:
                current_msg = Msg(strobj=line)

                if target_id not in self.data:
                    self.data[target_id] = []

                self.data[target_id].append(current_msg)

        log.show(
            'Dialogue',
            log.level.INFO,
            '對話紀錄載入完成'
        )

    def save(self, target_id, current_msg: Msg):
        if target_id not in self.data:
            self.data[target_id] = []

        self.data[target_id].append(current_msg)

        file_name = f'{target_id}.txt'

        with open(file_name, 'a') as fp:
            fp.write(str(current_msg) + '\n')






