
import json


class Msg:

    # 此處的 Key 是跟前端介接的，變數則命名成我習慣的樣子

    Key_Opt = 'operation'
    Key_Msg = 'msg'
    Key_Code = 'code'
    Key_Payload = 'payload'
    Key_PttID = 'pttId'
    Key_PttPassword = 'pwd'

    def __init__(self, code=None, msg=None, strobj=None):

        self.Dict = dict()

        if code is not None:
            self.add(self.Key_Code, code)
            self.add(self.Key_Msg, msg)
        else:
            self.Dict = json.loads(strobj)

    def add(self, key, value):
        self.Dict[key] = value

    def remove(self, key):
        del self.Dict[key]

    def __str__(self):
        return json.dumps(self.Dict, ensure_ascii=False)

    def get(self, key):
        if key not in self.Dict:
            return None
        return self.Dict[key]
