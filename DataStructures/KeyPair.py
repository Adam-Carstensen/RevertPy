
class KeyPair(object):
    def __init__(self, keyone, keytwo):
        self.keyone = keyone
        self.keytwo = keytwo

    def __eq__(self, obj: object) -> bool:
        return isinstance(obj, KeyPair) and obj.keyone == self.keyone and obj.keytwo == self.keytwo

    def __hash__(self) -> int:
        return hash(self.keyone) ^ hash(self.keytwo)
