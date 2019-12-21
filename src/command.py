
import json

from errorcode import ErrorCode

Key_Opt = 'operation'
Key_Msg = 'msg'
Key_Code = 'code'


class Command:
    def __init__(self):
        self.login = False
        self.logout = False

        self.PushMsg = []

    def analyze(self, RecvMsg: str):
        Msg = json.loads(RecvMsg)

        if Msg[Key_Opt] == 'echo':

            ResMsg = dict()
            ResMsg[Key_Code] = ErrorCode.Success
            ResMsg[Key_Msg] = Msg[Key_Msg]

            self.PushMsg.append(
                json.dumps(ResMsg)
            )

    def push(self, PushMsg):

        self.PushMsg.append(PushMsg)
