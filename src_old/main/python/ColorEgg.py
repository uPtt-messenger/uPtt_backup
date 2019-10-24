
import hashlib


class Obj():

    List = [
        'bbfa812c4c9c1ec4fcb5a4b2298f6d0c5bc3f5ce86864737367e6973ea4411fa',
    ]

    def __init__(self):
        self._isTarget = False

    def setTarget(self, ID):
        self._ID = ID

        Hash = hashlib.sha256()
        Hash.update(ID.lower().encode('utf-8'))

        HashResult = Hash.hexdigest()
        print(HashResult)

        if HashResult not in self.List:
            print(f'{ID} is not target')
            return
        print(f'{ID} is target')
        self._isTarget = True

    def isTarget(self):
        return self._isTarget


if __name__ == '__main__':
    O = Obj()

    O.setTarget('CodingMan')
