
from errorcode import ErrorCode
from msg import Msg


class Command:
    def __init__(self):
        self.login = False
        self.logout = False

        self.PushMsg = []

        self.login_id = None
        self.login_password = None
        self.logout = False
        self.close = False
        self.send_waterball_id = None
        self.send_waterball_content = None
        self.add_friend_id = None

    def analyze(self, recv_msg: Msg):

        opt = recv_msg.get(Msg.Key_Opt)
        if opt == 'echo':
            res_msg = Msg(ErrorCode.Success, recv_msg.get(Msg.Key_Msg))
            self.push(res_msg)

        elif opt == 'login':
            self.login_id = recv_msg.get(Msg.Key_Payload)[Msg.Key_PttID]
            self.login_password = recv_msg.get(Msg.Key_Payload)[
                Msg.Key_PttPassword]

        elif opt == 'logout':
            self.logout = True

        elif opt == 'close':
            self.close = True

        elif opt == 'sendwaterball':
            self.send_waterball_id = recv_msg.get(Msg.Key_Payload)[Msg.Key_PttID]
            self.send_waterball_content = recv_msg.get(Msg.Key_Payload)[Msg.Key_Content]

        elif opt == 'addfriend':
            self.add_friend_id = recv_msg.get(Msg.Key_Payload)[Msg.Key_PttID]

        else:
            res_msg = Msg(ErrorCode.Unsupport, 'Unsupported')
            self.push(res_msg)

    def push(self, push_msg):

        self.PushMsg.append(push_msg.__str__())

    def recvlogin(self):
        temp_id, temp_pw = self.login_id, self.login_password
        self.login_id, self.login_password = None, None
        return temp_id, temp_pw

    def recvlogout(self):
        if self.logout:
            self.logout = False
            return True
        return False

    def sendWaterBall(self):
        temp_id, temp_content = self.send_waterball_id, self.send_waterball_content
        self.send_waterball_id, self.send_waterball_content = None, None
        return temp_id, temp_content

    def addfriend(self):
        temp = self.add_friend_id
        self.add_friend_id = None
        return temp
