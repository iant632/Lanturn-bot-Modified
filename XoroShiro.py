class XoroShiro:
    def __init__(self, seed):
        self.s0 = seed
        self.s1 = 0x82A2B175229D6A5B

    @staticmethod
    def rotl(x, k):
        return ((x << k) | (x >> (64 - k))) & 0xFFFFFFFFFFFFFFFF

    def next(self):
        result = (self.s0 + self.s1) & 0xFFFFFFFFFFFFFFFF

        self.s1 ^= self.s0
        self.s0 = self.rotl(self.s0, 24) ^ self.s1 ^ ((self.s1 << 16) & 0xFFFFFFFFFFFFFFFF)
        self.s1 = self.rotl(self.s1, 37)

        return result
        
    def nextInt(self, value, mask):
        result = self.next() & mask
        while result >= value:
            result = self.next() & mask
        return result

    def reset(self, seed):
    	self.s0 = seed
    	self.s1 = 0x82A2B175229D6A5B