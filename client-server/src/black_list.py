from util import sha256
from msg import Msg
from errorcode import error_code
import log


class BlackList:
    def __init__(self, console_boj):
        self.console = console_boj

        self.console.event.login.append(self.event_login)

    def event_login(self, ptt_id, ptt_pw):
        if self.is_black_user(ptt_id):
            log.show_value(
                'command',
                log.level.INFO,
                '黑名單',
                ptt_id
            )

            block_msg = Msg(
                operate=Msg.key_login,
                code=error_code.BlackList,
                msg='黑名單使用者'
            )
            return block_msg
        return None

    def is_black_user(self, ptt_id):
        current_hash_value = sha256(ptt_id)

        return current_hash_value in self.console.dynamic_data.black_list
