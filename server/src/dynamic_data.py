import json
import urllib.request
import threading
import time

import log


class DynamicData:
    def __init__(self, console_obj):
        self.console = console_obj
        self.console.event.close.append(self.event_close)

        self.run_update = True

        self.update()

        self.update_thread = threading.Thread(
            target=self.run,
            daemon=True)

        self.update_thread.start()

    def event_close(self):

        log.show(
            'DynamicData',
            log.level.INFO,
            '執行終止程序'
        )

        self.run_update = False
        self.update_thread.join()

        log.show(
            'DynamicData',
            log.level.INFO,
            '終止程序完成'
        )

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
            '開始更新資料'
        )
        with urllib.request.urlopen(
                "https://raw.githubusercontent.com/PttCodingMan/uPtt_open_data/master/open_data.json") as url:
            self.data = json.loads(url.read().decode())

        log.show(
            'DynamicData',
            log.level.INFO,
            '更新資料完成'
        )

        self.version = self.data['version']
        self.tag_list = self.data['tag']
        self.black_list = self.data['black_list']
        self.announce = self.data['announce']

        log.show_value(
            'DynamicData',
            log.level.INFO,
            '發布版本',
            self.version
        )

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
                '無黑名單'
            )


    def update_tag(self):
        with urllib.request.urlopen(
                "https://raw.githubusercontent.com/PttCodingMan/uPtt_open_data/master/tag/tag.json") as url:
            self.tag_data = json.loads(url.read().decode())

        log.show(
            'DynamicData',
            log.level.INFO,
            '擷取稱號資料完成'
        )

        for _, (hash_value, tag) in enumerate(self.tag_data.items()):
            if hash_value.startswith('//'):
                continue
            if len(hash_value) != 64:
                continue
            log.show_value(
                'DynamicData',
                log.level.INFO,
                'tag',
                tag
            )

    def update_black_list(self):
        with urllib.request.urlopen(
                "https://raw.githubusercontent.com/PttCodingMan/uPtt_open_data/master/list/blacklist.json") as url:
            self.black_list = json.loads(url.read().decode())

        log.show(
            'DynamicData',
            log.level.INFO,
            '擷取黑名單資料完成'
        )

        for block_user in self.black_list['black_list']:
            if block_user.startswith('//'):
                continue
            log.show_value(
                'DynamicData',
                log.level.INFO,
                'block_user',
                block_user
            )
