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
		input = random.randint(5000,5999)

	thousands = int(input / 1000)
	hundreds = int((input / 100) % 10)
	tens = int((input / 10) % 10)
	ones = input % 10

	i, j = constructString(0, 0, thousands)
	i, j = constructString(i, j, hundreds)
	i, j = constructString(i, j, tens)
	i, j = constructString(i, j, ones)

	value = str(thousands) + str(hundreds) + str(tens) + str(ones)
	return btncmdseq, value