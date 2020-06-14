import binascii
import struct
import shutil
import time
import datetime
import os
from datetime import date
from PK8 import *
from framecalc import *
from seedgen import *

def is1on():
	try:
		#Checks flag if it's in use
		fileIn = open("com.bin", "rb")
		fileIn.seek(0)
		isInUse = int(fileIn.read()[0])
		fileIn.close()
		if isInUse == 1:
			return True

		return False
	except:
		return False

def is2on():
	try:
		#Checks flag if it's in use
		fileIn = open("com.bin", "rb")
		fileIn.seek(1)
		isInUse = int(fileIn.read()[0])
		fileIn.close()
		if isInUse == 1:
			return True

		return False
	except:
		return False


def initialize1():
	try:
		fileIn = open("com.bin", "r+b")
		fileIn.seek(2)
		fileIn.write(bytes([1]))
		fileIn.close()

		return True
	except:
		return False

def initialize2():
	try:
		#Checks flag if it's in use
		fileIn = open("com.bin", "r+b")
		fileIn.seek(5)
		fileIn.write(bytes([1]))
		fileIn.close()

		return True
	except Exception as e:
		print(e)

def checkTimeOut1():
	try:
		fileIn = open("com.bin", "r+b")
		fileIn.seek(4)
		isInUse = int(fileIn.read()[0])

		if isInUse == 1:
			fileIn.seek(2)
			fileIn.write(bytes([0]))
			fileIn.seek(3)
			fileIn.write(bytes([0]))
			fileIn.seek(4)
			fileIn.write(bytes([0]))
			fileIn.close()
			return True
		
		return False
	except:
		return False

def checkTimeOut2():
	try:
		fileIn = open("com.bin", "r+b")
		fileIn.seek(7)
		isInUse = int(fileIn.read()[0])

		if isInUse == 1:
			fileIn.seek(5)
			fileIn.write(bytes([0]))
			fileIn.seek(6)
			fileIn.write(bytes([0]))
			fileIn.seek(7)
			fileIn.write(bytes([0]))
			fileIn.close()
			return True
		
		return False
	except:
		return False

def checkSearchStatus1():
	try:
		fileIn = open("com.bin", "r+b")
		fileIn.seek(3)
		isInUse = int(fileIn.read()[0])
		if isInUse == 1:
			fileIn.seek(2)
			fileIn.write(bytes([1]))
			fileIn.seek(3)
			fileIn.write(bytes([0]))
			fileIn.seek(4)
			fileIn.write(bytes([0]))
			fileIn.close()
			return True
			
		return False
	except:
		return False

def checkSearchStatus2():
	try:
		fileIn = open("com.bin", "r+b")
		fileIn.seek(6)
		isInUse = int(fileIn.read()[0])
		if isInUse == 1:
			fileIn.seek(5)
			fileIn.write(bytes([1]))
			fileIn.seek(6)
			fileIn.write(bytes([0]))
			fileIn.seek(7)
			fileIn.write(bytes([0]))
			fileIn.close()
			return True
		
		return False
	except:
		return False

def getCodeString1():
	while True:
		try:
			fileIn = open("code1.txt", "r+")
			code = fileIn.readline()
			fileIn.close()
			return code	
		except:
			print("File reading error occured, trying again!")

def getCodeString2():
	while True:
		try:
			fileIn = open("code2.txt", "r+")
			code = fileIn.readline()
			fileIn.close()
			return code	
		except:
			print("File reading error occured, trying again!")

def checkDuduStatus1():
	try:
		fileIn = open("com.bin", "rb")
		fileIn.seek(2)
		isInUse = int(fileIn.read()[0])
		fileIn.close()

		if isInUse == 1:
			return True
		else:
			return False
	except:
		return False

def checkDuduStatus2():
	try:
		fileIn = open("com.bin", "rb")
		fileIn.seek(5)
		isInUse = int(fileIn.read()[0])
		fileIn.close()

		if isInUse == 1:
			return True
		else:
			return False
	except:
		return False

def getPokeData1():
	fileIn = open("out1.pk8", "rb")
	pk8 = bytearray(fileIn.read())
	fileIn.close()
	data = PK8(pk8)
	pk = data.getPK()

	if pk > 890 or pk < 0:
		return 0, 0, 999, 999, 999, 999, "", False

	year, day, month = data.getDate()

	ec = data.getEncryptionConstant()
	pid = data.getPID()

	IV1, IV2, IV3, IV4, IV5, IV6 = data.getIVs()

	iv = [IV1, IV2, IV3, IV5, IV6, IV4]

	OT = data.getOT()

	isGiganta = data.isGiganta()

	gen = seedgen()
	seed = gen.search(ec, pid, iv)

	return seed, iv, pk, year, day, month, OT, isGiganta

