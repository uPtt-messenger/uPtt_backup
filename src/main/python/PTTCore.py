import PTTLibrary
from PTTLibrary import PTT


class Core(object):
    def __init__(self, ID, PW):
        self._ID = ID
        self._PW = PW
    
        PTTBot = PTT.Library()
        try:
            PTTBot.login(ID, Password)
        except PTT.Exceptions.LoginError:
            PTTBot.log('登入失敗')
        PTTBot.log('登入成功')