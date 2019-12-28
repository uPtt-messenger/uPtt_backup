
import json

from errorcode import ErrorCode
from msg import Msg


class Command:
    def __init__(self):
        self.login = False
        self.logout = False

        self.PushMsg = []

        self.ID, self.Password = None, None
        self.logout = False

    def analyze(self, RecvMsgStr: str):
        RecvMsg = Msg(strobj=RecvMsgStr)

        Opt = RecvMsg.get(Msg.Key_Opt)
        if Opt == 'echo':

            ResMsg = Msg(ErrorCode.Success, RecvMsg.get(Msg.Key_Msg))
            self.push(ResMsg)

        elif Opt == 'login':
            self.ID = RecvMsg.get(Msg.Key_Payload)[Msg.Key_PttID]
            self.Password = RecvMsg.get(Msg.Key_Payload)[Msg.Key_PttPassword]

        elif Opt == 'logout':
            self.logout = True

    def push(self, PushMsg):

        self.PushMsg.append(PushMsg.__str__())

    def recvlogin(self):
        TempID, TempPW = self.ID, self.Password
        self.ID, self.Password = None, None
        return TempID, TempPW

    def recvlogout(self):
        if self.logout:
            self.logout = False
            return True
        return False
