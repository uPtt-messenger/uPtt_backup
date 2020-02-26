from util import sha256


class BlackList:
    def __init__(self, console_obj):
        self.console = console_obj

    def is_black_user(self, ptt_id):
        current_hash_value = sha256(ptt_id)

        return current_hash_value in self.console.dynamic_data.black_list
