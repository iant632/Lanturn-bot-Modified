import random

numpad = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 0, 10]]
btncmdseq = list()

def findLocation(n):
	i = 0
	j = 0

	while i < 4:
		while j < 3:
			if n == numpad[i][j]:
				return i, j
			j+=1
		j = 0
		i+=1

def findDifference(i, j, desiredLocation):
	is0 = False
	di, dj = findLocation(desiredLocation)

	if di == 3:
		is0 = True

	i = di - i
	j = dj - j

	return i, j, is0

def constructString(i, j, desiredLocation):
	global btncmdseq
	Signi = False
	Signj = False

	i, j, is0 = findDifference(i,j, desiredLocation)

	if i < 0:
		i = 0 - i
		Signi = True

	if j < 0:
		j = 0 - j
		Signj = True

	if Signi == True:
		x = 0
		while x < i:
			btncmdseq.append("click DUP")
			x+=1
	elif Signi == False:
		x = 0
		while x < i:
			btncmdseq.append("click DDOWN")
			x+=1

	if not is0:
		if Signj == True:
			x = 0
			while x < j:
				btncmdseq.append("click DLEFT")
				x+=1
		elif Signj == False:
			x = 0
			while x < j:
				btncmdseq.append("click DRIGHT")
				x+=1
		
	btncmdseq.append("click A")
	return findLocation(desiredLocation)


def getButtons(input):
	global btncmdseq
	btncmdseq.clear()

	if input == None:
		input = random.randint(50000000,59999999)

	thousands = int(input / 10000000)
	hundreds = int((input / 1000000) % 10)
	tens = int((input / 100000) % 10)
	ones = int((input / 10000) % 10)
	thousands2 = int((input / 1000) % 10)
	hundreds2 = int((input / 100) % 10)
	tens2 = int((input / 10) % 10)
	ones2 = input % 10

	i, j = constructString(0, 0, thousands)
	i, j = constructString(i, j, hundreds)
	i, j = constructString(i, j, tens)
	i, j = constructString(i, j, ones)
	i, j = constructString(i, j, thousands2)
	i, j = constructString(i, j, hundreds2)
	i, j = constructString(i, j, tens2)
	i, j = constructString(i, j, ones2)

	value = str(thousands) + str(hundreds) + str(tens) + str(ones) + str(thousands2) + str(hundreds2) + str(tens2) + str(ones2)
	return btncmdseq, value