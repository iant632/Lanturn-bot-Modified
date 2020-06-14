import struct

storedSize = 0x148
blockSize = 80

class PK8:
    def __init__(self, data):
        self.data = data

    def checkEncrypted(self):
        return self.data[0x70] != 0 and self.data[0xC0] != 0

    def getEncryptionConstant(self):
        return int(struct.unpack("I", bytes(self.data[0:4]))[0]) & 0xFFFFFFFF

    def advance(self, seed):
        return seed * 0x41C64E6D + 0x6073

    def Crypt(self):
        pkmWord = None
        seed = self.getEncryptionConstant()

        i = 8
        while i < storedSize:
            seed = self.advance(seed)
            pkmWord = (self.data[i + 1] << 8) | self.data[i]
            pkmWord = pkmWord ^ (seed >> 16)
            self.data[i + 1] = ((pkmWord & 0xFF00) >> 8) & 0xFF
            self.data[i] = pkmWord & 0xFF
            i += 2

    def getData(self):
        return self.data

    def getBlockPosition(self, index):
        blocks = [0, 1, 2, 3,
                0, 1, 3, 2,
                0, 2, 1, 3,
                0, 3, 1, 2,
                0, 2, 3, 1,
                0, 3, 2, 1,
                1, 0, 2, 3,
                1, 0, 3, 2,
                2, 0, 1, 3,
                3, 0, 1, 2,
                2, 0, 3, 1,
                3, 0, 2, 1,
                1, 2, 0, 3,
                1, 3, 0, 2,
                2, 1, 0, 3,
                3, 1, 0, 2,
                2, 3, 0, 1,
                3, 2, 0, 1,
                1, 2, 3, 0,
                1, 3, 2, 0,
                2, 1, 3, 0,
                3, 1, 2, 0,
                2, 3, 1, 0,
                3, 2, 1, 0,

                #duplicates of 0-7 to eliminate modulus
                0, 1, 2, 3,
                0, 1, 3, 2,
                0, 2, 1, 3,
                0, 3, 1, 2,
                0, 2, 3, 1,
                0, 3, 2, 1,
                1, 0, 2, 3,
                1, 0, 3, 2,]
        return blocks[index]

    def copyExistingData(self, source, beginning, end, output, outBeginning):
        j = outBeginning
        i = beginning

        while i < end:
            output[j] = source[i]
            j+=1
            i+=1
            #print("End: " + str(end) + "\ni: " + str(i))

    def copyData(self, source, beginning, end, output, outBeginning):
        j = outBeginning
        i = beginning

        while i < end:
            output.append(source[i])
            i+=1
            j+=1

    def printData(self):
        s = ""
        for x in range(len(self.data)):
            if self.data[x] < 16 and self.data[x] >= 0:
                s = s + "0"
            s = s + hex(self.data[x]) + " "
            if (x % 10) == 0 and x != 0:
                s = s + "\n"
        #print(s)

    def ShuffleArray(self, shuffleValue):
        index = shuffleValue * 4
        originalData = list()

        self.copyData(self.data, 0, storedSize, originalData, 0)

        #print("shuffle array invoked")
        block = 0
        while block < 4:
            offset = self.getBlockPosition(index + block)
            self.copyExistingData(originalData, 8 + blockSize * offset,
                8 + blockSize * offset + blockSize, 
                self.data, 8 + blockSize * block)
            block += 1

        self.printData()

    def decrypt(self):
        shuffleValue = (self.getEncryptionConstant() >> 13) & 31
        self.Crypt()
        self.ShuffleArray(shuffleValue)

    def getIV32(self):
        return int(struct.unpack("I", bytes(self.data[0x8C : 0x8C + 4]))[0])

    def getIVs(self):
        IV32 = self.getIV32()
        IV1 = (IV32 >> 5 * 0) & 0x1F
        IV2 = (IV32 >> 5 * 1) & 0x1F
        IV3 = (IV32 >> 5 * 2) & 0x1F
        IV4 = (IV32 >> 5 * 3) & 0x1F
        IV5 = (IV32 >> 5 * 4) & 0x1F
        IV6 = (IV32 >> 5 * 5) & 0x1F
        return IV1, IV2, IV3, IV4, IV5, IV6

    def getPID(self):
        return int(struct.unpack("I", bytes(self.data[0x1C : 0x1C + 4]))[0])

    def getPID1(self):
        return int(struct.unpack("H", bytes(self.data[0x1C : 0x1C + 2]))[0])

    def getPID2(self):
        return int(struct.unpack("H", bytes(self.data[0x1E : 0x1E + 2]))[0])

    def getSID(self):
        return int(struct.unpack("H", bytes(self.data[0xE : 0xE + 2]))[0])

    def getTID(self):
        return int(struct.unpack("H", bytes(self.data[0xC : 0xC + 2]))[0])

    def getPK(self):
        return int(struct.unpack("H", bytes(self.data[0x8 : 0x8 + 2]))[0])

    def getAbility(self):
        return int(struct.unpack("H", bytes(self.data[0x14 : 0x14 + 2]))[0])

    def getItem(self):
        return int(struct.unpack("H", bytes(self.data[0xA : 0xA + 2]))[0])

    def getNature(self):
        return int(self.data[0x20])
    
    def getStatNature(self):
        return int(self.data[0x21])
    
    def getEXP(self):
        return int(struct.unpack("I", bytes(self.data[0x10 : 0x10 + 4]))[0])

    def getDynamaxLevel(self):
        return int(self.data[0x90])

    def getEVs(self):
        EV1 = int(self.data[0x26])
        EV2 = int(self.data[0x27])
        EV3 = int(self.data[0x28])
        EV4 = int(self.data[0x29])
        EV5 = int(self.data[0x2A])
        EV6 = int(self.data[0x2B])
        return EV1, EV2, EV3, EV4, EV5, EV6

    def getMoves(self):
        Move1 = int(struct.unpack("H", bytes(self.data[0x72 : 0x72 + 2]))[0])
        Move2 = int(struct.unpack("H", bytes(self.data[0x74 : 0x74 + 2]))[0])
        Move3 = int(struct.unpack("H", bytes(self.data[0x76 : 0x76 + 2]))[0])
        Move4 = int(struct.unpack("H", bytes(self.data[0x78 : 0x78 + 2]))[0])
        return Move1, Move2, Move3, Move4


    def getOT(self):
        i = 0
        while True:
            if bytes(self.data[0xF8 + i]) == b'' and bytes(self.data[0xF8 + i + 1]) == b'' or i == 16:
                if i == 0:
                    return "Error"
                else:
                    return bytes(self.data[0xF8 : 0xF8 + i]).decode('utf-16')
            else:
                i = i + 2
        
        

    def getDate(self):
        year = int(self.data[0x11C])
        month = int(self.data[0x11D])
        day = int(self.data[0x11E])
        return year, day, month

    def getPSV(self):
        pid = self.getPID()
        return((pid >> 16 ^ (pid & 0xFFFF)) >> 4)

    def getTSV(self):
        return ((self.getTID() ^ self.getSID()) >> 4)

    def isGiganta(self):
        return (self.data[0x16] & 16) != 0

    def getGender(self):
        return int((self.data[0x22] >> 2) & 0x3)

    def isShiny(self):
        return self.getPSV() == self.getTSV()

    def isEgg(self):
        return ((self.getIV32() >> 30) & 1) == 1
