
import json

from errorcode import ErrorCode

Key_Opt = 'operation'
Key_Msg = 'msg'
Key_Code = 'code'
Key_Payload = 'payload'
Key_PttID = 'pttId'
Key_PttPassword = 'pwd'


class Command:
    def __init__(self):
        self.login = False
        self.logout = False

        self.PushMsg = []

        self.ID, self.Password = None, None

    def analyze(self, RecvMsg: str):
        Msg = json.loads(RecvMsg)

        if Msg[Key_Opt] == 'echo':

            ResMsg = dict()
            ResMsg[Key_Code] = ErrorCode.Success
            ResMsg[Key_Msg] = Msg[Key_Msg]

            self.PushMsg.append(
                json.dumps(ResMsg)
            )
        elif Msg[Key_Opt] == 'login':
            self.ID = Msg[Key_Payload][Key_PttID]
            self.Password = Msg[Key_Payload][Key_PttPassword]

    def push(self, PushMsg):

        self.PushMsg.append(PushMsg)

    def recvlogin(self):
        TempID, TempPW = self.ID, self.Password
        self.ID, self.Password = None, None
        return TempID, TempPW
