from XoroShiro import *

class framecalc:
	XC = int("82A2B175229D6A5B", 16)
	MASK = int("FFFFFFFFFFFFFFFF", 16)

	def __init__(self, seed):
		self.seed = int(seed, 16)

	def getShinyXOR(self, val):
		return (val >> 16) ^ (val & 0xFFFF)

	def getShinyValue(self, num):
		return self.getShinyXOR(num) >> 4

	def getShinyType(self, pid, tisid):
		p = self.getShinyXOR(pid)
		t = self.getShinyXOR(tisid)
		if p == t:
			return 2 #square shiny
		if (p ^ t) < 0x10:
			return 1 #star shiny
		return 0

	def getShinyFrames(self):
		seed = self.seed
		rng = XoroShiro(seed)
		starFrame = -1
		squareFrame = -1

		isStarHidden = -1
		isSquareHidden = -1

		ivs = [-2, -2, -2, -2, -2, -2]
		starivs = [-2, -2, -2, -2, -2, -2]
		squareivs = [-2, -2, -2, -2, -2, -2]

		nature = -1
		starnature = -1
		squarenature = -1

		i = 0
		while True:
			a = rng.nextInt(0xFFFFFFFF, 0xFFFFFFFF)
			SIDTID = rng.nextInt(0xFFFFFFFF, 0xFFFFFFFF)
			PID = rng.nextInt(0xFFFFFFFF,0xFFFFFFFF)

			shinyType = self.getShinyType(PID, SIDTID)

			if shinyType == 0:
				rng.reset(seed)
				seed = rng.next()
				rng.reset(seed)
				ivs = [-2, -2, -2, -2, -2, -2]
				i += 1
				if i >= 10000:
					return starFrame, squareFrame, isStarHidden, isSquareHidden, starivs, squareivs, starnature, squarenature
				continue

			p = 0
			while p < 4:
				b = rng.nextInt(6, 7)
				if ivs[b] == -2:
					ivs[b] = 31
					p += 1
			
			p = 0
			while p < 6:
				if ivs[p] == -2:
					b = rng.nextInt(32, 31)
					ivs[p] = b
				p += 1
			
			isHidden = rng.nextInt(3, 3)

			c = rng.nextInt(253, 255)

			nature = rng.nextInt(25, 31)

			if starFrame == -1:
				if shinyType == 1:
					starFrame = i
					isStarHidden = isHidden
					starivs = ivs
					starnature = nature

			if squareFrame == -1:
				if shinyType == 2:
					squareFrame = i
					isSquareHidden = isHidden
					squareivs = ivs
					squarenature = nature

			rng.reset(seed)
			seed = rng.next()
			rng.reset(seed)
			ivs = [-2, -2, -2, -2, -2, -2]
			i += 1

			if starFrame != -1 and squareFrame != -1:
				return starFrame, squareFrame, isStarHidden, isSquareHidden, starivs, squareivs, starnature, squarenature

			if i >= 10000:
				return starFrame, squareFrame, isStarHidden, isSquareHidden, starivs, squareivs, starnature, squarenature
		