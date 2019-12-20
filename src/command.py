

class Command:
    def __init__(self):
        self.login = False
        self.logout = False

        self.PushMsg = []

    def analyze(self, RecvMsg):
        pass

    def push(self, PushMsg):

        self.PushMsg.append(PushMsg)
