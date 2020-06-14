from discord.ext import tasks, commands
import discord
import datetime
from framecalc import *
from seedgen import *
from GetPokeInfo import *
from bot import *
from datetime import date
from Person import *
from ArrayQueue import *
import time

# 300 with the current queue and the reporting system
# will make sure everyone has a place and can see when they will be served
# q = ArrayQueue(300)

# until possible merge and improvement, setting it to 20 as from the previous commits
q = ArrayQueue(40)

class RaidCommands(commands.Cog):
	def __init__(self, client):
		self.checkDataReady.start()
		self.idInt = None
		self.person = None
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

	#Clears instance variables
	def clearData1(self):
		self.userChannel1 = None
		self.user1 = None
		self.id1 = 0
		self.idInt1 = None
		self.person1 = None
		self.ifdetailed1 = None

	def clearData2(self):
		self.userChannel2 = None
		self.user2 = None
		self.id2 = 0
		self.person2 = None
		self.idInt2 = None
		self.ifdetailed2 = None

	#Generates the appropriate string based on your star and square frames
	def generateFrameString(self, starFrame, squareFrame):
		starFrameMessage = ""
		if starFrame != -1:
			starFrameMessage = str(starFrame + 1)
		else:
			starFrameMessage = "Shiny frame greater than 10000! Try again :("

		squareFrameMessage = ""
		if squareFrame != -1:
			squareFrameMessage = str(squareFrame + 1)
		else:
			squareFrameMessage = "Shiny frame greater than 10000! Try again :("

		return starFrameMessage, squareFrameMessage

	#Set text using result 0, 1, 2
	def generateAbilityString(self, star, square):
		starMessage = ""
		if star == 0:
			starMessage = "Ability 1 is available"
		elif star == 1:
			starMessage = "Ability 2 is available"
		elif star == 2:
			starMessage = "Hidden ability is available."
		else:
			starMessage = "Too far to calculate."

		squareMessage = ""
		if square == 0:
			squareMessage = "Ability 1 is available"
		elif square == 1:
			squareMessage = "Ability 2 is available"
		elif square == 2:
			squareMessage = "Hidden ability is available."
		else:
			squareMessage = "Too far to calculate."

		return starMessage, squareMessage
		
	#Send Trade Line
	@commands.command(name="tradeList")
	async def sendList(self, ctx):
		global q
		await ctx.send(q.sendList())

	#Check how many bot is remain
	@commands.command(name="bot")
	async def sendStatus(self, ctx):
		a = 0
		if is1on():
			a += 1
		if is2on():
			a += 1
		await ctx.send(str(a) + " Nintendo Switch is online.")
	
	@commands.command(name="tradeCancel")
	async def queueCancel(self, ctx):
		global q

		if q.availableSpace():

			if ctx.message.guild != None:

				#Gather the person's information
				id = ctx.message.author.id
				p = Person(id, ctx.message.channel, ctx.message.author, 0)

				#Print if served or bot is offline
				if self.idInt1 == id:
					await ctx.send("Please wait until Switch 1 is online.")
					
				if self.idInt2 == id:
					await ctx.send("Please wait until Switch 2 is online.")

				elif not q.contains(p):
					await ctx.send("I can't help you :(")

				else:
					q.removeQueue(p)
					await ctx.send(str(ctx.message.author.display_name) + ", Your trade is canceled.")

	#Typical Seed Check
	@commands.command(name="CheckMySeed")
	async def checkMySeed(self, ctx):
		global q

		if q.availableSpace():
			print("Invoked by: " + str(ctx.message.author) + " in: " + str(ctx.message.guild))
			if ctx.message.guild != None:

				#Gather the person's information
				id = ctx.message.author.id
				#Person(id, channel, author, 0) 0 means typical seed check
				p = Person(id, ctx.message.channel, ctx.message.author, 0)

				#Checks if queue already contains assets from the constructed person object
				if not q.contains(p) and self.idInt1 != id and self.idInt2 != id:
					#Check if this bot is on there are no person in the queue
					var1 = self.person1 == None and is1on()
					var2 = self.person2 == None and is2on()
					if var1 or var2:
						q.enqueue(p)
						await ctx.send(str(ctx.message.author.display_name) + " Bot dispatched, I will ping you once I start searching! There are currently no one in front of you!")

					#Check if there's no person in the queue
					else:
						q.enqueue(p)
						await ctx.send(str(ctx.message.author.display_name) + " Bot dispatched, I will ping you once I start searching! There are currently " + str(q.size()) + " people waiting in front of you.")

				#It's your turn.
				elif self.idInt1 == id or self.idInt2== id:
					await ctx.send("It is your turn now :)")

				else:
					place = q.size() - q.indexOf(p)
					await ctx.send("There are currently " + str(place) + " people waiting in front of you.")
		else:
			await ctx.send("There are too much people so I can't add you in.")

	#Check Seed Info
	@commands.command(name="CheckSeedInfo")
	async def checkMySeed2(self, ctx):
		global q

		if q.availableSpace():
			print("Invoked by: " + str(ctx.message.author) + " in: " + str(ctx.message.guild))
			if ctx.message.guild != None:

				#신청을 시도하는 사람의 데이터를 모음.
				id = ctx.message.author.id
				#Person(id, channel, author, 1) 1은 자세한 시드체크를 의미함.
				p = Person(id, ctx.message.channel, ctx.message.author, 1)

				#Checks if queue already contains assets from the constructed person object
				if not q.contains(p) and self.idInt1 != id and self.idInt2 != id:
					#현재 봇이 켜져있고, 제공되는 사람이 없는지 확인합니다.
					var1 = self.person1 == None and is1on()
					var2 = self.person2 == None and is2on()
					if var1 or var2:
						q.enqueue(p)
						await ctx.send(str(ctx.message.author.display_name) + " Bot dispatched, I will ping you once I start searching! There are currently no one in front of you!")

					#현재 리스트에 신청자가 없는지 확인합니다.
					else:
						q.enqueue(p)
						await ctx.send(str(ctx.message.author.display_name) + " Bot dispatched, I will ping you once I start searching! There are currently " + str(q.size()) + " people waiting in front of you.")

					#현재 서비스를 받는 사람입니다.
				elif self.idInt1 == id or self.idInt2== id:
					await ctx.send("It is your turn now :)")

				else:
					place = q.size() - q.indexOf(p)
					await ctx.send("There are currently " + str(place) + " people waiting in front of you.")
		else:
			await ctx.send("There are too much people so I can't add you in.")


	#Main loop that is sending and receiving data from the dudu client
	@tasks.loop(seconds=0.1)
	async def checkDataReady(self):
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
			initialize1()

		if self.person2 == None and not q.isEmpty() and is2on():
			self.person2 = q.dequeue()
			self.id2 = self.person2.getIDString()
			self.userChannel2 = self.person2.getUserChannel()
			self.ifdetailed2 = self.person2.ifdetailed()
			self.user2 = self.person2.getUser()
			self.idInt2 = self.person2.getID()
			initialize2()

		#FOR 1

		#Checks if lanturn is now searching and if there is a person being served
		if checkSearchStatus1() and self.person1 != None:
			#Gets link code from text file
			code = getCodeString1()

			await self.user1.send("```python\nHi there! Your private link code is: " + code + "\nPlease use it to match up with me in trade!```")

		#Check if user has timed out and checks if a valid userChannel is present
		if checkTimeOut1() and self.userChannel1 != None:
			await self.userChannel1.send(self.id1 + " You have been timed out! You either took too long to respond or you lost connection. People remaining in line: " + str(q.size()))
			self.clearData1()

		#Check if a valid user channel is present and if the dudu client is still running
		if self.userChannel1 != None and not checkDuduStatus1():
			time.sleep(2.0)
			seed, iv, pk, year, day, month, OT = getPokeData1()

			if pk != 0:
				names = ["Egg", "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoranâ™€", "Nidorina", "Nidoqueen", "Nidoranâ™‚", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetchâ€™d", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Raikou", "Entei", "Suicune", "Larvitar", "Pupitar", "Tyranitar", "Lugia", "Ho-Oh", "Celebi", "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple", "Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo", "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Tropius", "Chimecho", "Absol", "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Regirock", "Regice", "Registeel", "Latias", "Latios", "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys", "Turtwig", "Grotle", "Torterra", "Chimchar", "Monferno", "Infernape", "Piplup", "Prinplup", "Empoleon", "Starly", "Staravia", "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune", "Shinx", "Luxio", "Luxray", "Budew", "Roserade", "Cranidos", "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam", "Mothim", "Combee", "Vespiquen", "Pachirisu", "Buizel", "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom", "Drifloon", "Drifblim", "Buneary", "Lopunny", "Mismagius", "Honchkrow", "Glameow", "Purugly", "Chingling", "Stunky", "Skuntank", "Bronzor", "Bronzong", "Bonsly", "Mime Jr.", "Happiny", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp", "Munchlax", "Riolu", "Lucario", "Hippopotas", "Hippowdon", "Skorupi", "Drapion", "Croagunk", "Toxicroak", "Carnivine", "Finneon", "Lumineon", "Mantyke", "Snover", "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth", "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z", "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom", "Uxie", "Mesprit", "Azelf", "Dialga", "Palkia", "Heatran", "Regigigas", "Giratina", "Cresselia", "Phione", "Manaphy", "Darkrai", "Shaymin", "Arceus", "Victini", "Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog", "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole", "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Basculin", "Sandile", "Krokorok", "Krookodile", "Darumaka", "Darmanitan", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask", "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark", "Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite", "Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet", "Accelgor", "Stunfisk", "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta", "Volcarona", "Cobalion", "Terrakion", "Virizion", "Tornadus", "Thundurus", "Reshiram", "Zekrom", "Landorus", "Kyurem", "Keldeo", "Meloetta", "Genesect", "Chespin", "Quilladin", "Chesnaught", "Fennekin", "Braixen", "Delphox", "Froakie", "Frogadier", "Greninja", "Bunnelby", "Diggersby", "Fletchling", "Fletchinder", "Talonflame", "Scatterbug", "Spewpa", "Vivillon", "Litleo", "Pyroar", "FlabÃ©bÃ©", "Floette", "Florges", "Skiddo", "Gogoat", "Pancham", "Pangoro", "Furfrou", "Espurr", "Meowstic", "Honedge", "Doublade", "Aegislash", "Spritzee", "Aromatisse", "Swirlix", "Slurpuff", "Inkay", "Malamar", "Binacle", "Barbaracle", "Skrelp", "Dragalge", "Clauncher", "Clawitzer", "Helioptile", "Heliolisk", "Tyrunt", "Tyrantrum", "Amaura", "Aurorus", "Sylveon", "Hawlucha", "Dedenne", "Carbink", "Goomy", "Sliggoo", "Goodra", "Klefki", "Phantump", "Trevenant", "Pumpkaboo", "Gourgeist", "Bergmite", "Avalugg", "Noibat", "Noivern", "Xerneas", "Yveltal", "Zygarde", "Diancie", "Hoopa", "Volcanion", "Rowlet", "Dartrix", "Decidueye", "Litten", "Torracat", "Incineroar", "Popplio", "Brionne", "Primarina", "Pikipek", "Trumbeak", "Toucannon", "Yungoos", "Gumshoos", "Grubbin", "Charjabug", "Vikavolt", "Crabrawler", "Crabominable", "Oricorio", "Cutiefly", "Ribombee", "Rockruff", "Lycanroc", "Wishiwashi", "Mareanie", "Toxapex", "Mudbray", "Mudsdale", "Dewpider", "Araquanid", "Fomantis", "Lurantis", "Morelull", "Shiinotic", "Salandit", "Salazzle", "Stufful", "Bewear", "Bounsweet", "Steenee", "Tsareena", "Comfey", "Oranguru", "Passimian", "Wimpod", "Golisopod", "Sandygast", "Palossand", "Pyukumuku", "Type: Null", "Silvally", "Minior", "Komala", "Turtonator", "Togedemaru", "Mimikyu", "Bruxish", "Drampa", "Dhelmise", "Jangmo-o", "Hakamo-o", "Kommo-o", "Tapu Koko", "Tapu Lele", "Tapu Bulu", "Tapu Fini", "Cosmog", "Cosmoem", "Solgaleo", "Lunala", "Nihilego", "Buzzwole", "Pheromosa", "Xurkitree", "Celesteela", "Kartana", "Guzzlord", "Necrozma", "Magearna", "Marshadow", "Poipole", "Naganadel", "Stakataka", "Blacephalon", "Zeraora", "Meltan", "Melmetal", "Grookey", "Thwackey", "Rillaboom", "Scorbunny", "Raboot", "Cinderace", "Sobble", "Drizzile", "Inteleon", "Skwovet", "Greedent", "Rookidee", "Corvisquire", "Corviknight", "Blipbug", "Dottler", "Orbeetle", "Nickit", "Thievul", "Gossifleur", "Eldegoss", "Wooloo", "Dubwool", "Chewtle", "Drednaw", "Yamper", "Boltund", "Rolycoly", "Carkol", "Coalossal", "Applin", "Flapple", "Appletun", "Silicobra", "Sandaconda", "Cramorant", "Arrokuda", "Barraskewda", "Toxel", "Toxtricity", "Sizzlipede", "Centiskorch", "Clobbopus", "Grapploct", "Sinistea", "Polteageist", "Hatenna", "Hattrem", "Hatterene", "Impidimp", "Morgrem", "Grimmsnarl", "Obstagoon", "Perrserker", "Cursola", "Sirfetchâ€™d", "Mr. Rime", "Runerigus", "Milcery", "Alcremie", "Falinks", "Pincurchin", "Snom", "Frosmoth", "Stonjourner", "Eiscue", "Indeedee", "Morpeko", "Cufant", "Copperajah", "Dracozolt", "Arctozolt", "Dracovish", "Arctovish", "Duraludon", "Dreepy", "Drakloak", "Dragapult", "Zacian", "Zamazenta", "Eternatus"]

				if isGiganta:
					pokemon_string = "Gigantamax " + names[pk]
				else:
					pokemon_string = names[pk]
				
				if seed != -1:	
					calc = framecalc(seed)
					starFrame, squareFrame, isStarHidden, isSquareHidden, stariv, squareiv, starnature, squarenature = calc.getShinyFrames()
					date_pk = datetime.date(year+2000, month, day)
					if starFrame != -1:
						if starFrame > 3:
							delta_star = datetime.timedelta(days=starFrame - 3)
							date_star = date_pk + delta_star
							stardateString = date_star.strftime("%YY %mM %dD")

						elif starFrame == 3:
							stardateString = "You succeed to open the raid den! Congratulations :)"

						else:
							stardateString = "Oh... Your shiny pokemon is fixed :("

					else:
						stardateString = "It's too far to calculate :("

					if squareFrame != -1:
						if squareFrame > 3:
							delta_square = datetime.timedelta(days=squareFrame - 3)
							date_square = date_pk + delta_square
							squaredateString = date_square.strftime("%Y %mM %dD")

						elif squareFrame == 3:
							squaredateString = "You succeed to open the raid den! Congratulations :)"

						else:
							squaredateString = "Oh... Your shiny pokemon is fixed :("

					else:
						squaredateString = "It's too far to calculate :("

					starFrameMessage, squareFrameMessage = self.generateFrameString(starFrame, squareFrame)

					if self.ifdetailed1 == 0: 

						await self.userChannel1.send(self.id1 + "```Pokemon : " + names[pk] +
							"\nOT : " + OT +
							"\nSeed : " + seed[2:] + 
							"\nIV: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
							"\nStar Shiny at Frame : " + starFrameMessage +
							"\nSave at this date : " + stardateString +
							"\nSquare Shiny at Frame : " + squareFrameMessage +
							"\nSave at this date : " + squaredateString +
							"```You can check more info in this website! https://leanny.github.io/seedchecker/index_old.html?seed=" + seed[2:])

					else:
						starHiddenMessage, squareHiddenMessage = self.generateAbilityString(isStarHidden, isSquareHidden)

						nature_name = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile", "Relaxed", "Impish", "Lax", "Timid", "Hasty", "Serious", "Jolly", "Naive", "Modest", "Mild", "Quiet", "Bashful", "Rash", "Calm", "Gentle", "Sassy", "Careful", "Quirky"]

						if starFrame == -1 and squareFrame == -1:
							await self.userChannel1.send(self.id1 + "```Pokemon : " + names[pk] +
							"\nOT : " + OT +
							"\nSeed : " + seed[2:] + 
							"\nIV: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
							"\nStar Shiny at Frame : Shiny frame greater than 10000! Try again :(" + 
							"```You can check more info in this website! https://leanny.github.io/seedchecker/index_old.html?seed=" + seed[2:])

						elif starFrame != -1 and squareFrame == -1:

							await self.userChannel1.send(self.id1 + "```Pokemon : " + names[pk] +
								"\nOT : " + OT +
								"\nSeed : " + seed[2:] + 
								"\nIV: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
								"\nShiny at Frame : " + starFrameMessage +
								"\nKind of Shiny : Star" +
								"\nSave at this date : " + stardateString +
								"\nAbility : " + starHiddenMessage +
								"\n5 Star IVs: " + str(stariv[0]) + "/" + str(stariv[1]) + "/" + str(stariv[2]) + "/" + str(stariv[3]) + "/" + str(stariv[4]) + "/" + str(stariv[5]) + 
								"\nNature : " + nature_name[starnature] +
								"```You can check more info in this website! https://leanny.github.io/seedchecker/index_old.html?seed=" + seed[2:])

						elif starFrame < squareFrame and starFrame != -1:

							await self.userChannel1.send(self.id1 + "```Pokemon : " + names[pk] +
								"\nOT : " + OT +
								"\nSeed : " + seed[2:] + 
								"\nIV: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
								"\nShiny at Frame : " + starFrameMessage +
								"\nKind of Shiny : Star" +
								"\nSave at this date : " + stardateString +
								"\nAbility : " + starHiddenMessage +
								"\n5 Star IVs: " + str(stariv[0]) + "/" + str(stariv[1]) + "/" + str(stariv[2]) + "/" + str(stariv[3]) + "/" + str(stariv[4]) + "/" + str(stariv[5]) + 
								"\nNature : " + nature_name[starnature] +
								"```You can check more info in this website! https://leanny.github.io/seedchecker/index_old.html?seed=" + seed[2:])

						else:

							await self.userChannel1.send(self.id1 + "```Pokemon : " + names[pk] +
								"\nOT : " + OT +
								"\nSeed : " + seed[2:] + 
								"\nIV: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
								"\nShiny at Frame : " + squareFrameMessage +
								"\nKind of Shiny : Square" +
								"\nSave at this date : " + squaredateString +
								"\nAbility : " + squareHiddenMessage +
								"\n5 Star IVs: " + str(squareiv[0]) + "/" + str(squareiv[1]) + "/" + str(squareiv[2]) + "/" + str(squareiv[3]) + "/" + str(squareiv[4]) + "/" + str(squareiv[5]) + 
								"\nNature : " + nature_name[squarenature] +
								"```You can check more info in this website! https://leanny.github.io/seedchecker/index_old.html?seed=" + seed[2:])

					#self.writeStat(self.person1, pk, starFrame, squareFrame)

					#outputs how many people remain in line
					time.sleep(1.0)
					await self.userChannel1.send("People remaining in line: " + str(q.size()))
					self.clearData1()
					removePK81()
				else:
					await self.userChannel1.send(self.id1 + ", Sorry but I couldn't find seed from " + OT + "'s " + names[pk] + ". People remaining in line: " + str(q.size()))
					self.clearData1()
					removePK81()


		#FOR 2

		#Checks if lanturn is now searching and if there is a person being served
		if checkSearchStatus2() and self.person2 != None:
			#Gets link code from text file
			code = getCodeString2()

			await self.user2.send("```python\nHi there! Your private link code is: " + code + "\nPlease use it to match up with me in trade!```")

		#Check if user has timed out and checks if a valid userChannel is present
		if checkTimeOut2() and self.userChannel2 != None:
			await self.userChannel2.send(self.id2 + " You have been timed out! You either took too long to respond or you lost connection. People remaining in line: " + str(q.size()))
			self.clearData2()

		#Check if a valid user channel is present and if the dudu client is still running
		if self.userChannel2 != None and not checkDuduStatus2():
			time.sleep(2.0)
			seed, iv, pk, year, day, month, OT = getPokeData2()

			if pk != 0:
				names = ["Egg", "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoranâ™€", "Nidorina", "Nidoqueen", "Nidoranâ™‚", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetchâ€™d", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Raikou", "Entei", "Suicune", "Larvitar", "Pupitar", "Tyranitar", "Lugia", "Ho-Oh", "Celebi", "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple", "Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo", "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Tropius", "Chimecho", "Absol", "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Regirock", "Regice", "Registeel", "Latias", "Latios", "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys", "Turtwig", "Grotle", "Torterra", "Chimchar", "Monferno", "Infernape", "Piplup", "Prinplup", "Empoleon", "Starly", "Staravia", "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune", "Shinx", "Luxio", "Luxray", "Budew", "Roserade", "Cranidos", "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam", "Mothim", "Combee", "Vespiquen", "Pachirisu", "Buizel", "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom", "Drifloon", "Drifblim", "Buneary", "Lopunny", "Mismagius", "Honchkrow", "Glameow", "Purugly", "Chingling", "Stunky", "Skuntank", "Bronzor", "Bronzong", "Bonsly", "Mime Jr.", "Happiny", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp", "Munchlax", "Riolu", "Lucario", "Hippopotas", "Hippowdon", "Skorupi", "Drapion", "Croagunk", "Toxicroak", "Carnivine", "Finneon", "Lumineon", "Mantyke", "Snover", "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth", "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z", "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom", "Uxie", "Mesprit", "Azelf", "Dialga", "Palkia", "Heatran", "Regigigas", "Giratina", "Cresselia", "Phione", "Manaphy", "Darkrai", "Shaymin", "Arceus", "Victini", "Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog", "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole", "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Basculin", "Sandile", "Krokorok", "Krookodile", "Darumaka", "Darmanitan", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask", "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark", "Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite", "Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet", "Accelgor", "Stunfisk", "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta", "Volcarona", "Cobalion", "Terrakion", "Virizion", "Tornadus", "Thundurus", "Reshiram", "Zekrom", "Landorus", "Kyurem", "Keldeo", "Meloetta", "Genesect", "Chespin", "Quilladin", "Chesnaught", "Fennekin", "Braixen", "Delphox", "Froakie", "Frogadier", "Greninja", "Bunnelby", "Diggersby", "Fletchling", "Fletchinder", "Talonflame", "Scatterbug", "Spewpa", "Vivillon", "Litleo", "Pyroar", "FlabÃ©bÃ©", "Floette", "Florges", "Skiddo", "Gogoat", "Pancham", "Pangoro", "Furfrou", "Espurr", "Meowstic", "Honedge", "Doublade", "Aegislash", "Spritzee", "Aromatisse", "Swirlix", "Slurpuff", "Inkay", "Malamar", "Binacle", "Barbaracle", "Skrelp", "Dragalge", "Clauncher", "Clawitzer", "Helioptile", "Heliolisk", "Tyrunt", "Tyrantrum", "Amaura", "Aurorus", "Sylveon", "Hawlucha", "Dedenne", "Carbink", "Goomy", "Sliggoo", "Goodra", "Klefki", "Phantump", "Trevenant", "Pumpkaboo", "Gourgeist", "Bergmite", "Avalugg", "Noibat", "Noivern", "Xerneas", "Yveltal", "Zygarde", "Diancie", "Hoopa", "Volcanion", "Rowlet", "Dartrix", "Decidueye", "Litten", "Torracat", "Incineroar", "Popplio", "Brionne", "Primarina", "Pikipek", "Trumbeak", "Toucannon", "Yungoos", "Gumshoos", "Grubbin", "Charjabug", "Vikavolt", "Crabrawler", "Crabominable", "Oricorio", "Cutiefly", "Ribombee", "Rockruff", "Lycanroc", "Wishiwashi", "Mareanie", "Toxapex", "Mudbray", "Mudsdale", "Dewpider", "Araquanid", "Fomantis", "Lurantis", "Morelull", "Shiinotic", "Salandit", "Salazzle", "Stufful", "Bewear", "Bounsweet", "Steenee", "Tsareena", "Comfey", "Oranguru", "Passimian", "Wimpod", "Golisopod", "Sandygast", "Palossand", "Pyukumuku", "Type: Null", "Silvally", "Minior", "Komala", "Turtonator", "Togedemaru", "Mimikyu", "Bruxish", "Drampa", "Dhelmise", "Jangmo-o", "Hakamo-o", "Kommo-o", "Tapu Koko", "Tapu Lele", "Tapu Bulu", "Tapu Fini", "Cosmog", "Cosmoem", "Solgaleo", "Lunala", "Nihilego", "Buzzwole", "Pheromosa", "Xurkitree", "Celesteela", "Kartana", "Guzzlord", "Necrozma", "Magearna", "Marshadow", "Poipole", "Naganadel", "Stakataka", "Blacephalon", "Zeraora", "Meltan", "Melmetal", "Grookey", "Thwackey", "Rillaboom", "Scorbunny", "Raboot", "Cinderace", "Sobble", "Drizzile", "Inteleon", "Skwovet", "Greedent", "Rookidee", "Corvisquire", "Corviknight", "Blipbug", "Dottler", "Orbeetle", "Nickit", "Thievul", "Gossifleur", "Eldegoss", "Wooloo", "Dubwool", "Chewtle", "Drednaw", "Yamper", "Boltund", "Rolycoly", "Carkol", "Coalossal", "Applin", "Flapple", "Appletun", "Silicobra", "Sandaconda", "Cramorant", "Arrokuda", "Barraskewda", "Toxel", "Toxtricity", "Sizzlipede", "Centiskorch", "Clobbopus", "Grapploct", "Sinistea", "Polteageist", "Hatenna", "Hattrem", "Hatterene", "Impidimp", "Morgrem", "Grimmsnarl", "Obstagoon", "Perrserker", "Cursola", "Sirfetchâ€™d", "Mr. Rime", "Runerigus", "Milcery", "Alcremie", "Falinks", "Pincurchin", "Snom", "Frosmoth", "Stonjourner", "Eiscue", "Indeedee", "Morpeko", "Cufant", "Copperajah", "Dracozolt", "Arctozolt", "Dracovish", "Arctovish", "Duraludon", "Dreepy", "Drakloak", "Dragapult", "Zacian", "Zamazenta", "Eternatus"]
				
				if isGiganta:
					pokemon_string = "Gigantamax " + names[pk]
				else:
					pokemon_string = names[pk]

				if seed != -1:
					calc = framecalc(seed)
					starFrame, squareFrame, isStarHidden, isSquareHidden, stariv, squareiv, starnature, squarenature = calc.getShinyFrames()
					date_pk = datetime.date(year+2000, month, day)
					if starFrame != -1:
						if starFrame > 3:
							delta_star = datetime.timedelta(days=starFrame - 3)
							date_star = date_pk + delta_star
							stardateString = date_star.strftime("%YY %mM %dD")

						elif starFrame == 3:
							stardateString = "You succeed to open the raid den! Congratulations :)"

						else:
							stardateString = "Oh... Your shiny pokemon is fixed :("

					else:
						stardateString = "It's too far to calculate :("

					if squareFrame != -1:
						if squareFrame > 3:
							delta_square = datetime.timedelta(days=squareFrame - 3)
							date_square = date_pk + delta_square
							squaredateString = date_square.strftime("%Y %mM %dD")

						elif squareFrame == 3:
							squaredateString = "You succeed to open the raid den! Congratulations :)"

						else:
							squaredateString = "Oh... Your shiny pokemon is fixed :("

					else:
						squaredateString = "It's too far to calculate :("

					starFrameMessage, squareFrameMessage = self.generateFrameString(starFrame, squareFrame)

					if self.ifdetailed2 == 0: 

						await self.userChannel2.send(self.id2 + "```Pokemon : " + names[pk] +
							"\nOT : " + OT +
							"\nSeed : " + seed[2:] + 
							"\nIV: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
							"\nStar Shiny at Frame : " + starFrameMessage +
							"\nSave at this date : " + stardateString +
							"\nSquare Shiny at Frame : " + squareFrameMessage +
							"\nSave at this date : " + squaredateString +
							"```You can check more info in this website! https://leanny.github.io/seedchecker/index_old.html?seed=" + seed[2:])

					else:
						starHiddenMessage, squareHiddenMessage = self.generateAbilityString(isStarHidden, isSquareHidden)

						nature_name = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile", "Relaxed", "Impish", "Lax", "Timid", "Hasty", "Serious", "Jolly", "Naive", "Modest", "Mild", "Quiet", "Bashful", "Rash", "Calm", "Gentle", "Sassy", "Careful", "Quirky"]

						if starFrame == -1 and squareFrame == -1:
							await self.userChannel2.send(self.id2 + "```Pokemon : " + names[pk] +
							"\nOT : " + OT +
							"\nSeed : " + seed[2:] + 
							"\nIV: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
							"\nStar Shiny at Frame : Shiny frame greater than 10000! Try again :(" + 
							"```You can check more info in this website! https://leanny.github.io/seedchecker/index_old.html?seed=" + seed[2:])

						elif starFrame != -1 and squareFrame == -1:

							await self.userChannel2.send(self.id2 + "```Pokemon : " + names[pk] +
								"\nOT : " + OT +
								"\nSeed : " + seed[2:] + 
								"\nIV: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
								"\nShiny at Frame : " + starFrameMessage +
								"\nKind of Shiny : Star" +
								"\nSave at this date : " + stardateString +
								"\nAbility : " + starHiddenMessage +
								"\n5 Star IVs: " + str(stariv[0]) + "/" + str(stariv[1]) + "/" + str(stariv[2]) + "/" + str(stariv[3]) + "/" + str(stariv[4]) + "/" + str(stariv[5]) + 
								"\nNature : " + nature_name[starnature] +
								"```You can check more info in this website! https://leanny.github.io/seedchecker/index_old.html?seed=" + seed[2:])

						elif starFrame < squareFrame and starFrame != -1:

							await self.userChannel2.send(self.id2 + "```Pokemon : " + names[pk] +
								"\nOT : " + OT +
								"\nSeed : " + seed[2:] + 
								"\nIV: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
								"\nShiny at Frame : " + starFrameMessage +
								"\nKind of Shiny : Star" +
								"\nSave at this date : " + stardateString +
								"\nAbility : " + starHiddenMessage +
								"\n5 Star IVs: " + str(stariv[0]) + "/" + str(stariv[1]) + "/" + str(stariv[2]) + "/" + str(stariv[3]) + "/" + str(stariv[4]) + "/" + str(stariv[5]) + 
								"\nNature : " + nature_name[starnature] +
								"```You can check more info in this website! https://leanny.github.io/seedchecker/index_old.html?seed=" + seed[2:])

						else:

							await self.userChannel2.send(self.id2 + "```Pokemon : " + names[pk] +
								"\nOT : " + OT +
								"\nSeed : " + seed[2:] + 
								"\nIV: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
								"\nShiny at Frame : " + squareFrameMessage +
								"\nKind of Shiny : Square" +
								"\nSave at this date : " + squaredateString +
								"\nAbility : " + squareHiddenMessage +
								"\n5 Star IVs: " + str(squareiv[0]) + "/" + str(squareiv[1]) + "/" + str(squareiv[2]) + "/" + str(squareiv[3]) + "/" + str(squareiv[4]) + "/" + str(squareiv[5]) + 
								"\nNature : " + nature_name[squarenature] +
								"```You can check more info in this website! https://leanny.github.io/seedchecker/index_old.html?seed=" + seed[2:])	

					#self.writeStat(self.person2, pk, starFrame, squareFrame)

					#outputs how many people remain in line
					time.sleep(1.0)
					await self.userChannel2.send("People remaining in line: " + str(q.size()))
					self.clearData2()
					removePK82()
				else:
					await self.userChannel2.send(self.id1 + ", Sorry but I couldn't find seed from " + OT + "'s " + names[pk] + ". People remaining in line: " + str(q.size()))
					self.clearData2()
					removePK82()	
		#await ctx.send("Invoked")		


def setup(client):
	client.add_cog(RaidCommands(client))


