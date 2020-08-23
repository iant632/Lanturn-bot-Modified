import struct
from random import randint

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

    def Crypt2(self):
        seed = self.getEncryptionConstant()
        i = 8
        while i < 0x148:
            seed = self.advance(seed)
            self.data[i] = (self.data[i] ^ (seed >> 16)) & 0xFF
            self.data[i + 1] = (self.data[i+1] ^ (seed >> 24)) & 0xFF
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

    def blockPositionInvert(self, index) :
        blocks = [0, 1, 2, 4, 3, 5, 6, 7, 12, 18, 13, 19, 8, 10, 14, 20, 16, 22, 9, 11, 15, 21, 17, 23, 0, 1, 2, 4, 3, 5, 6, 7,]
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

    def decrypt(self):
        shuffleValue = (self.getEncryptionConstant() >> 13) & 31
        self.Crypt2()
        self.ShuffleArray(shuffleValue)
        self.printData()

    def encrypt(self):
        shuffleValue = (self.getEncryptionConstant() >> 13) & 31
        self.ShuffleArray(self.blockPositionInvert(shuffleValue))
        self.Crypt2()

    def calculateCheckSum(self):
        chk = 0
        i = 8
        while i < 0x146:
            chk += int(self.data[i]) + int(self.data[i+1]) * 256
            i += 2

        chk = chk & 0xFFFF
        chk2 = chk % 256
        self.data[0x6] = chk2
        self.data[0x7] = int((chk - chk2) / 256)


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
        return int(self.data[0x148])

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
            if bytes(self.data[0xF8 + i]) == b'' and bytes(self.data[0xF8 + i + 1]) == b'' or i == 24:
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

    def isNicknamed(self):
        return ((self.getIV32() >> 31) & 1) == 1

    def getHeight(self):
        return int(self.data[0x50])

    def getWeight(self):
        return int(self.data[0x51])

    def isGift(self):
        return (self.data[0x22] & 0x1) == 1

    def makeShiny(self):
        tid = self.getTID()
        sid = self.getSID()
        pid = randint(0, 4294967295)
        pid1 = pid & 0xFFFF
        pid2 = (pid >> 16) & 0xFFFF
        while ((tid ^ sid) ^ (pid1 ^ pid2)) > 15:
            pid = randint(0, 4294967295)
            pid1 = pid & 0xFFFF
            pid2 = (pid >> 16) & 0xFFFF

        self.data[0x1E] = pid & 0xFF
        self.data[0x1F] = (pid >> 8) & 0xFF
        self.data[0x1C] = (pid >> 16) & 0xFF
        self.data[0x1D] = (pid >> 24) & 0xFF
        self.calculateCheckSum()

    def makeSquare(self):
        tid = self.getTID()
        sid = self.getSID()
        pid = randint(0, 4294967295)
        pid1 = pid & 0xFFFF
        pid2 = (pid >> 16) & 0xFFFF
        while ((tid ^ sid) ^ (pid1 ^ pid2)) != 0:
            pid = randint(0, 4294967295)
            pid1 = pid & 0xFFFF
            pid2 = (pid >> 16) & 0xFFFF

        self.data[0x1E] = pid & 0xFF
        self.data[0x1F] = (pid >> 8) & 0xFF
        self.data[0x1C] = (pid >> 16) & 0xFF
        self.data[0x1D] = (pid >> 24) & 0xFF
        self.calculateCheckSum()

    def changeEVs(self, index):
        evs = []
        if index == 1:
            with open('EV1.txt', 'r') as fileIn:
                filecontents = fileIn.readlines()

                for line in filecontents:
                    current_place = line[:-1]

                    # add item to the list
                    evs.append(int(current_place))
        else:
            with open('EV2.txt', 'r') as fileIn:
                filecontents = fileIn.readlines()

                for line in filecontents:
                    current_place = line[:-1]

                    # add item to the list
                    evs.append(int(current_place))

        self.data[0x26] = evs[0]
        self.data[0x27] = evs[1]
        self.data[0x28] = evs[2]
        self.data[0x2A] = evs[3]
        self.data[0x2B] = evs[4]
        self.data[0x29] = evs[5]
        self.calculateCheckSum()

    def changeIVs(self, index):
        ivs = []
        if index == 1:
            with open('IV1.txt', 'r') as fileIn:
                filecontents = fileIn.readlines()

                for line in filecontents:
                    current_place = line[:-1]

                    # add item to the list
                    ivs.append(int(current_place))
        else:
            with open('IV2.txt', 'r') as fileIn:
                filecontents = fileIn.readlines()

                for line in filecontents:
                    current_place = line[:-1]

                    # add item to the list
                    ivs.append(int(current_place))

        if self.isEgg():
            Egg = 1
        else:
            Egg = 0

        if self.isNicknamed():
            Nickname = 1
        else:
            Nickname = 0

        ivs32 = (Nickname << 31) + (Egg << 30) + (ivs[4] << 25) + (ivs[3] << 20) + (ivs[5] << 15) + (ivs[2] << 10) + (ivs[1] << 5) + ivs[0]

        self.data[0x8C] = ivs32 & 0xFF
        self.data[0x8D] = (ivs32 >> 8) & 0xFF
        self.data[0x8E] = (ivs32 >> 16) & 0xFF
        self.data[0x8F] = (ivs32 >> 24) & 0xFF
        self.data[0x126] = 0
        self.calculateCheckSum()

    def changeUser(self, data2, level):
        for i in range(0, 4):
            self.data[0xC + i] = data2[0xC + i]
        for i in range(0, 24):
            self.data[0xF8 + i] = data2[0xF8 + i]

        if data2[0x125] > 128:
            self.data[0x125] = 128 + level
        else:
            self.data[0x125] = level

        self.calculateCheckSum()

    def randomPIDSID(self):
        tid = self.getTID()
        sid = self.getSID()
        pid = randint(0, 4294967295)
        pid1 = pid & 0xFFFF
        pid2 = (pid >> 16) & 0xFFFF
        while ((tid ^ sid) ^ (pid1 ^ pid2)) < 15:
            pid = randint(0, 4294967295)
            pid1 = pid & 0xFFFF
            pid2 = (pid >> 16) & 0xFFFF

        self.data[0x1E] = pid & 0xFF
        self.data[0x1F] = (pid >> 8) & 0xFF
        self.data[0x1C] = (pid >> 16) & 0xFF
        self.data[0x1D] = (pid >> 24) & 0xFF
        
        ec = randint(0, 4294967295)

        self.data[0x0] = ec & 0xFF
        self.data[0x1] = (ec >> 8) & 0xFF
        self.data[0x2] = (ec >> 16) & 0xFF
        self.data[0x3] = (ec >> 24) & 0xFF

        self.calculateCheckSum()

    def randomPIDSIDShiny(self):
        tid = self.getTID()
        sid = self.getSID()
        pid = randint(0, 4294967295)
        pid1 = pid & 0xFFFF
        pid2 = (pid >> 16) & 0xFFFF
        while ((tid ^ sid) ^ (pid1 ^ pid2)) > 15:
            pid = randint(0, 4294967295)
            pid1 = pid & 0xFFFF
            pid2 = (pid >> 16) & 0xFFFF

        self.data[0x1E] = pid & 0xFF
        self.data[0x1F] = (pid >> 8) & 0xFF
        self.data[0x1C] = (pid >> 16) & 0xFF
        self.data[0x1D] = (pid >> 24) & 0xFF
        
        ec = randint(0, 4294967295)

        self.data[0x0] = ec & 0xFF
        self.data[0x1] = (ec >> 8) & 0xFF
        self.data[0x2] = (ec >> 16) & 0xFF
        self.data[0x3] = (ec >> 24) & 0xFF

        self.calculateCheckSum()

    def randomNature(self):
        nature = randint(0, 24)
        self.data[0x20] = nature
        self.data[0x21] = nature

        self.calculateCheckSum()

    def randomIVs(self, flawless):
        ivs = [0, 0, 0, 0, 0, 0]
        i = 0
        while i != flawless:
            j = randint(1, 5)
            if ivs[j] != 31:
                ivs[j] = 31
                i += 1

        i = 0
        while i != 6:
            if ivs[i] != 31:
                ivs[i] = randint(0, 31)
            i += 1            

        Nickname = 0
        Egg = 0

        ivs32 = (Nickname << 31) + (Egg << 30) + (ivs[4] << 25) + (ivs[3] << 20) + (ivs[5] << 15) + (ivs[2] << 10) + (ivs[1] << 5) + ivs[0]

        self.data[0x8C] = ivs32 & 0xFF
        self.data[0x8D] = (ivs32 >> 8) & 0xFF
        self.data[0x8E] = (ivs32 >> 16) & 0xFF
        self.data[0x8F] = (ivs32 >> 24) & 0xFF
        self.data[0x126] = 0
        self.calculateCheckSum()

    def randomIVsGO(self):
        ivs = [0, 0, 0, 0, 0, 0]
        ivs[0] = randint(0, 15) * 2 + 1
        ivs[1] = randint(0, 15) * 2 + 1
        ivs[2] = randint(0, 15) * 2 + 1
        ivs[3] = ivs[1]
        ivs[4] = ivs[2]
        ivs[5] = randint(0, 31)

        Nickname = 0
        Egg = 0

        ivs32 = (Nickname << 31) + (Egg << 30) + (ivs[4] << 25) + (ivs[3] << 20) + (ivs[5] << 15) + (ivs[2] << 10) + (ivs[1] << 5) + ivs[0]

        self.data[0x8C] = ivs32 & 0xFF
        self.data[0x8D] = (ivs32 >> 8) & 0xFF
        self.data[0x8E] = (ivs32 >> 16) & 0xFF
        self.data[0x8F] = (ivs32 >> 24) & 0xFF
        self.calculateCheckSum()

    def randomHW(self):
        self.data[0x50] = randint(0, 255)
        self.data[0x51] = randint(0, 255)
        self.calculateCheckSum()

    def randomGender(self):
        randGender = randint(0, 1)
        self.data[0x22] = (randGender << 2)
        self.calculateCheckSum()

    def makeStandard(self):
        if self.getEXP() < 50:
            self.data[0x10] = 0x5A
            self.data[0x11] = 0x62
            self.data[0x12] = 0x2

        if self.getPK() not in [888, 889, 890]:
            self.data[0x90] = 0xA

        if self.data[0x7A] > 0:
            self.data[0x7E] = 0x3
        if self.data[0x7B] > 0:
            self.data[0x7F] = 0x3
        if self.data[0x7C] > 0:
            self.data[0x80] = 0x3
        if self.data[0x7D] > 0:
            self.data[0x81] = 0x3

        self.calculateCheckSum()
    
    def changeNature(self, index):
        self.data[0x20] = index
        self.data[0x21] = index
        self.calculateCheckSum()
