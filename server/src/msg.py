
import json


class Msg:

    # 此處的 Key 是跟前端介接的，變數則命名成我習慣的樣子

    key_opt: str = 'operation'
    key_login = 'login'
    key_logout = 'logout'
    key_sendwaterball = 'sendwaterball'
    key_recvwaterball = 'recvwaterball'
    key_msg = 'msg'
    key_code = 'code'
    key_payload = 'payload'
    key_ptt_id = 'pttId'
    key_ptt_pass = 'pwd'
    key_content = 'content'
    key_date = 'date'
    key_type = 'type'
    key_timestamp = 'timestamp'
    key_notify = 'notify'
    key_token = 'token'

    def __init__(self, operate=None, code=None, msg=None, strobj=None):

        self.Dict = dict()

        if operate is not None:
            self.add(self.key_opt, operate)

        if code is not None:
            self.add(self.key_code, code)
            self.add(self.key_msg, msg)

        if strobj is not None:
            self.Dict = json.loads(strobj)

    def add(self, key, value):

        if isinstance(value, Msg):
            value = value.Dict

        self.Dict[key] = value

    def remove(self, key):
        del self.Dict[key]

    def __str__(self):
        return json.dumps(self.Dict, ensure_ascii=False)

    def get(self, key):
        if key not in self.Dict:
            return None
        return self.Dict[key]
