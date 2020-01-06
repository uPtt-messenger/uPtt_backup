# 這是用來處理對話紀錄的
from datetime import date

from msg import Msg


class Dialogue:
    def __init__(self, configObj):
        self.config = configObj

        self.dialoglist = dict()

    def addsave(self, target, dictdata):

        self.dialoglist[target].append(dictdata)

        self.config.saveDialogue(
            target,
            self.dialoglist[target]
        )

    def send(self, target, content):

        if target not in self.dialoglist:
            self.dialoglist[target] = []

        msg = Msg()
        msg[Msg.Key_Type] = 'send'
        msg[Msg.Key_PttID] = target
        msg[Msg.Key_Content] = content

        # 01/06 16:13

        msg[Msg.Key_Date] = date.today().strftime('%m/%d %H:%M')

        self.addsave(target, msg.Dict)

    def recv(self, target, content, date):

        if target not in self.dialoglist:
            self.dialoglist[target] = []

        msg = Msg()
        msg[Msg.Key_Type] = 'recv'
        msg[Msg.Key_PttID] = target
        msg[Msg.Key_Content] = content
        msg[Msg.Key_Date] = date

        self.addsave(target, msg.Dict)
