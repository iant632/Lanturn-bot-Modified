from discord.ext import tasks, commands
import discord
import datetime
import numpy as np
from framecalc import *
from seedgen import *
from GetPokeInfo import *
from bot import *
from Language import *
from datetime import date
from Person import *
from ArrayQueue import *
import time
import codecs
import linecache
import sys

# 300 with the current queue and the reporting system
# will make sure everyone has a place and can see when they will be served
# q = ArrayQueue(300)

# until possible merge and improvement, setting it to 20 as from the previous commits
q = ArrayQueue(40)

class RaidCommands(commands.Cog):
	def __init__(self, client):
		self.checkDataReady.start()
		self.userChannel1 = None
		self.user1 = None
		self.id1 = 0
		self.person1 = None
		self.idInt1 = None
		self.userChannel2 = None
		self.user2 = None
		self.id2 = 0
		self.person2 = None
		self.idInt2 = None
		self.testMode = False
		self.msg1 = None
		self.msg2 = None
		self.language1 = None
		self.language2 = None

	#Clears instance variables
	def clearData1(self):
		self.userChannel1 = None
		self.user1 = None
		self.id1 = 0
		self.idInt1 = None
		self.person1 = None
		self.ifdetailed1 = None
		self.msg1 = None
		self.language1 = None

	def clearData2(self):
		self.userChannel2 = None
		self.user2 = None
		self.id2 = 0
		self.person2 = None
		self.idInt2 = None
		self.ifdetailed2 = None
		self.msg2 = None
		self.language2 = None

	def PrintException(self):
		exc_type, exc_obj, tb = sys.exc_info()
		f = tb.tb_frame
		lineno = tb.tb_lineno
		filename = f.f_code.co_filename
		linecache.checkcache(filename)
		line = linecache.getline(filename, lineno, f.f_globals)
		print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

	def getLanguageText(self, language, index_number):
		if language == 0:
			with codecs.open( "Korean.txt", "r", "utf-8" ) as file:
				DesiredText = file.readlines()

		if language == 1:
			with codecs.open( "English.txt", "r", "utf-8" ) as file:
				DesiredText = file.readlines()

		if language == 2:
			with codecs.open( "Japanese.txt", "r", "utf-8" ) as file:
				DesiredText = file.readlines()

		return DesiredText[index_number].replace("\r\n", "")

	#Generates the appropriate string based on your star and square frames
	def generateFrameString(self, starFrame, squareFrame, language):
		starFrameMessage = ""
		if starFrame != -1:
			starFrameMessage = str(starFrame + 1)
		else:
			starFrameMessage = self.getLanguageText(language, 42)

		squareFrameMessage = ""
		if squareFrame != -1:
			squareFrameMessage = str(squareFrame + 1)
		else:
			squareFrameMessage = self.getLanguageText(language, 43)

		return starFrameMessage, squareFrameMessage

	#나온 결과값인 0, 1, 2에 따라 텍스트를 설정함.
	def generateAbilityString(self, star, square):
		starMessage = ""
		if star == 0:
			starMessage = "1번 특성이 나오는 굴입니다."
		elif star == 1:
			starMessage = "2번 특성이 나오는 굴입니다."
		elif star == 2:
			starMessage = "숨겨진 특성이 나올 수 있는 굴입니다."
		else:
			starMessage = "너무 멀어서 계산이 되지 않네요 :("

		squareMessage = ""
		if square == 0:
			squareMessage = "1번 특성이 나오는 굴입니다."
		elif square == 1:
			squareMessage = "2번 특성이 나오는 굴입니다."
		elif square == 2:
			squareMessage = "숨겨진 특성이 나올 수 있는 굴입니다."
		else:
			squareMessage = "너무 멀어서 계산이 되지 않네요 :("

		return starMessage, squareMessage

	async def addList(self, ctx, number, language):
		global q

		if q.availableSpace():
			print("Invoked by: " + str(ctx.message.author) + " in: " + str(ctx.message.guild))
			if ctx.message.guild != None:

				#신청을 시도하는 사람의 데이터를 모음.
				id = ctx.message.author.id
				#Person(id, channel, author, 0) 0은 일반적인 시드체크를 의미함.
				p = Person(id, ctx.message.channel, ctx.message.author, number, language)

				#Checks if queue already contains assets from the constructed person object
				if not q.contains(p) and self.idInt1 != id and self.idInt2 != id:
					#현재 봇이 켜져있고, 제공되는 사람이 없는지 확인합니다.
					var1 = self.person1 == None and q.size() == 0 and is1on()
					var2 = self.person2 == None and q.size() == 0 and is2on()
					if var1 or var2:
						q.enqueue(p)
						await ctx.send(str(ctx.message.author.display_name) + self.getLanguageText(language, 1))

					#현재 리스트에 신청자가 없는지 확인합니다.
					else:
						q.enqueue(p)
						await ctx.send(str(ctx.message.author.display_name) + self.getLanguageText(language, 2) + str(q.size()) + self.getLanguageText(language, 3))

					#현재 서비스를 받는 사람입니다.
				elif self.idInt1 == id or self.idInt2== id:
					await ctx.send(self.getLanguageText(language, 4))

				else:
					place = q.size() - q.indexOf(p)
					await ctx.send(self.getLanguageText(language, 5) + str(place) + self.getLanguageText(language, 6))
		else:
			await ctx.send(self.getLanguageText(language, 7))

	async def sendList(self, ctx, language):
		global q
		list_text = self.getLanguageText(language, 8) + "```\n"
		if self.user1 != None:
			list_text += "\n" + self.getLanguageText(language, 9) + self.user1.display_name
		else:
			if is1on():
				list_text += "\n" + self.getLanguageText(language, 10)
			else:
				list_text += "\n" + self.getLanguageText(language, 11)

		if self.user2 != None:
			list_text += "\n" + self.getLanguageText(language, 12) + self.user2.display_name
		else:
			if is2on():
				list_text += "\n" + self.getLanguageText(language, 13)
			else:
				list_text += "\n" + self.getLanguageText(language, 14)

		list_text += q.sendList(language)

		await ctx.send(list_text)

	async def cancelQueue(self, ctx, language):
		global q

		if ctx.message.guild != None:

			#현재 취소를 신청하는 사람의 정보를 모음
			id = ctx.message.author.id
			p = Person(id, ctx.message.channel, ctx.message.author, 0, 0)

			#현재 서비스를 제공하는 중이거나, 신청하지 않은 경우 출력합니다.
			if self.idInt1 == id:
				if is1on():
					await ctx.send(self.getLanguageText(language, 15))

			elif self.idInt2 == id:
				if is2on():
					await ctx.send(self.getLanguageText(language, 15))

			elif not q.contains(p):
				await ctx.send(self.getLanguageText(language, 16))

			else:
				q.removeQueue(p)
				await ctx.send(str(ctx.message.author.display_name) + self.getLanguageText(language, 17))

	def getDateString(self, starFrame, squareFrame, date_pk, language):
		if starFrame != -1:
			if starFrame > 3:
				delta_star = datetime.timedelta(days=starFrame - 3)
				date_star = date_pk + delta_star
				stardateString = date_star.strftime(self.getLanguageText(language, 44))

			elif starFrame == 3:
				stardateString = self.getLanguageText(language, 45)

			else:
				stardateString = self.getLanguageText(language, 46)

		else:
			stardateString = self.getLanguageText(language, 47)

		if squareFrame != -1:
			if squareFrame > 3:
				delta_square = datetime.timedelta(days=squareFrame - 3)
				date_square = date_pk + delta_square
				squaredateString = date_square.strftime(self.getLanguageText(language, 44))

			elif squareFrame == 3:
				squaredateString = self.getLanguageText(language, 48)

			else:
				squaredateString = self.getLanguageText(language, 49)

		else:
			squaredateString = self.getLanguageText(language, 50)

		return stardateString, squaredateString

	async def sendResult(self, number):
		time.sleep(2.0)
		if number == 1:
			seed, iv, pk, year, day, month, OT, isGiganta = getPokeData1()
			ifdetailed = self.ifdetailed1
			userid = self.id1
			userChannel = self.userChannel1
			msg = self.msg1
			language = self.language1
		else:
			seed, iv, pk, year, day, month, OT, isGiganta = getPokeData2()
			ifdetailed = self.ifdetailed2
			userid = self.id2
			userChannel = self.userChannel2
			msg = self.msg2
			language = self.language2

		await msg.delete()

		if pk != 0:
			pokemon_string = getPokeString(pk, isGiganta, False, language)

			if seed != -1:	
				calc = framecalc(seed)
				starFrame, squareFrame, isStarHidden, isSquareHidden, stariv, squareiv, starnature, squarenature = calc.getShinyFrames()
				date_pk = datetime.date(year+2000, month, day)
				
				stardateString, squaredateString = self.getDateString(starFrame, squareFrame, date_pk, language)

				starFrameMessage, squareFrameMessage = self.generateFrameString(starFrame, squareFrame, language)

				if ifdetailed == 0: 
					await userChannel.send(userid + self.getLanguageText(language, 51) + pokemon_string +
						"\n" + self.getLanguageText(language, 52) + OT +
						"\n" + self.getLanguageText(language, 53) + seed[2:] + 
						"\n" + self.getLanguageText(language, 54) + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
						"\n" + self.getLanguageText(language, 55) + starFrameMessage +
						"\n" + self.getLanguageText(language, 56) + stardateString +
						"\n" + self.getLanguageText(language, 57) + squareFrameMessage +
						"\n" + self.getLanguageText(language, 58) + squaredateString +
						self.getLanguageText(language, 59) + seed[2:])

				else:
					nature_name = ["노력", "외로움", "용감", "고집", "개구쟁이", "대담", "온순", "무사태평", "장난꾸러기", "촐랑", "겁쟁이", "성급", "성실", "명랑", "천진난만", "조심", "의젓", "냉정", "수줍음", "덜렁", "차분", "얌전", "건방", "신중", "변덕"]
					starHiddenMessage, squareHiddenMessage = self.generateAbilityString(isStarHidden, isSquareHidden)

					if starFrame == -1 and squareFrame == -1:
						await userChannel.send(userid + "```포켓몬 : " + pokemon_string +
						"\n어버이 : " + OT +
						"\n시드 : " + seed[2:] + 
						"\n개체값: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
						"\n최초의 이로치 프레임 : 이로치 시드가 10000보다 커요!" + 
						"```자세한 건 이 사이트에서 확인이 가능해요! https://iant.kr/seedchecker?seed=" + seed[2:] + "\n공지는 항상 읽어주세요 :)")

					elif starFrame != -1 and squareFrame == -1:

						await userChannel.send(userid + "```포켓몬 : " + pokemon_string +
							"\n어버이 : " + OT +
							"\n시드 : " + seed[2:] + 
							"\n개체값: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
							"\n최초의 이로치 프레임 : " + starFrameMessage +
							"\n이로치 종류 : 별로치" +
							"\n별로치 저장해야되는 날짜 : " + stardateString +
							"\n별로치 특성 : " + starHiddenMessage +
							"\n5성 기준 별로치 개체값: " + str(stariv[0]) + "/" + str(stariv[1]) + "/" + str(stariv[2]) + "/" + str(stariv[3]) + "/" + str(stariv[4]) + "/" + str(stariv[5]) + 
							"\n별로치 성격 : " + nature_name[starnature] +
							"```자세한 건 이 사이트에서 확인이 가능해요! https://iant.kr/seedchecker?seed=" + seed[2:] + "\n공지는 항상 읽어주세요 :)")

					elif starFrame < squareFrame and starFrame != -1:

						await userChannel.send(userid + "```포켓몬 : " + pokemon_string +
							"\n어버이 : " + OT +
							"\n시드 : " + seed[2:] + 
							"\n개체값: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
							"\n최초의 이로치 프레임 : " + starFrameMessage +
							"\n이로치 종류 : 별로치" +
							"\n별로치 저장해야되는 날짜 : " + stardateString +
							"\n별로치 특성 : " + starHiddenMessage +
							"\n5성 기준 이로치 개체값: " + str(stariv[0]) + "/" + str(stariv[1]) + "/" + str(stariv[2]) + "/" + str(stariv[3]) + "/" + str(stariv[4]) + "/" + str(stariv[5]) + 
							"\n별로치 성격 : " + nature_name[starnature] +
							"```자세한 건 이 사이트에서 확인이 가능해요! https://iant.kr/seedchecker?seed=" + seed[2:] + "\n공지는 항상 읽어주세요 :)")

					else:

						await userChannel.send(userid + "```포켓몬 : " + pokemon_string +
							"\n어버이 : " + OT +
							"\n시드 : " + seed[2:] + 
							"\n개체값: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
							"\n최초의 이로치 프레임 : " + squareFrameMessage +
							"\n이로치 종류 : 미로치" +
							"\n미로치 저장해야되는 날짜 : " + squaredateString +
							"\n미로치 특성 : " + squareHiddenMessage +
							"\n5성 기준 미로치 개체값: " + str(squareiv[0]) + "/" + str(squareiv[1]) + "/" + str(squareiv[2]) + "/" + str(squareiv[3]) + "/" + str(squareiv[4]) + "/" + str(squareiv[5]) + 
							"\n미로치 성격 : " + nature_name[squarenature] +
							"```자세한 건 이 사이트에서 확인이 가능해요! https://iant.kr/seedchecker?seed=" + seed[2:] + "\n공지는 항상 읽어주세요 :)")

				#self.writeStat(self.person1, pk, starFrame, squareFrame)

				#outputs how many people remain in line
				time.sleep(1.0)
				await userChannel.send(self.getLanguageText(language, 60) + str(q.size()) + self.getLanguageText(language, 61))

			else:
				await userChannel.send(userid + self.getLanguageText(language, 62) + OT + self.getLanguageText(language, 63) + pokemon_string + self.getLanguageText(language, 64) + str(q.size()) + self.getLanguageText(language, 65))

			return 0
		else:
			await userChannel.send(userid + self.getLanguageText(language, 66) + str(q.size()) + self.getLanguageText(language, 67))
			return 0
		
	async def sendResult2(self, number):
		time.sleep(2.0)
		if number == 1:
			pk, exp, Dlevel, shiny, nature, statnature, iv, ev, move, item, OT, TID, SID, isGiganta, ability, gender, isEgg, PID, EC = getPokeInfo1()
			userChannel = self.userChannel1
			userid = self.id1
			msg = self.msg1
			language = self.language1
		else:
			pk, exp, Dlevel, shiny, nature, statnature, iv, ev, move, item, OT, TID, SID, isGiganta, ability, gender, isEgg, PID, EC = getPokeInfo2()
			userChannel = self.userChannel2
			userid = self.id2
			msg = self.msg2
			language = self.language2

		await msg.delete()

		print()

		if pk != 0:

			pokemon_string = getPokeString(pk, isGiganta, isEgg, language)
			shiny_name = ["X", "☆", "◇"]
			gender_name = getGenderString(gender, language)
			nature_name = getNatureString(nature, language)
			statnature_name = getNatureString(statnature, language)
			ability_name = getAbilityString(ability, language)
			item_name = getItemString(item, language)
			move_name = getMoveString(move, language)

			await userChannel.send(userid + "```" + pokemon_string + " @ " + item_name[item] +
				"\n" + self.getLanguageText(language, 68) + gender_name +
				"\n" + self.getLanguageText(language, 69) + str(exp) +
				"\n" + self.getLanguageText(language, 70) + str(Dlevel) +
				"\n" + self.getLanguageText(language, 54) + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
				"\n" + self.getLanguageText(language, 71) + str(ev[0]) + "/" + str(ev[1]) + "/" + str(ev[2]) + "/" + str(ev[3]) + "/" + str(ev[4]) + "/" + str(ev[5]) + 
				"\n" + self.getLanguageText(language, 72) + ability_name +
				"\n" + self.getLanguageText(language, 73) + shiny_name[shiny] +
				"\n" + self.getLanguageText(language, 74) + nature_name +
				"\n" + self.getLanguageText(language, 75) + statnature_name +
				"\n" + move_name[0] + "/" + move_name[1] + "/" + move_name[2] + "/" + move_name[3] +
				"\n\n" + self.getLanguageText(language, 52) + OT +
				"\nTID: " + str(TID).zfill(6) +
				"\nSID: " + str(round(SID)).zfill(4) + 
				"\nPID: " + str(hex(PID)) +
				"\nEC: " + str(hex(EC)) + "```")
			
			time.sleep(1.0)
			await userChannel.send(self.getLanguageText(language, 60) + str(q.size()) + self.getLanguageText(language, 61))
		
		else:
			await userChannel.send(userid + self.getLanguageText(language, 66) + str(q.size()) + self.getLanguageText(language, 67))
			return 0

	#남은 사람 리스트를 제출합니다.
	@commands.command(name="리스트")
	async def sendList2(self, ctx):
		await self.sendList(ctx, 0)

	#comm.bin 의 파일을 읽어 현재 켜져있는 봇을 체크함.
	@commands.command(name="봇")
	async def sendStatus(self, ctx):
		a = 0
		if is1on():
			a += 1
		if is2on():
			a += 1
		await ctx.send("현재 " + str(a) + "개의 봇용 닌텐도 스위치가 켜져 있습니다.")

	#리스트와 같은 코드.
	@commands.command(name="대기열")
	async def sendList3(self, ctx):
		await self.sendList(ctx, 0)

	@commands.command(name="GetQueue")
	async def sendList4(self, ctx):
		await self.sendList(ctx, 1)
	
	@commands.command(name="취소")
	async def queueCancel(self, ctx):
		await self.cancelQueue(ctx, 0)

	@commands.command(name="TradeCancel")
	async def queueCancel2(self, ctx):
		await self.cancelQueue(ctx, 1)

	@commands.command(name="tradecancel")
	async def queueCancel3(self, ctx):
		await self.cancelQueue(ctx, 1)

	#일반적인 시드체크
	@commands.command(name="시드체크")
	async def checkMySeed(self, ctx):
		await self.addList(ctx, 0, 0)

	#자세히 체크 코드
	@commands.command(name="자세히체크")
	async def checkMySeed2(self, ctx):
		await self.addList(ctx, 1, 0)

	#정보 체크 코드
	@commands.command(name="정보체크")
	async def checkMySeed3(self, ctx):
		await self.addList(ctx, 2, 0)

	@commands.command(name="CheckMySeed")
	async def checkMySeed4(self, ctx):
		await self.addList(ctx, 0, 1)
	
	@commands.command(name="checkmyseed")
	async def checkMySeed5(self, ctx):
		await self.addList(ctx, 0, 1)
	
	@commands.command(name="GetPokeInfo")
	async def checkMySeed7(self, ctx):
		await self.addList(ctx, 2, 1)
	
	@commands.command(name="GetPokeInfo")
	async def checkMySeed8(self, ctx):
		await self.addList(ctx, 2, 1)

	@commands.command(name="シード検索")
	async def checkMySeed6(self, ctx):
		await self.addList(ctx, 0, 2)
	
	@commands.command(name="交換キャンセル")
	async def queueCancel4(self, ctx):
		await self.cancelQueue(ctx, 2)

	@commands.command(name="待機リスト")
	async def sendList5(self, ctx):
		await self.sendList(ctx, 2)

	@commands.command(name="詳細検索")
	async def checkMySeed9(self, ctx):
		await self.addList(ctx, 2, 2)
	


	#Main loop that is sending and receiving data from the dudu client
	@tasks.loop(seconds=0.1)
	async def checkDataReady(self):
		try:
			global q

			#If there is no person being served and the queue is not empty, get the next person in the queue
			#and start the dudu client
			if self.person1 == None and not q.isEmpty() and is1on():
				self.person1 = q.dequeue()
				self.id1 = self.person1.getIDString()
				self.userChannel1 = self.person1.getUserChannel()
				self.ifdetailed1 = self.person1.ifdetailed()
				self.idInt1 = self.person1.getID()
				self.user1 = self.person1.getUser()
				self.language1 = self.person1.getLanguage()
				initialize1()

			if self.person2 == None and not q.isEmpty() and is2on():
				self.person2 = q.dequeue()
				self.id2 = self.person2.getIDString()
				self.userChannel2 = self.person2.getUserChannel()
				self.ifdetailed2 = self.person2.ifdetailed()
				self.user2 = self.person2.getUser()
				self.idInt2 = self.person2.getID()
				self.language2 = self.person2.getLanguage()
				initialize2()

			#FOR 1

			#Checks if lanturn is now searching and if there is a person being served
			if checkSearchStatus1() and self.person1 != None:
				
				#Gets link code from text file
				code = getCodeString1()

				await self.user1.send("```python\n" + self.getLanguageText(self.language1, 18) + code + self.getLanguageText(self.language1, 19))
				self.msg1 = await self.userChannel1.send(self.getLanguageText(self.language1, 20) + self.user1.display_name + self.getLanguageText(self.language1, 21))


			if checkPassword1() and self.person1 != None:
				await self.msg1.delete()
				self.msg1 = await self.userChannel1.send(self.getLanguageText(self.language1, 22) + self.user1.display_name + self.getLanguageText(self.language1, 23))

			if checkTrade1() and self.person1 != None:
				await self.msg1.delete()
				self.msg1 = await self.userChannel1.send(self.getLanguageText(self.language1, 24))

			if checkMeet1() and self.person1 != None:
				username = getUserName1()
				await self.msg1.delete()
				self.msg1 = await self.userChannel1.send(self.getLanguageText(self.language1, 25) + username + self.getLanguageText(self.language1, 26))

			#Check if user has timed out and checks if a valid userChannel is present
			if checkTimeOut1() and self.userChannel1 != None:
				await self.msg1.delete()
				await self.userChannel1.send(self.id1 + self.getLanguageText(self.language1, 27) + str(q.size()) + self.getLanguageText(self.language1, 28))
				self.clearData1()

			#Check if a valid user channel is present and if the dudu client is still running
			if self.userChannel1 != None and not checkDuduStatus1():
				if self.ifdetailed1 != 2:
					await self.sendResult(1)
					time.sleep(1.0)
					self.clearData1()
					removePK81()

				else:
					await self.sendResult2(1)
					time.sleep(1.0)
					self.clearData1()
					removePK81()



			#FOR 2

			#Checks if lanturn is now searching and if there is a person being served
			if checkSearchStatus2() and self.person2 != None:
				
				#Gets link code from text file
				code = getCodeString2()

				await self.user2.send("```python\n" + self.getLanguageText(self.language2, 29) + code + self.getLanguageText(self.language2, 30))
				self.msg2 = await self.userChannel2.send(self.getLanguageText(self.language2, 31) + self.user2.display_name + self.getLanguageText(self.language2, 32))

			if checkPassword2() and self.person2 != None:
				await self.msg2.delete()
				self.msg2 = await self.userChannel2.send(self.getLanguageText(self.language2, 33) + self.user2.display_name + self.getLanguageText(self.language2, 34))

			if checkTrade2() and self.person2 != None:
				await self.msg2.delete()
				self.msg2 = await self.userChannel2.send(self.getLanguageText(self.language2, 35))

			if checkMeet2() and self.person2 != None:
				username = getUserName2()
				await self.msg2.delete()
				self.msg2 = await self.userChannel2.send(self.getLanguageText(self.language2, 36) + username + self.getLanguageText(self.language2, 37))

			#Check if user has timed out and checks if a valid userChannel is present
			if checkTimeOut2() and self.userChannel2 != None:
				await self.msg2.delete()
				await self.userChannel2.send(self.id2 + self.getLanguageText(self.language2, 38) + str(q.size()) + self.getLanguageText(self.language2, 39))
				self.clearData2()

			#Check if a valid user channel is present and if the dudu client is still running
			if self.userChannel2 != None and not checkDuduStatus2():
				if self.ifdetailed2 != 2:
					await self.sendResult(2)
					time.sleep(1.0)
					self.clearData2()
					removePK82()

				else:
					await self.sendResult2(2)
					time.sleep(1.0)
					self.clearData2()
					removePK82()
			#await ctx.send("Invoked")

		except FileNotFoundError as not_found:
			print(self.PrintException())
			if not_found.filename == 'out1.pk8':
				await self.userChannel1.send(self.id1 + self.getLanguageText(self.language1, 40) + str(q.size()) + self.getLanguageText(self.language1, 41))
				self.clearData1()
			elif not_found.filename == 'out2.pk8':
				await self.userChannel2.send(self.id2 + self.getLanguageText(self.language2, 42) + str(q.size()) + self.getLanguageText(self.language2, 43))
				self.clearData2()
	
		except Exception as e:
			print(self.PrintException())
			pass



def setup(client):
	client.add_cog(RaidCommands(client))


