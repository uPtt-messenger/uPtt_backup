from errorcode import error_code
from msg import Msg
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
            current_res_msg = Msg(
                operate=opt,
                code=error_code.Success,
                msg=recv_msg.get(Msg.key_msg)
            )
            self.push(current_res_msg)

        elif opt == 'login':
            ptt_id = recv_msg.get(Msg.key_payload)[Msg.key_ptt_id]
            ptt_pass = recv_msg.get(Msg.key_payload)[
                Msg.key_ptt_pass]

            log.show(
                'command',
                log.level.INFO,
                '執行登入程序'
            )

            res_msg = None
            for e in self.event.login:
                current_res_msg = e(ptt_id, ptt_pass)
                if current_res_msg is None:
                    continue
                if current_res_msg.get(Msg.key_code) != error_code.Success:
                    self.push(current_res_msg)
                    log.show(
                        'command',
                        log.level.INFO,
                        '登入程序中斷'
                    )
                    return
                res_msg = current_res_msg
            self.push(res_msg)

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
            current_res_msg = Msg(
                operate=opt,
                code=error_code.Unsupported,
                msg='Unsupported'
            )
            self.push(current_res_msg)

    def push(self, push_msg):
        self.PushMsg.append(push_msg.__str__())
