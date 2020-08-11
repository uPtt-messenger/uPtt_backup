import os
from os import walk
# from datetime import datetime
# import json

import log
from msg import Msg
from config import Config
import aes


class Dialogue:
    def __init__(self, console_obj):
        self.console = console_obj
        self.path = f'{self.console.config.config_path}/{self.console.ptt_id}/dialogue'
        self.data = dict()

        if not os.path.exists(self.path):
            os.makedirs(self.path)
            self.aes_key = None
        else:
            self.aes_key = self.console.config.get_value(Config.level_USER, Config.key_aes_key)

            log.show_value(
                'Dialogue',
                log.level.DEBUG,
                '載入金鑰',
                self.aes_key
            )

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

                    if target_id not in self.data:
                        self.data[target_id] = []

                    # print(current_msg)
                    if current_msg.data[Msg.key_api_version] == 1:
                        cipher_msg_str = current_msg.data[Msg.key_cipher_msg]
                        # print(cipher_msg_str)
                        cipher_msg = Msg(dictobj=cipher_msg_str)
                        # print(cipher_msg)

                        decrypt_data = aes.decrypt(self.aes_key, cipher_msg)
                        decrypt_msg = Msg(strobj=decrypt_data)

                    log.show_value(
                        'Dialogue',
                        log.level.DEBUG,
                        '解密對話',
                        decrypt_msg
                    )
                    self.data[target_id].append(decrypt_msg)

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

        if self.aes_key is None:
            self.aes_key = self.console.config.get_value(Config.level_USER, Config.key_aes_key)
            if self.aes_key is None:
                self.aes_key = aes.gen_key()
                self.console.config.set_value(Config.level_USER, Config.key_aes_key, self.aes_key)

        encrypt_msg = aes.encrypt(self.aes_key, str(current_msg))

        restore_msg = Msg()
        restore_msg.add(Msg.key_api_version, 1)
        restore_msg.add(Msg.key_cipher_msg, encrypt_msg)

        with open(current_path, 'a') as fp:
            fp.write(str(restore_msg) + '\n')

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
