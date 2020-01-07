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

        print('5', json.dumps(self.dialoglist, indent=4, ensure_ascii=False))
        self.dialoglist[target].append(dictdata)
        print('4', json.dumps(self.dialoglist, indent=4, ensure_ascii=False))

        self.config.saveDialogue(
            target,
            self.dialoglist[target]
        )

    def send(self, target, content):

        print('1', json.dumps(self.dialoglist, indent=4, ensure_ascii=False))

        if target not in self.dialoglist:
            self.dialoglist[target] = []

        print('2', json.dumps(self.dialoglist, indent=4, ensure_ascii=False))

        msg = Msg()
        msg.add(Msg.Key_Type, 'send')
        msg.add(Msg.Key_PttID, target)
        msg.add(Msg.Key_Content, content)
        # 01/06 16:13
        msg.add(Msg.Key_Date, datetime.now().strftime('%m/%d %H:%M'))

        self.addsave(target, msg.Dict)

    def recv(self, target, content, date):

        if target not in self.dialoglist:
            self.dialoglist[target] = []

        msg = Msg()
        msg.add(Msg.Key_Type, 'recv')
        msg.add(Msg.Key_PttID, target)
        msg.add(Msg.Key_Content, content)
        msg.add(Msg.Key_Date, date)

        self.addsave(target, msg.Dict)

    def loadDialogue(self):

        log.showvalue(
            'Dialogue',
            log.Level.INFO,
            '載入對話紀錄',
            self.config.dialogfiles
        )

        for fname in self.config.dialogfiles:

            log.showvalue(
                'Dialogue',
                log.Level.INFO,
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
                    log.Level.INFO,
                    e.__traceback__.__str__()
                )
                log.show(
                    'Dialogue',
                    log.Level.INFO,
                    e.__str__()
                )

                log.show(
                    'Dialogue',
                    log.Level.INFO,
                    f'無法讀取 {fname}'
                )
                continue

        log.show(
            'Dialogue',
            log.Level.INFO,
            '載入對話紀錄完成'
        )

        print(
            json.dumps(self.dialoglist, indent=4, ensure_ascii=False)
        )
