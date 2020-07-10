import random


class Protocol(object):

    def __init__(self):
        self.package = []
        self.header = 0x00

    def __new__(cls, *args, **kw):
        '''
        启用单例模式
        :param args:
        :param kw:
        :return:
        '''
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def get_lsb(self, bytes):
        lsb = int.from_bytes(bytes[1:5], 'big')
        lsb = random.randint(1, 1000)
        #print("## lsb = %d" % lsb)
        return lsb

    def get_msb(self, bytes):
        msb = int.from_bytes(bytes[6:10], 'big')
        msb = random.randint(1, 1000)
        #print("## lsb = %d" % msb)
        return msb

    def get_dev_code(self, bytes):
        return "12345678"
