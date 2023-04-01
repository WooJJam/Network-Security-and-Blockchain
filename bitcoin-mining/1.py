from bitmap import BitMap
from hashlib import sha256

class BloomFilter:
    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.n = 0
        self.bf = BitMap(m)
        
    def getPositions(self, item):
        positions = []
        for i in range(1, self.k+1):
            sha = sha256((item + str(i)).encode('utf-8')).hexdigest()
            position = int(sha, 16) % self.m
            positions.append(position)
        return positions
    
    def add(self, item):
        positions = self.getPositions(item)
        for pos in positions:
            self.bf.set(pos)
        self.n += 1
    
    def contains(self, item):
        positions = self.getPositions(item)
        for pos in positions:
            if not self.bf.test(pos):
                return False
        return True
    
    def reset(self):
        self.bf.reset()
        self.n = 0
        
    def __repr__(self):
        ones = self.bf.count()
        return "M = {}, F = {}\nBitMap = {}\n항목의 수 = {}, 1인 비트수 = {}\n".format(
            self.m, self.k, str(self.bf), self.n, ones)

if __name__ == "__main__":
    bf = BloomFilter(53, 3)
    for ch in "AEIOU":
        bf.add(ch)
    print(bf)
    for ch in "ABCDEFGHIJ":
        print(ch, bf.contains(ch))
