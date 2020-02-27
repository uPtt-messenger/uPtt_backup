from errorcode import error_code
from msg import Msg
from black_list import is_black_user
import log


class Command:
    def __init__(self, event_console, dynamic_data_obj):
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

        self.event = event_console
        self.dynamic_data = dynamic_data_obj

    def analyze(self, recv_msg: Msg):

        opt = recv_msg.get(Msg.key_opt)
        if opt == 'echo':
            res_msg = Msg(
                operate=opt,
                code=error_code.Success,
                msg=recv_msg.get(Msg.key_msg)
            )
            self.push(res_msg)

        elif opt == 'login':
            ptt_id = recv_msg.get(Msg.key_payload)[Msg.key_ptt_id]
            ptt_pass = recv_msg.get(Msg.key_payload)[
                Msg.key_ptt_pass]

            if is_black_user(self.dynamic_data, ptt_id):
                log.show_value(
                    'command',
                    log.level.INFO,
                    '黑名單',
                    ptt_id
                )

                res_msg = Msg(
                    operate=opt,
                    code=error_code.BlackList,
                    msg='黑名單使用者'
                )
                self.push(res_msg)
                return

            log.show(
                'command',
                log.level.INFO,
                '執行登入程序'
            )

            for e in self.event.login:
                e(ptt_id, ptt_pass)

            log.show(
                'command',
                log.level.INFO,
                '登入程序全數完成'
            )

        elif opt == 'logout':
            log.show(
                'command',
                log.level.INFO,
                '執行登出程序'
            )

            for e in self.event.logout:
                e()

            log.show(
                'command',
                log.level.INFO,
                '登出程序全數完成'
            )

        elif opt == 'close':
            log.show(
                'command',
                log.level.INFO,
                '執行終止程序'
            )
            for e in self.event.close:
                e()
            log.show(
                'command',
                log.level.INFO,
                '終止程序全數完成'
            )

        elif opt == 'sendwaterball':
            waterball_id = recv_msg.get(Msg.key_payload)[Msg.key_ptt_id]
            waterball_content = recv_msg.get(Msg.key_payload)[Msg.key_content]

            log.show(
                'command',
                log.level.INFO,
                '執行丟水球程序'
            )
            for e in self.event.send_waterball:
                e(waterball_id, waterball_content)
            log.show(
                'command',
                log.level.INFO,
                '丟水球程序全數完成'
            )

        elif opt == 'addfriend':
            self.add_friend_id = recv_msg.get(Msg.key_payload)[Msg.key_ptt_id]

        else:
            res_msg = Msg(
                operate=opt,
                code=error_code.Unsupported,
                msg='Unsupported'
            )
            self.push(res_msg)

    def push(self, push_msg):
        self.PushMsg.append(push_msg.__str__())
