import log


class FriendList:
    def __init__(self):
        self.friendlist = []

    def add(self, target):
        self.friendlist.append(target)

    def remove(self, target):
        if target in self.friendlist:
            self.friendlist.remove(target)
