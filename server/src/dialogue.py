# 這是用來處理對話紀錄的
from datetime import datetime
import json

import log
from msg import Msg


class Dialogue:
    def __init__(self, configObj):
        self.config = configObj

        self.dialoglist = dict()

    def addsave(self, target, dictdata):

        self.dialoglist[target].append(dictdata)

        self.config.save_dialogue(
            target,
            self.dialoglist[target]
        )

    def send(self, target, content):

        if target not in self.dialoglist:
            self.dialoglist[target] = []

        msg = Msg()
        msg.add(Msg.key_type, 'send')
        msg.add(Msg.key_ptt_id, target)
        msg.add(Msg.key_content, content)
        # 01/06 16:13
        msg.add(Msg.key_date, datetime.now().strftime('%m/%d %H:%M'))

        self.addsave(target, msg.msg)

    def recv(self, target, content, date):

        if target not in self.dialoglist:
            self.dialoglist[target] = []

        msg = Msg()
        msg.add(Msg.key_type, 'recv')
        msg.add(Msg.key_ptt_id, target)
        msg.add(Msg.key_content, content)
        msg.add(Msg.key_date, date)

        self.addsave(target, msg.msg)

    def loadDialogue(self):

        log.show_value(
            'Dialogue',
            log.level.INFO,
            '載入對話紀錄',
            self.config.dialogfiles
        )

        for fname in self.config.dialogfiles:

            log.show_value(
                'Dialogue',
                log.level.INFO,
                '開啟對話紀錄檔案',
                fname
            )

            pttid = fname[fname.rfind('/') + 1:-4]

            try:
                with open(fname, encoding='utf8') as f:
                    self.dialoglist[pttid] = json.load(f)
            except Exception as e:

                log.show(
                    'Dialogue',
                    log.level.INFO,
                    e.__traceback__.__str__()
                )
                log.show(
                    'Dialogue',
                    log.level.INFO,
                    e.__str__()
                )

                log.show(
                    'Dialogue',
                    log.level.INFO,
                    f'無法讀取 {fname}'
                )
                continue

        log.show(
            'Dialogue',
            log.level.INFO,
            '載入對話紀錄完成'
        )

        # print(
        #     json.dumps(self.dialoglist, indent=4, ensure_ascii=False)
        # )