def getPokeInfo1():
	fileIn = open("out1.pk8", "rb")
	pk8 = bytearray(fileIn.read())
	fileIn.close()
	data = PK8(pk8)
	pk = data.getPK()

	IV1, IV2, IV3, IV4, IV5, IV6 = data.getIVs()
	iv = [IV1, IV2, IV3, IV5, IV6, IV4]

	OT = data.getOT()
	rawTID = data.getTID()
	rawSID = data.getSID()
	TID = rawTID + (rawSID * 65536) % 1000000
	SID = (rawTID + (rawSID * 65536) - TID) / 1000000

	PID1 = data.getPID1()
	PID2 = data.getPID2()

	ability = data.getAbility()

	nature = data.getNature()
	statnature = data.getStatNature()

	if ((rawTID ^ rawSID) ^ (PID1 ^ PID2)) == 0:
		shiny = 2
	elif ((rawTID ^ rawSID) ^ (PID1 ^ PID2)) < 16:
		shiny = 1
	else:
		shiny = 0

	item = data.getItem()

	EV1, EV2, EV3, EV4, EV5, EV6 = data.getEVs()
	ev = [EV1, EV2, EV3, EV5, EV6, EV4] 

	move1, move2, move3, move4 = data.getMoves()
	move = [move1, move2, move3, move4]

	isGiganta = data.isGiganta()

	exp = data.getEXP()
	Dlevel = data.getDynamaxLevel()

	return pk, exp, Dlevel, shiny, nature, statnature, iv, ev, move, item, OT, TID, SID, isGiganta, ability

def removePK81():
	os.remove(r'./backup1.pk8')
	os.rename('out1.pk8', 'backup1.pk8')

def getPokeData2():
	fileIn = open("out2.pk8", "rb")
	pk8 = bytearray(fileIn.read())
	fileIn.close()
	data = PK8(pk8)
	pk = data.getPK()

	if pk > 890 or pk < 0:
		return 0, 0, 999, 999, 999, 999, "", False

	year, day, month = data.getDate()

	ec = data.getEncryptionConstant()
	pid = data.getPID()

	IV1, IV2, IV3, IV4, IV5, IV6 = data.getIVs()

	iv = [IV1, IV2, IV3, IV5, IV6, IV4]

	OT = data.getOT()

	gen = seedgen()
	seed = gen.search(ec, pid, iv)

	isGiganta = data.isGiganta()

	return seed, iv, pk, year, day, month, OT, isGiganta

def getPokeInfo2():
	fileIn = open("out2.pk8", "rb")
	pk8 = bytearray(fileIn.read())
	fileIn.close()
	data = PK8(pk8)
	pk = data.getPK()

	IV1, IV2, IV3, IV4, IV5, IV6 = data.getIVs()
	iv = [IV1, IV2, IV3, IV5, IV6, IV4]

	OT = data.getOT()
	rawTID = data.getTID()
	rawSID = data.getSID()
	TID = rawTID + (rawSID * 65536) % 1000000
	SID = (rawTID + (rawSID * 65536) - TID) / 1000000

	PID1 = data.getPID1()
	PID2 = data.getPID2()

	ability = data.getAbility()

	nature = data.getNature()
	statnature = data.getStatNature()

	if ((rawTID ^ rawSID) ^ (PID1 ^ PID2)) == 0:
		shiny = 2
	elif ((rawTID ^ rawSID) ^ (PID1 ^ PID2)) < 16:
		shiny = 1
	else:
		shiny = 0

	item = data.getItem()

	EV1, EV2, EV3, EV4, EV5, EV6 = data.getEVs()
	ev = [EV1, EV2, EV3, EV5, EV6, EV4] 

	move1, move2, move3, move4 = data.getMoves()
	move = [move1, move2, move3, move4]

	isGiganta = data.isGiganta()

	exp = data.getEXP()
	Dlevel = data.getDynamaxLevel()

	return pk, exp, Dlevel, shiny, nature, statnature, iv, ev, move, item, OT, TID, SID, isGiganta, ability

def removePK82():
	os.remove(r'./backup2.pk8')
	os.rename('out2.pk8', 'backup2.pk8')