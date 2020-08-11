import json
import threading
import time
import urllib.request

import log
from config import Config


class DynamicData:
    def __init__(self, console_obj, run=True):
        self.console = console_obj
        self.console.event.close.append(self.event_close)

        self.run_update = True

        self.update()

        if run:
            self.update_thread = threading.Thread(
                target=self.run,
                daemon=True)

            self.update_thread.start()

    def event_close(self):

        log.show(
            'DynamicData',
            log.level.INFO,
            '執行終止程序')

        self.run_update = False
        self.update_thread.join()

        log.show(
            'DynamicData',
            log.level.INFO,
            '終止程序完成')

    def run(self):

        while self.run_update:
            start_time = end_time = time.time()
            while end_time - start_time < self.console.config.update_cycle:
                time.sleep(self.console.config.quick_response_time)
                end_time = time.time()
                if not self.run_update:
                    break
            if not self.run_update:
                break
            self.update()

    def update(self):
        log.show(
            'DynamicData',
            log.level.INFO,
            '開始更新資料')

        if self.console.run_mode == 'dev':
            update_url = 'https://raw.githubusercontent.com/PttCodingMan/uPtt/develop/data/open_data.json'
        elif self.console.run_mode == 'release':
            update_url = 'https://raw.githubusercontent.com/PttCodingMan/uPtt/master/data/open_data.json'
        with urllib.request.urlopen(update_url) as url:
            self.data = json.loads(url.read().decode())

        log.show(
            'DynamicData',
            log.level.INFO,
            '更新資料完成'
        )

        self.console.config.set_value(Config.level_USER, Config.key_version, self.data['version'])

        self.version = self.data['version']
        self.tag_list = self.data['tag']
        self.black_list = self.data['black_list']
        self.announce = self.data['announce']
        self.online_server = self.data['online_server']

        log.show_value(
            'DynamicData',
            log.level.INFO,
            '發布版本',
            self.version)

        del_key_list = []
        for _, (hash_value, tag) in enumerate(self.tag_list.items()):
            if hash_value.startswith('//'):
                del_key_list.append(hash_value)
                continue
            if len(hash_value) != 64:
                del_key_list.append(hash_value)
                continue

        for del_key in del_key_list:
            del self.tag_list[del_key]

        for _, (hash_value, tag) in enumerate(self.tag_list.items()):
            log.show_value(
                'DynamicData',
                log.level.INFO,
                'tag',
                tag
            )

        if self.black_list:
            for block_user in self.black_list:
                log.show_value(
                    'DynamicData',
                    log.level.INFO,
                    'block_user',
                    block_user
                )
        else:
            log.show(
                'DynamicData',
                log.level.INFO,
                '無黑名單')

        log.show_value(
            'DynamicData',
            log.level.INFO,
            'online_server',
            self.online_server)
