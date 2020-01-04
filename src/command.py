
import json

from errorcode import ErrorCode
from msg import Msg


class Command:
    def __init__(self):
        self.login = False
        self.logout = False

        self.PushMsg = []

        self.loginid = None
        self.loginpassword = None
        self.logout = False
        self.close = False
        self.sendWBid = None
        self.sendWBcontent = None

    def analyze(self, RecvMsgStr: str):
        RecvMsg = Msg(strobj=RecvMsgStr)

        Opt = RecvMsg.get(Msg.Key_Opt)
        if Opt == 'echo':
            ResMsg = Msg(ErrorCode.Success, RecvMsg.get(Msg.Key_Msg))
            self.push(ResMsg)

        elif Opt == 'login':
            self.loginid = RecvMsg.get(Msg.Key_Payload)[Msg.Key_PttID]
            self.loginpassword = RecvMsg.get(Msg.Key_Payload)[
                Msg.Key_PttPassword]

        elif Opt == 'logout':
            self.logout = True

        elif Opt == 'close':
            self.close = True

        elif Opt == 'sendwaterball':
            self.sendWBid = RecvMsg.get(Msg.Key_Payload)[Msg.Key_PttID]
            self.sendWBcontent = RecvMsg.get(Msg.Key_Payload)[Msg.Key_Content]
        else:
            ResMsg = Msg(ErrorCode.Unsupport, 'Unsupported')
            self.push(ResMsg)

    def push(self, PushMsg):

        self.PushMsg.append(PushMsg.__str__())

    def recvlogin(self):
        TempID, TempPW = self.loginid, self.loginpassword
        self.loginid, self.loginpassword = None, None
        return TempID, TempPW

    def recvlogout(self):
        if self.logout:
            self.logout = False
            return True
        return False

    def sendWaterBall(self):
        TempID, TempContent = self.sendWBid, self.sendWBcontent
        self.sendWBid, self.sendWBcontent = None, None
        return TempID, TempContent
