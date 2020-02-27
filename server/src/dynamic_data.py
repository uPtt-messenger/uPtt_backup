import json
import urllib.request

import log


class DynamicData:
    def __init__(self):
        log.show(
            'DynamicData',
            log.level.INFO,
            '開始擷取資料'
        )
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

        log.show(
            'DynamicData',
            log.level.INFO,
            '更新資料完成'
        )
