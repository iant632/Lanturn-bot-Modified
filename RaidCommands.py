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
		self.testMode = False
		self.msg1 = None
		self.msg2 = None

	#Clears instance variables
	def clearData1(self):
		self.userChannel1 = None
		self.user1 = None
		self.id1 = 0
		self.idInt1 = None
		self.person1 = None
		self.ifdetailed1 = None
		self.msg1 = None

	def clearData2(self):
		self.userChannel2 = None
		self.user2 = None
		self.id2 = 0
		self.person2 = None
		self.idInt2 = None
		self.ifdetailed2 = None
		self.msg2 = None

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
	
	def getDateString(self, starFrame, squareFrame, date_pk):
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

		return stardateString, squaredateString
	
	async def addList(self, ctx, number):
		global q

		if q.availableSpace():
			print("Invoked by: " + str(ctx.message.author) + " in: " + str(ctx.message.guild))
			if ctx.message.guild != None:

				#Gather the person's information
				id = ctx.message.author.id
				#Person(id, channel, author, 0) 0 means typical seed check
				p = Person(id, ctx.message.channel, ctx.message.author, number)

				#Checks if queue already contains assets from the constructed person object
				if not q.contains(p) and self.idInt1 != id and self.idInt2 != id:
					#Check if this bot is on there are no person in the queue
					var1 = self.person1 == None and is1on()
					var2 = self.person2 == None and is2on()
					if var1 or var2:
						q.enqueue(p)
						await ctx.send(str(ctx.message.author.display_name) + ", Bot dispatched, I will ping you once I start searching! There are currently no one in front of you!")

					#Check if there's no person in the queue
					else:
						q.enqueue(p)
						await ctx.send(str(ctx.message.author.display_name) + ", Bot dispatched, I will ping you once I start searching! There are currently " + str(q.size()) + " people waiting in front of you.")

				#It's your turn.
				elif self.idInt1 == id or self.idInt2== id:
					await ctx.send("It is your turn now :)")

				else:
					place = q.size() - q.indexOf(p)
					await ctx.send("There are currently " + str(place) + " people waiting in front of you.")
		else:
			await ctx.send("There are too much people so I can't add you in.")

	def getPokeName(self, pk, isGiganta, isEgg):
		names = ["Egg", "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoranâ™€", "Nidorina", "Nidoqueen", "Nidoranâ™‚", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetchâ€™d", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Raikou", "Entei", "Suicune", "Larvitar", "Pupitar", "Tyranitar", "Lugia", "Ho-Oh", "Celebi", "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple", "Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo", "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Tropius", "Chimecho", "Absol", "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Regirock", "Regice", "Registeel", "Latias", "Latios", "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys", "Turtwig", "Grotle", "Torterra", "Chimchar", "Monferno", "Infernape", "Piplup", "Prinplup", "Empoleon", "Starly", "Staravia", "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune", "Shinx", "Luxio", "Luxray", "Budew", "Roserade", "Cranidos", "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam", "Mothim", "Combee", "Vespiquen", "Pachirisu", "Buizel", "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom", "Drifloon", "Drifblim", "Buneary", "Lopunny", "Mismagius", "Honchkrow", "Glameow", "Purugly", "Chingling", "Stunky", "Skuntank", "Bronzor", "Bronzong", "Bonsly", "Mime Jr.", "Happiny", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp", "Munchlax", "Riolu", "Lucario", "Hippopotas", "Hippowdon", "Skorupi", "Drapion", "Croagunk", "Toxicroak", "Carnivine", "Finneon", "Lumineon", "Mantyke", "Snover", "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth", "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z", "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom", "Uxie", "Mesprit", "Azelf", "Dialga", "Palkia", "Heatran", "Regigigas", "Giratina", "Cresselia", "Phione", "Manaphy", "Darkrai", "Shaymin", "Arceus", "Victini", "Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog", "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole", "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Basculin", "Sandile", "Krokorok", "Krookodile", "Darumaka", "Darmanitan", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask", "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark", "Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite", "Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet", "Accelgor", "Stunfisk", "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta", "Volcarona", "Cobalion", "Terrakion", "Virizion", "Tornadus", "Thundurus", "Reshiram", "Zekrom", "Landorus", "Kyurem", "Keldeo", "Meloetta", "Genesect", "Chespin", "Quilladin", "Chesnaught", "Fennekin", "Braixen", "Delphox", "Froakie", "Frogadier", "Greninja", "Bunnelby", "Diggersby", "Fletchling", "Fletchinder", "Talonflame", "Scatterbug", "Spewpa", "Vivillon", "Litleo", "Pyroar", "FlabÃ©bÃ©", "Floette", "Florges", "Skiddo", "Gogoat", "Pancham", "Pangoro", "Furfrou", "Espurr", "Meowstic", "Honedge", "Doublade", "Aegislash", "Spritzee", "Aromatisse", "Swirlix", "Slurpuff", "Inkay", "Malamar", "Binacle", "Barbaracle", "Skrelp", "Dragalge", "Clauncher", "Clawitzer", "Helioptile", "Heliolisk", "Tyrunt", "Tyrantrum", "Amaura", "Aurorus", "Sylveon", "Hawlucha", "Dedenne", "Carbink", "Goomy", "Sliggoo", "Goodra", "Klefki", "Phantump", "Trevenant", "Pumpkaboo", "Gourgeist", "Bergmite", "Avalugg", "Noibat", "Noivern", "Xerneas", "Yveltal", "Zygarde", "Diancie", "Hoopa", "Volcanion", "Rowlet", "Dartrix", "Decidueye", "Litten", "Torracat", "Incineroar", "Popplio", "Brionne", "Primarina", "Pikipek", "Trumbeak", "Toucannon", "Yungoos", "Gumshoos", "Grubbin", "Charjabug", "Vikavolt", "Crabrawler", "Crabominable", "Oricorio", "Cutiefly", "Ribombee", "Rockruff", "Lycanroc", "Wishiwashi", "Mareanie", "Toxapex", "Mudbray", "Mudsdale", "Dewpider", "Araquanid", "Fomantis", "Lurantis", "Morelull", "Shiinotic", "Salandit", "Salazzle", "Stufful", "Bewear", "Bounsweet", "Steenee", "Tsareena", "Comfey", "Oranguru", "Passimian", "Wimpod", "Golisopod", "Sandygast", "Palossand", "Pyukumuku", "Type: Null", "Silvally", "Minior", "Komala", "Turtonator", "Togedemaru", "Mimikyu", "Bruxish", "Drampa", "Dhelmise", "Jangmo-o", "Hakamo-o", "Kommo-o", "Tapu Koko", "Tapu Lele", "Tapu Bulu", "Tapu Fini", "Cosmog", "Cosmoem", "Solgaleo", "Lunala", "Nihilego", "Buzzwole", "Pheromosa", "Xurkitree", "Celesteela", "Kartana", "Guzzlord", "Necrozma", "Magearna", "Marshadow", "Poipole", "Naganadel", "Stakataka", "Blacephalon", "Zeraora", "Meltan", "Melmetal", "Grookey", "Thwackey", "Rillaboom", "Scorbunny", "Raboot", "Cinderace", "Sobble", "Drizzile", "Inteleon", "Skwovet", "Greedent", "Rookidee", "Corvisquire", "Corviknight", "Blipbug", "Dottler", "Orbeetle", "Nickit", "Thievul", "Gossifleur", "Eldegoss", "Wooloo", "Dubwool", "Chewtle", "Drednaw", "Yamper", "Boltund", "Rolycoly", "Carkol", "Coalossal", "Applin", "Flapple", "Appletun", "Silicobra", "Sandaconda", "Cramorant", "Arrokuda", "Barraskewda", "Toxel", "Toxtricity", "Sizzlipede", "Centiskorch", "Clobbopus", "Grapploct", "Sinistea", "Polteageist", "Hatenna", "Hattrem", "Hatterene", "Impidimp", "Morgrem", "Grimmsnarl", "Obstagoon", "Perrserker", "Cursola", "Sirfetchâ€™d", "Mr. Rime", "Runerigus", "Milcery", "Alcremie", "Falinks", "Pincurchin", "Snom", "Frosmoth", "Stonjourner", "Eiscue", "Indeedee", "Morpeko", "Cufant", "Copperajah", "Dracozolt", "Arctozolt", "Dracovish", "Arctovish", "Duraludon", "Dreepy", "Drakloak", "Dragapult", "Zacian", "Zamazenta", "Eternatus"]

		if isGiganta:
			pokemon_string = "Gigantamax " + names[pk]
		else:
			pokemon_string = names[pk]
		if isEgg:
			pokemon_string = "Egg (" + pokemon_string + ")"

		return pokemon_string

	async def sendResult(self, number):
		time.sleep(1.0)
		if number == 1:
			seed, iv, pk, year, day, month, OT, isGiganta = getPokeData1()
			ifdetailed = self.ifdetailed1
			userid = self.id1
			userChannel = self.userChannel1
			msg = self.msg1
		else:
			seed, iv, pk, year, day, month, OT, isGiganta = getPokeData2()
			ifdetailed = self.ifdetailed2
			userid = self.id2
			userChannel = self.userChannel2
			msg = self.msg2

		await msg.delete()
		if pk != 0:

			pokemon_string = self.getPokeName(pk, isGiganta, False)

			if seed != -1:	
				calc = framecalc(seed)
				starFrame, squareFrame, isStarHidden, isSquareHidden, stariv, squareiv, starnature, squarenature = calc.getShinyFrames()
				date_pk = datetime.date(year+2000, month, day)

				starFrameMessage, squareFrameMessage = self.generateFrameString(starFrame, squareFrame)

				stardateString, squaredateString = self.getDateString(starFrame, squareFrame, date_pk)

				if ifdetailed == 0: 

					await userChannel.send(userid + "```Pokemon : " + pokemon_string +
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
						await userChannel.send(userid + "```Pokemon : " + pokemon_string +
						"\nOT : " + OT +
						"\nSeed : " + seed[2:] + 
						"\nIV: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
						"\nStar Shiny at Frame : Shiny frame greater than 10000! Try again :(" + 
						"```You can check more info in this website! https://leanny.github.io/seedchecker/index_old.html?seed=" + seed[2:])

					elif starFrame != -1 and squareFrame == -1:

						await userChannel.send(userid + "```Pokemon : " + pokemon_string +
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

						await userChannel.send(userid + "```Pokemon : " + pokemon_string +
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

						await userChannel.send(userid + "```Pokemon : " + pokemon_string +
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
				await userChannel.send("People remaining in line: " + str(q.size()))
			else:
				await userChannel.send(userid + ", Sorry but I couldn't find seed from " + OT + "'s " + pokemon_string + ". People remaining in line: " + str(q.size()))

	async def sendResult2(self, number):
		time.sleep(1.0)
		if number == 1:
			pk, exp, Dlevel, shiny, nature, statnature, iv, ev, move, item, OT, TID, SID, isGiganta, ability, gender, isEgg, PID, EC = getPokeInfo1()
			userChannel = self.userChannel1
			userid = self.id1
			msg = self.msg1
		else:
			pk, exp, Dlevel, shiny, nature, statnature, iv, ev, move, item, OT, TID, SID, isGiganta, ability, gender, isEgg, PID, EC = getPokeInfo2()
			userChannel = self.userChannel2
			userid = self.id2
			msg = self.msg2

		await msg.delete()

		pokemon_string = self.getPokeName(pk, isGiganta, isEgg)
		gender_name = ["Male", "Female", "None"]
		shiny_name = ["X", "☆", "◇"]
		nature_name = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile", "Relaxed", "Impish", "Lax", "Timid", "Hasty", "Serious", "Jolly", "Naive", "Modest", "Mild", "Quiet", "Bashful", "Rash", "Calm", "Gentle", "Sassy", "Careful", "Quirky"]
		ability_name = ["—", "Stench", "Drizzle", "Speed Boost", "Battle Armor", "Sturdy", "Damp", "Limber", "Sand Veil", "Static", "Volt Absorb", "Water Absorb", "Oblivious", "Cloud Nine", "Compound Eyes", "Insomnia", "Color Change", "Immunity", "Flash Fire", "Shield Dust", "Own Tempo", "Suction Cups", "Intimidate", "Shadow Tag", "Rough Skin", "Wonder Guard", "Levitate", "Effect Spore", "Synchronize", "Clear Body", "Natural Cure", "Lightning Rod", "Serene Grace", "Swift Swim", "Chlorophyll", "Illuminate", "Trace", "Huge Power", "Poison Point", "Inner Focus", "Magma Armor", "Water Veil", "Magnet Pull", "Soundproof", "Rain Dish", "Sand Stream", "Pressure", "Thick Fat", "Early Bird", "Flame Body", "Run Away", "Keen Eye", "Hyper Cutter", "Pickup", "Truant", "Hustle", "Cute Charm", "Plus", "Minus", "Forecast", "Sticky Hold", "Shed Skin", "Guts", "Marvel Scale", "Liquid Ooze", "Overgrow", "Blaze", "Torrent", "Swarm", "Rock Head", "Drought", "Arena Trap", "Vital Spirit", "White Smoke", "Pure Power", "Shell Armor", "Air Lock", "Tangled Feet", "Motor Drive", "Rivalry", "Steadfast", "Snow Cloak", "Gluttony", "Anger Point", "Unburden", "Heatproof", "Simple", "Dry Skin", "Download", "Iron Fist", "Poison Heal", "Adaptability", "Skill Link", "Hydration", "Solar Power", "Quick Feet", "Normalize", "Sniper", "Magic Guard", "No Guard", "Stall", "Technician", "Leaf Guard", "Klutz", "Mold Breaker", "Super Luck", "Aftermath", "Anticipation", "Forewarn", "Unaware", "Tinted Lens", "Filter", "Slow Start", "Scrappy", "Storm Drain", "Ice Body", "Solid Rock", "Snow Warning", "Honey Gather", "Frisk", "Reckless", "Multitype", "Flower Gift", "Bad Dreams", "Pickpocket", "Sheer Force", "Contrary", "Unnerve", "Defiant", "Defeatist", "Cursed Body", "Healer", "Friend Guard", "Weak Armor", "Heavy Metal", "Light Metal", "Multiscale", "Toxic Boost", "Flare Boost", "Harvest", "Telepathy", "Moody", "Overcoat", "Poison Touch", "Regenerator", "Big Pecks", "Sand Rush", "Wonder Skin", "Analytic", "Illusion", "Imposter", "Infiltrator", "Mummy", "Moxie", "Justified", "Rattled", "Magic Bounce", "Sap Sipper", "Prankster", "Sand Force", "Iron Barbs", "Zen Mode", "Victory Star", "Turboblaze", "Teravolt", "Aroma Veil", "Flower Veil", "Cheek Pouch", "Protean", "Fur Coat", "Magician", "Bulletproof", "Competitive", "Strong Jaw", "Refrigerate", "Sweet Veil", "Stance Change", "Gale Wings", "Mega Launcher", "Grass Pelt", "Symbiosis", "Tough Claws", "Pixilate", "Gooey", "Aerilate", "Parental Bond", "Dark Aura", "Fairy Aura", "Aura Break", "Primordial Sea", "Desolate Land", "Delta Stream", "Stamina", "Wimp Out", "Emergency Exit", "Water Compaction", "Merciless", "Shields Down", "Stakeout", "Water Bubble", "Steelworker", "Berserk", "Slush Rush", "Long Reach", "Liquid Voice", "Triage", "Galvanize", "Surge Surfer", "Schooling", "Disguise", "Battle Bond", "Power Construct", "Corrosion", "Comatose", "Queenly Majesty", "Innards Out", "Dancer", "Battery", "Fluffy", "Dazzling", "Soul-Heart", "Tangling Hair", "Receiver", "Power of Alchemy", "Beast Boost", "RKS System", "Electric Surge", "Psychic Surge", "Misty Surge", "Grassy Surge", "Full Metal Body", "Shadow Shield", "Prism Armor", "Neuroforce", "Intrepid Sword", "Dauntless Shield", "Libero", "Ball Fetch", "Cotton Down", "Propeller Tail", "Mirror Armor", "Gulp Missile", "Stalwart", "Steam Engine", "Punk Rock", "Sand Spit", "Ice Scales", "Ripen", "Ice Face", "Power Spot", "Mimicry", "Screen Cleaner", "Steely Spirit", "Perish Body", "Wandering Spirit", "Gorilla Tactics", "Neutralizing Gas", "Pastel Veil", "Hunger Switch"]
		item_name = ["None", "Master Ball", "Ultra Ball", "Great Ball", "Poké Ball", "Safari Ball", "Net Ball", "Dive Ball", "Nest Ball", "Repeat Ball", "Timer Ball", "Luxury Ball", "Premier Ball", "Dusk Ball", "Heal Ball", "Quick Ball", "Cherish Ball", "Potion", "Antidote", "Burn Heal", "Ice Heal", "Awakening", "Paralyze Heal", "Full Restore", "Max Potion", "Hyper Potion", "Super Potion", "Full Heal", "Revive", "Max Revive", "Fresh Water", "Soda Pop", "Lemonade", "Moomoo Milk", "Energy Powder", "Energy Root", "Heal Powder", "Revival Herb", "Ether", "Max Ether", "Elixir", "Max Elixir", "Lava Cookie", "Berry Juice", "Sacred Ash", "HP Up", "Protein", "Iron", "Carbos", "Calcium", "Rare Candy", "PP Up", "Zinc", "PP Max", "Old Gateau", "Guard Spec.", "Dire Hit", "X Attack", "X Defense", "X Speed", "X Accuracy", "X Sp. Atk", "X Sp. Def", "Poké Doll", "Fluffy Tail", "Blue Flute", "Yellow Flute", "Red Flute", "Black Flute", "White Flute", "Shoal Salt", "Shoal Shell", "Red Shard", "Blue Shard", "Yellow Shard", "Green Shard", "Super Repel", "Max Repel", "Escape Rope", "Repel", "Sun Stone", "Moon Stone", "Fire Stone", "Thunder Stone", "Water Stone", "Leaf Stone", "Tiny Mushroom", "Big Mushroom", "Pearl", "Big Pearl", "Stardust", "Star Piece", "Nugget", "Heart Scale", "Honey", "Growth Mulch", "Damp Mulch", "Stable Mulch", "Gooey Mulch", "Root Fossil", "Claw Fossil", "Helix Fossil", "Dome Fossil", "Old Amber", "Armor Fossil", "Skull Fossil", "Rare Bone", "Shiny Stone", "Dusk Stone", "Dawn Stone", "Oval Stone", "Odd Keystone", "Griseous Orb", "Tea", "???", "Autograph", "Douse Drive", "Shock Drive", "Burn Drive", "Chill Drive", "???", "Pokémon Box Link", "Medicine Pocket", "TM Case", "Candy Jar", "Power-Up Pocket", "Clothing Trunk", "Catching Pocket", "Battle Pocket", "???", "???", "???", "???", "???", "Sweet Heart", "Adamant Orb", "Lustrous Orb", "Greet Mail", "Favored Mail", "RSVP Mail", "Thanks Mail", "Inquiry Mail", "Like Mail", "Reply Mail", "Bridge Mail S", "Bridge Mail D", "Bridge Mail T", "Bridge Mail V", "Bridge Mail M", "Cheri Berry", "Chesto Berry", "Pecha Berry", "Rawst Berry", "Aspear Berry", "Leppa Berry", "Oran Berry", "Persim Berry", "Lum Berry", "Sitrus Berry", "Figy Berry", "Wiki Berry", "Mago Berry", "Aguav Berry", "Iapapa Berry", "Razz Berry", "Bluk Berry", "Nanab Berry", "Wepear Berry", "Pinap Berry", "Pomeg Berry", "Kelpsy Berry", "Qualot Berry", "Hondew Berry", "Grepa Berry", "Tamato Berry", "Cornn Berry", "Magost Berry", "Rabuta Berry", "Nomel Berry", "Spelon Berry", "Pamtre Berry", "Watmel Berry", "Durin Berry", "Belue Berry", "Occa Berry", "Passho Berry", "Wacan Berry", "Rindo Berry", "Yache Berry", "Chople Berry", "Kebia Berry", "Shuca Berry", "Coba Berry", "Payapa Berry", "Tanga Berry", "Charti Berry", "Kasib Berry", "Haban Berry", "Colbur Berry", "Babiri Berry", "Chilan Berry", "Liechi Berry", "Ganlon Berry", "Salac Berry", "Petaya Berry", "Apicot Berry", "Lansat Berry", "Starf Berry", "Enigma Berry", "Micle Berry", "Custap Berry", "Jaboca Berry", "Rowap Berry", "Bright Powder", "White Herb", "Macho Brace", "Exp. Share", "Quick Claw", "Soothe Bell", "Mental Herb", "Choice Band", "King’s Rock", "Silver Powder", "Amulet Coin", "Cleanse Tag", "Soul Dew", "Deep Sea Tooth", "Deep Sea Scale", "Smoke Ball", "Everstone", "Focus Band", "Lucky Egg", "Scope Lens", "Metal Coat", "Leftovers", "Dragon Scale", "Light Ball", "Soft Sand", "Hard Stone", "Miracle Seed", "Black Glasses", "Black Belt", "Magnet", "Mystic Water", "Sharp Beak", "Poison Barb", "Never-Melt Ice", "Spell Tag", "Twisted Spoon", "Charcoal", "Dragon Fang", "Silk Scarf", "Upgrade", "Shell Bell", "Sea Incense", "Lax Incense", "Lucky Punch", "Metal Powder", "Thick Club", "Leek", "Red Scarf", "Blue Scarf", "Pink Scarf", "Green Scarf", "Yellow Scarf", "Wide Lens", "Muscle Band", "Wise Glasses", "Expert Belt", "Light Clay", "Life Orb", "Power Herb", "Toxic Orb", "Flame Orb", "Quick Powder", "Focus Sash", "Zoom Lens", "Metronome", "Iron Ball", "Lagging Tail", "Destiny Knot", "Black Sludge", "Icy Rock", "Smooth Rock", "Heat Rock", "Damp Rock", "Grip Claw", "Choice Scarf", "Sticky Barb", "Power Bracer", "Power Belt", "Power Lens", "Power Band", "Power Anklet", "Power Weight", "Shed Shell", "Big Root", "Choice Specs", "Flame Plate", "Splash Plate", "Zap Plate", "Meadow Plate", "Icicle Plate", "Fist Plate", "Toxic Plate", "Earth Plate", "Sky Plate", "Mind Plate", "Insect Plate", "Stone Plate", "Spooky Plate", "Draco Plate", "Dread Plate", "Iron Plate", "Odd Incense", "Rock Incense", "Full Incense", "Wave Incense", "Rose Incense", "Luck Incense", "Pure Incense", "Protector", "Electirizer", "Magmarizer", "Dubious Disc", "Reaper Cloth", "Razor Claw", "Razor Fang", "TM01", "TM02", "TM03", "TM04", "TM05", "TM06", "TM07", "TM08", "TM09", "TM10", "TM11", "TM12", "TM13", "TM14", "TM15", "TM16", "TM17", "TM18", "TM19", "TM20", "TM21", "TM22", "TM23", "TM24", "TM25", "TM26", "TM27", "TM28", "TM29", "TM30", "TM31", "TM32", "TM33", "TM34", "TM35", "TM36", "TM37", "TM38", "TM39", "TM40", "TM41", "TM42", "TM43", "TM44", "TM45", "TM46", "TM47", "TM48", "TM49", "TM50", "TM51", "TM52", "TM53", "TM54", "TM55", "TM56", "TM57", "TM58", "TM59", "TM60", "TM61", "TM62", "TM63", "TM64", "TM65", "TM66", "TM67", "TM68", "TM69", "TM70", "TM71", "TM72", "TM73", "TM74", "TM75", "TM76", "TM77", "TM78", "TM79", "TM80", "TM81", "TM82", "TM83", "TM84", "TM85", "TM86", "TM87", "TM88", "TM89", "TM90", "TM91", "TM92", "HM01", "HM02", "HM03", "HM04", "HM05", "HM06", "???", "???", "Explorer Kit", "Loot Sack", "Rule Book", "Poké Radar", "Point Card", "Journal", "Seal Case", "Fashion Case", "Seal Bag", "Pal Pad", "Works Key", "Old Charm", "Galactic Key", "Red Chain", "Town Map", "Vs. Seeker", "Coin Case", "Old Rod", "Good Rod", "Super Rod", "Sprayduck", "Poffin Case", "Bike", "Suite Key", "Oak’s Letter", "Lunar Wing", "Member Card", "Azure Flute", "S.S. Ticket", "Contest Pass", "Magma Stone", "Parcel", "Coupon 1", "Coupon 2", "Coupon 3", "Storage Key", "Secret Potion", "Vs. Recorder", "Gracidea", "Secret Key", "Apricorn Box", "Unown Report", "Berry Pots", "Dowsing Machine", "Blue Card", "Slowpoke Tail", "Clear Bell", "Card Key", "Basement Key", "Squirt Bottle", "Red Scale", "Lost Item", "Pass", "Machine Part", "Silver Wing", "Rainbow Wing", "Mystery Egg", "Red Apricorn", "Blue Apricorn", "Yellow Apricorn", "Green Apricorn", "Pink Apricorn", "White Apricorn", "Black Apricorn", "Fast Ball", "Level Ball", "Lure Ball", "Heavy Ball", "Love Ball", "Friend Ball", "Moon Ball", "Sport Ball", "Park Ball", "Photo Album", "GB Sounds", "Tidal Bell", "Rage Candy Bar", "Data Card 01", "Data Card 02", "Data Card 03", "Data Card 04", "Data Card 05", "Data Card 06", "Data Card 07", "Data Card 08", "Data Card 09", "Data Card 10", "Data Card 11", "Data Card 12", "Data Card 13", "Data Card 14", "Data Card 15", "Data Card 16", "Data Card 17", "Data Card 18", "Data Card 19", "Data Card 20", "Data Card 21", "Data Card 22", "Data Card 23", "Data Card 24", "Data Card 25", "Data Card 26", "Data Card 27", "Jade Orb", "Lock Capsule", "Red Orb", "Blue Orb", "Enigma Stone", "Prism Scale", "Eviolite", "Float Stone", "Rocky Helmet", "Air Balloon", "Red Card", "Ring Target", "Binding Band", "Absorb Bulb", "Cell Battery", "Eject Button", "Fire Gem", "Water Gem", "Electric Gem", "Grass Gem", "Ice Gem", "Fighting Gem", "Poison Gem", "Ground Gem", "Flying Gem", "Psychic Gem", "Bug Gem", "Rock Gem", "Ghost Gem", "Dragon Gem", "Dark Gem", "Steel Gem", "Normal Gem", "Health Feather", "Muscle Feather", "Resist Feather", "Genius Feather", "Clever Feather", "Swift Feather", "Pretty Feather", "Cover Fossil", "Plume Fossil", "Liberty Pass", "Pass Orb", "Dream Ball", "Poké Toy", "Prop Case", "Dragon Skull", "Balm Mushroom", "Big Nugget", "Pearl String", "Comet Shard", "Relic Copper", "Relic Silver", "Relic Gold", "Relic Vase", "Relic Band", "Relic Statue", "Relic Crown", "Casteliacone", "Dire Hit 2", "X Speed 2", "X Sp. Atk 2", "X Sp. Def 2", "X Defense 2", "X Attack 2", "X Accuracy 2", "X Speed 3", "X Sp. Atk 3", "X Sp. Def 3", "X Defense 3", "X Attack 3", "X Accuracy 3", "X Speed 6", "X Sp. Atk 6", "X Sp. Def 6", "X Defense 6", "X Attack 6", "X Accuracy 6", "Ability Urge", "Item Drop", "Item Urge", "Reset Urge", "Dire Hit 3", "Light Stone", "Dark Stone", "TM93", "TM94", "TM95", "Xtransceiver", "???", "Gram 1", "Gram 2", "Gram 3", "Xtransceiver", "Medal Box", "DNA Splicers", "DNA Splicers", "Permit", "Oval Charm", "Shiny Charm", "Plasma Card", "Grubby Hanky", "Colress Machine", "Dropped Item", "Dropped Item", "Reveal Glass", "Weakness Policy", "Assault Vest", "Holo Caster", "Prof’s Letter", "Roller Skates", "Pixie Plate", "Ability Capsule", "Whipped Dream", "Sachet", "Luminous Moss", "Snowball", "Safety Goggles", "Poké Flute", "Rich Mulch", "Surprise Mulch", "Boost Mulch", "Amaze Mulch", "Gengarite", "Gardevoirite", "Ampharosite", "Venusaurite", "Charizardite X", "Blastoisinite", "Mewtwonite X", "Mewtwonite Y", "Blazikenite", "Medichamite", "Houndoominite", "Aggronite", "Banettite", "Tyranitarite", "Scizorite", "Pinsirite", "Aerodactylite", "Lucarionite", "Abomasite", "Kangaskhanite", "Gyaradosite", "Absolite", "Charizardite Y", "Alakazite", "Heracronite", "Mawilite", "Manectite", "Garchompite", "Latiasite", "Latiosite", "Roseli Berry", "Kee Berry", "Maranga Berry", "Sprinklotad", "TM96", "TM97", "TM98", "TM99", "TM100", "Power Plant Pass", "Mega Ring", "Intriguing Stone", "Common Stone", "Discount Coupon", "Elevator Key", "TMV Pass", "Honor of Kalos", "Adventure Guide", "Strange Souvenir", "Lens Case", "Makeup Bag", "Travel Trunk", "Lumiose Galette", "Shalour Sable", "Jaw Fossil", "Sail Fossil", "Looker Ticket", "Bike", "Holo Caster", "Fairy Gem", "Mega Charm", "Mega Glove", "Mach Bike", "Acro Bike", "Wailmer Pail", "Devon Parts", "Soot Sack", "Basement Key", "Pokéblock Kit", "Letter", "Eon Ticket", "Scanner", "Go-Goggles", "Meteorite", "Key to Room 1", "Key to Room 2", "Key to Room 4", "Key to Room 6", "Storage Key", "Devon Scope", "S.S. Ticket", "HM07", "Devon Scuba Gear", "Contest Costume", "Contest Costume", "Magma Suit", "Aqua Suit", "Pair of Tickets", "Mega Bracelet", "Mega Pendant", "Mega Glasses", "Mega Anchor", "Mega Stickpin", "Mega Tiara", "Mega Anklet", "Meteorite", "Swampertite", "Sceptilite", "Sablenite", "Altarianite", "Galladite", "Audinite", "Metagrossite", "Sharpedonite", "Slowbronite", "Steelixite", "Pidgeotite", "Glalitite", "Diancite", "Prison Bottle", "Mega Cuff", "Cameruptite", "Lopunnite", "Salamencite", "Beedrillite", "Meteorite", "Meteorite", "Key Stone", "Meteorite Shard", "Eon Flute", "Normalium Z", "Firium Z", "Waterium Z", "Electrium Z", "Grassium Z", "Icium Z", "Fightinium Z", "Poisonium Z", "Groundium Z", "Flyinium Z", "Psychium Z", "Buginium Z", "Rockium Z", "Ghostium Z", "Dragonium Z", "Darkinium Z", "Steelium Z", "Fairium Z", "Pikanium Z", "Bottle Cap", "Gold Bottle Cap", "Z-Ring", "Decidium Z", "Incinium Z", "Primarium Z", "Tapunium Z", "Marshadium Z", "Aloraichium Z", "Snorlium Z", "Eevium Z", "Mewnium Z", "Normalium Z", "Firium Z", "Waterium Z", "Electrium Z", "Grassium Z", "Icium Z", "Fightinium Z", "Poisonium Z", "Groundium Z", "Flyinium Z", "Psychium Z", "Buginium Z", "Rockium Z", "Ghostium Z", "Dragonium Z", "Darkinium Z", "Steelium Z", "Fairium Z", "Pikanium Z", "Decidium Z", "Incinium Z", "Primarium Z", "Tapunium Z", "Marshadium Z", "Aloraichium Z", "Snorlium Z", "Eevium Z", "Mewnium Z", "Pikashunium Z", "Pikashunium Z", "???", "???", "???", "???", "Forage Bag", "Fishing Rod", "Professor’s Mask", "Festival Ticket", "Sparkling Stone", "Adrenaline Orb", "Zygarde Cube", "???", "Ice Stone", "Ride Pager", "Beast Ball", "Big Malasada", "Red Nectar", "Yellow Nectar", "Pink Nectar", "Purple Nectar", "Sun Flute", "Moon Flute", "???", "Enigmatic Card", "Silver Razz Berry", "Golden Razz Berry", "Silver Nanab Berry", "Golden Nanab Berry", "Silver Pinap Berry", "Golden Pinap Berry", "???", "???", "???", "???", "???", "Secret Key", "S.S. Ticket", "Silph Scope", "Parcel", "Card Key", "Gold Teeth", "Lift Key", "Terrain Extender", "Protective Pads", "Electric Seed", "Psychic Seed", "Misty Seed", "Grassy Seed", "Stretchy Spring", "Chalky Stone", "Marble", "Lone Earring", "Beach Glass", "Gold Leaf", "Silver Leaf", "Polished Mud Ball", "Tropical Shell", "Leaf Letter", "Leaf Letter", "Small Bouquet", "???", "???", "???", "Lure", "Super Lure", "Max Lure", "Pewter Crunchies", "Fighting Memory", "Flying Memory", "Poison Memory", "Ground Memory", "Rock Memory", "Bug Memory", "Ghost Memory", "Steel Memory", "Fire Memory", "Water Memory", "Grass Memory", "Electric Memory", "Psychic Memory", "Ice Memory", "Dragon Memory", "Dark Memory", "Fairy Memory", "Solganium Z", "Lunalium Z", "Ultranecrozium Z", "Mimikium Z", "Lycanium Z", "Kommonium Z", "Solganium Z", "Lunalium Z", "Ultranecrozium Z", "Mimikium Z", "Lycanium Z", "Kommonium Z", "Z-Power Ring", "Pink Petal", "Orange Petal", "Blue Petal", "Red Petal", "Green Petal", "Yellow Petal", "Purple Petal", "Rainbow Flower", "Surge Badge", "N-Solarizer", "N-Lunarizer", "N-Solarizer", "N-Lunarizer", "Ilima Normalium Z", "Left Poké Ball", "Roto Hatch", "Roto Bargain", "Roto Prize Money", "Roto Exp. Points", "Roto Friendship", "Roto Encounter", "Roto Stealth", "Roto HP Restore", "Roto PP Restore", "Roto Boost", "Roto Catch", "Health Candy", "Mighty Candy", "Tough Candy", "Smart Candy", "Courage Candy", "Quick Candy", "Health Candy L", "Mighty Candy L", "Tough Candy L", "Smart Candy L", "Courage Candy L", "Quick Candy L", "Health Candy XL", "Mighty Candy XL", "Tough Candy XL", "Smart Candy XL", "Courage Candy XL", "Quick Candy XL", "Bulbasaur Candy", "Charmander Candy", "Squirtle Candy", "Caterpie Candy", "Weedle Candy", "Pidgey Candy", "Rattata Candy", "Spearow Candy", "Ekans Candy", "Pikachu Candy", "Sandshrew Candy", "Nidoran♀ Candy", "Nidoran♂ Candy", "Clefairy Candy", "Vulpix Candy", "Jigglypuff Candy", "Zubat Candy", "Oddish Candy", "Paras Candy", "Venonat Candy", "Diglett Candy", "Meowth Candy", "Psyduck Candy", "Mankey Candy", "Growlithe Candy", "Poliwag Candy", "Abra Candy", "Machop Candy", "Bellsprout Candy", "Tentacool Candy", "Geodude Candy", "Ponyta Candy", "Slowpoke Candy", "Magnemite Candy", "Farfetch’d Candy", "Doduo Candy", "Seel Candy", "Grimer Candy", "Shellder Candy", "Gastly Candy", "Onix Candy", "Drowzee Candy", "Krabby Candy", "Voltorb Candy", "Exeggcute Candy", "Cubone Candy", "Hitmonlee Candy", "Hitmonchan Candy", "Lickitung Candy", "Koffing Candy", "Rhyhorn Candy", "Chansey Candy", "Tangela Candy", "Kangaskhan Candy", "Horsea Candy", "Goldeen Candy", "Staryu Candy", "Mr. Mime Candy", "Scyther Candy", "Jynx Candy", "Electabuzz Candy", "Pinsir Candy", "Tauros Candy", "Magikarp Candy", "Lapras Candy", "Ditto Candy", "Eevee Candy", "Porygon Candy", "Omanyte Candy", "Kabuto Candy", "Aerodactyl Candy", "Snorlax Candy", "Articuno Candy", "Zapdos Candy", "Moltres Candy", "Dratini Candy", "Mewtwo Candy", "Mew Candy", "Meltan Candy", "Magmar Candy", "???", "???", "???", "???", "???", "???", "???", "???", "???", "???", "???", "???", "???", "???", "???", "???", "Endorsement", "Pokémon Box Link", "Wishing Star", "Dynamax Band", "???", "???", "Fishing Rod", "Rotom Bike", "???", "???", "Sausages", "Bob’s Food Tin", "Bach’s Food Tin", "Tin of Beans", "Bread", "Pasta", "Mixed Mushrooms", "Smoke-Poke Tail", "Large Leek", "Fancy Apple", "Brittle Bones", "Pack of Potatoes", "Pungent Root", "Salad Mix", "Fried Food", "Boiled Egg", "Camping Gear", "???", "???", "Rusted Sword", "Rusted Shield", "Fossilized Bird", "Fossilized Fish", "Fossilized Drake", "Fossilized Dino", "Strawberry Sweet", "Love Sweet", "Berry Sweet", "Clover Sweet", "Flower Sweet", "Star Sweet", "Ribbon Sweet", "Sweet Apple", "Tart Apple", "Throat Spray", "Eject Pack", "Heavy-Duty Boots", "Blunder Policy", "Room Service", "Utility Umbrella", "Exp. Candy XS", "Exp. Candy S", "Exp. Candy M", "Exp. Candy L", "Exp. Candy XL", "Dynamax Candy", "TR00", "TR01", "TR02", "TR03", "TR04", "TR05", "TR06", "TR07", "TR08", "TR09", "TR10", "TR11", "TR12", "TR13", "TR14", "TR15", "TR16", "TR17", "TR18", "TR19", "TR20", "TR21", "TR22", "TR23", "TR24", "TR25", "TR26", "TR27", "TR28", "TR29", "TR30", "TR31", "TR32", "TR33", "TR34", "TR35", "TR36", "TR37", "TR38", "TR39", "TR40", "TR41", "TR42", "TR43", "TR44", "TR45", "TR46", "TR47", "TR48", "TR49", "TR50", "TR51", "TR52", "TR53", "TR54", "TR55", "TR56", "TR57", "TR58", "TR59", "TR60", "TR61", "TR62", "TR63", "TR64", "TR65", "TR66", "TR67", "TR68", "TR69", "TR70", "TR71", "TR72", "TR73", "TR74", "TR75", "TR76", "TR77", "TR78", "TR79", "TR80", "TR81", "TR82", "TR83", "TR84", "TR85", "TR86", "TR87", "TR88", "TR89", "TR90", "TR91", "TR92", "TR93", "TR94", "TR95", "TR96", "TR97", "TR98", "TR99", "TM00", "Lonely Mint", "Adamant Mint", "Naughty Mint", "Brave Mint", "Bold Mint", "Impish Mint", "Lax Mint", "Relaxed Mint", "Modest Mint", "Mild Mint", "Rash Mint", "Quiet Mint", "Calm Mint", "Gentle Mint", "Careful Mint", "Sassy Mint", "Timid Mint", "Hasty Mint", "Jolly Mint", "Naive Mint", "Serious Mint", "Wishing Piece", "Cracked Pot", "Chipped Pot", "Hi-tech Earbuds", "Fruit Bunch", "Moomoo Cheese", "Spice Mix", "Fresh Cream", "Packaged Curry", "Coconut Milk", "Instant Noodles", "Precooked Burger", "Gigantamix", "Wishing Chip", "Rotom Bike", "Catching Charm", "???", "Old Letter", "Band Autograph", "Sonia’s Book", "???", "???", "???", "???", "???", "???", "Rotom Catalog", "★And458", "★And15", "★And337", "★And603", "★And390", "★Sgr6879", "★Sgr6859", "★Sgr6913", "★Sgr7348", "★Sgr7121", "★Sgr6746", "★Sgr7194", "★Sgr7337", "★Sgr7343", "★Sgr6812", "★Sgr7116", "★Sgr7264", "★Sgr7597", "★Del7882", "★Del7906", "★Del7852", "★Psc596", "★Psc361", "★Psc510", "★Psc437", "★Psc8773", "★Lep1865", "★Lep1829", "★Boo5340", "★Boo5506", "★Boo5435", "★Boo5602", "★Boo5733", "★Boo5235", "★Boo5351", "★Hya3748", "★Hya3903", "★Hya3418", "★Hya3482", "★Hya3845", "★Eri1084", "★Eri472", "★Eri1666", "★Eri897", "★Eri1231", "★Eri874", "★Eri1298", "★Eri1325", "★Eri984", "★Eri1464", "★Eri1393", "★Eri850", "★Tau1409", "★Tau1457", "★Tau1165", "★Tau1791", "★Tau1910", "★Tau1346", "★Tau1373", "★Tau1412", "★CMa2491", "★CMa2693", "★CMa2294", "★CMa2827", "★CMa2282", "★CMa2618", "★CMa2657", "★CMa2646", "★UMa4905", "★UMa4301", "★UMa5191", "★UMa5054", "★UMa4295", "★UMa4660", "★UMa4554", "★UMa4069", "★UMa3569", "★UMa3323", "★UMa4033", "★UMa4377", "★UMa4375", "★UMa4518", "★UMa3594", "★Vir5056", "★Vir4825", "★Vir4932", "★Vir4540", "★Vir4689", "★Vir5338", "★Vir4910", "★Vir5315", "★Vir5359", "★Vir5409", "★Vir5107", "★Ari617", "★Ari553", "★Ari546", "★Ari951", "★Ori1713", "★Ori2061", "★Ori1790", "★Ori1903", "★Ori1948", "★Ori2004", "★Ori1852", "★Ori1879", "★Ori1899", "★Ori1543", "★Cas21", "★Cas168", "★Cas403", "★Cas153", "★Cas542", "★Cas219", "★Cas265", "★Cnc3572", "★Cnc3208", "★Cnc3461", "★Cnc3449", "★Cnc3429", "★Cnc3627", "★Cnc3268", "★Cnc3249", "★Com4968", "★Crv4757", "★Crv4623", "★Crv4662", "★Crv4786", "★Aur1708", "★Aur2088", "★Aur1605", "★Aur2095", "★Aur1577", "★Aur1641", "★Aur1612", "★Pav7790", "★Cet911", "★Cet681", "★Cet188", "★Cet539", "★Cet804", "★Cep8974", "★Cep8162", "★Cep8238", "★Cep8417", "★Cen5267", "★Cen5288", "★Cen551", "★Cen5459", "★Cen5460", "★CMi2943", "★CMi2845", "★Equ8131", "★Vul7405", "★UMi424", "★UMi5563", "★UMi5735", "★UMi6789", "★Crt4287", "★Lyr7001", "★Lyr7178", "★Lyr7106", "★Lyr7298", "★Ara6585", "★Sco6134", "★Sco6527", "★Sco6553", "★Sco5953", "★Sco5984", "★Sco6508", "★Sco6084", "★Sco5944", "★Sco6630", "★Sco6027", "★Sco6247", "★Sco6252", "★Sco5928", "★Sco6241", "★Sco6165", "★Tri544", "★Leo3982", "★Leo4534", "★Leo4357", "★Leo4057", "★Leo4359", "★Leo4031", "★Leo3852", "★Leo3905", "★Leo3773", "★Gru8425", "★Gru8636", "★Gru8353", "★Lib5685", "★Lib5531", "★Lib5787", "★Lib5603", "★Pup3165", "★Pup3185", "★Pup3045", "★Cyg7924", "★Cyg7417", "★Cyg7796", "★Cyg8301", "★Cyg7949", "★Cyg7528", "★Oct7228", "★Col1956", "★Col2040", "★Col2177", "★Gem2990", "★Gem2891", "★Gem2421", "★Gem2473", "★Gem2216", "★Gem2777", "★Gem2650", "★Gem2286", "★Gem2484", "★Gem2930", "★Peg8775", "★Peg8781", "★Peg39", "★Peg8308", "★Peg8650", "★Peg8634", "★Peg8684", "★Peg8450", "★Peg8880", "★Peg8905", "★Oph6556", "★Oph6378", "★Oph6603", "★Oph6149", "★Oph6056", "★Oph6075", "★Ser5854", "★Ser7141", "★Ser5879", "★Her6406", "★Her6148", "★Her6410", "★Her6526", "★Her6117", "★Her6008", "★Per936", "★Per1017", "★Per1131", "★Per1228", "★Per834", "★Per941", "★Phe99", "★Phe338", "★Vel3634", "★Vel3485", "★Vel3734", "★Aqr8232", "★Aqr8414", "★Aqr8709", "★Aqr8518", "★Aqr7950", "★Aqr8499", "★Aqr8610", "★Aqr8264", "★Cru4853", "★Cru4730", "★Cru4763", "★Cru4700", "★Cru4656", "★PsA8728", "★TrA6217", "★Cap7776", "★Cap7754", "★Cap8278", "★Cap8322", "★Cap7773", "★Sge7479", "★Car2326", "★Car3685", "★Car3307", "★Car3699", "★Dra5744", "★Dra5291", "★Dra6705", "★Dra6536", "★Dra7310", "★Dra6688", "★Dra4434", "★Dra6370", "★Dra7462", "★Dra6396", "★Dra6132", "★Dra6636", "★CVn4915", "★CVn4785", "★CVn4846", "★Aql7595", "★Aql7557", "★Aql7525", "★Aql7602", "★Aql7235"]
		move_name = ["———", "Pound", "Karate Chop", "Double Slap", "Comet Punch", "Mega Punch", "Pay Day", "Fire Punch", "Ice Punch", "Thunder Punch", "Scratch", "Vise Grip", "Guillotine", "Razor Wind", "Swords Dance", "Cut", "Gust", "Wing Attack", "Whirlwind", "Fly", "Bind", "Slam", "Vine Whip", "Stomp", "Double Kick", "Mega Kick", "Jump Kick", "Rolling Kick", "Sand Attack", "Headbutt", "Horn Attack", "Fury Attack", "Horn Drill", "Tackle", "Body Slam", "Wrap", "Take Down", "Thrash", "Double-Edge", "Tail Whip", "Poison Sting", "Twineedle", "Pin Missile", "Leer", "Bite", "Growl", "Roar", "Sing", "Supersonic", "Sonic Boom", "Disable", "Acid", "Ember", "Flamethrower", "Mist", "Water Gun", "Hydro Pump", "Surf", "Ice Beam", "Blizzard", "Psybeam", "Bubble Beam", "Aurora Beam", "Hyper Beam", "Peck", "Drill Peck", "Submission", "Low Kick", "Counter", "Seismic Toss", "Strength", "Absorb", "Mega Drain", "Leech Seed", "Growth", "Razor Leaf", "Solar Beam", "Poison Powder", "Stun Spore", "Sleep Powder", "Petal Dance", "String Shot", "Dragon Rage", "Fire Spin", "Thunder Shock", "Thunderbolt", "Thunder Wave", "Thunder", "Rock Throw", "Earthquake", "Fissure", "Dig", "Toxic", "Confusion", "Psychic", "Hypnosis", "Meditate", "Agility", "Quick Attack", "Rage", "Teleport", "Night Shade", "Mimic", "Screech", "Double Team", "Recover", "Harden", "Minimize", "Smokescreen", "Confuse Ray", "Withdraw", "Defense Curl", "Barrier", "Light Screen", "Haze", "Reflect", "Focus Energy", "Bide", "Metronome", "Mirror Move", "Self-Destruct", "Egg Bomb", "Lick", "Smog", "Sludge", "Bone Club", "Fire Blast", "Waterfall", "Clamp", "Swift", "Skull Bash", "Spike Cannon", "Constrict", "Amnesia", "Kinesis", "Soft-Boiled", "High Jump Kick", "Glare", "Dream Eater", "Poison Gas", "Barrage", "Leech Life", "Lovely Kiss", "Sky Attack", "Transform", "Bubble", "Dizzy Punch", "Spore", "Flash", "Psywave", "Splash", "Acid Armor", "Crabhammer", "Explosion", "Fury Swipes", "Bonemerang", "Rest", "Rock Slide", "Hyper Fang", "Sharpen", "Conversion", "Tri Attack", "Super Fang", "Slash", "Substitute", "Struggle", "Sketch", "Triple Kick", "Thief", "Spider Web", "Mind Reader", "Nightmare", "Flame Wheel", "Snore", "Curse", "Flail", "Conversion 2", "Aeroblast", "Cotton Spore", "Reversal", "Spite", "Powder Snow", "Protect", "Mach Punch", "Scary Face", "Feint Attack", "Sweet Kiss", "Belly Drum", "Sludge Bomb", "Mud-Slap", "Octazooka", "Spikes", "Zap Cannon", "Foresight", "Destiny Bond", "Perish Song", "Icy Wind", "Detect", "Bone Rush", "Lock-On", "Outrage", "Sandstorm", "Giga Drain", "Endure", "Charm", "Rollout", "False Swipe", "Swagger", "Milk Drink", "Spark", "Fury Cutter", "Steel Wing", "Mean Look", "Attract", "Sleep Talk", "Heal Bell", "Return", "Present", "Frustration", "Safeguard", "Pain Split", "Sacred Fire", "Magnitude", "Dynamic Punch", "Megahorn", "Dragon Breath", "Baton Pass", "Encore", "Pursuit", "Rapid Spin", "Sweet Scent", "Iron Tail", "Metal Claw", "Vital Throw", "Morning Sun", "Synthesis", "Moonlight", "Hidden Power", "Cross Chop", "Twister", "Rain Dance", "Sunny Day", "Crunch", "Mirror Coat", "Psych Up", "Extreme Speed", "Ancient Power", "Shadow Ball", "Future Sight", "Rock Smash", "Whirlpool", "Beat Up", "Fake Out", "Uproar", "Stockpile", "Spit Up", "Swallow", "Heat Wave", "Hail", "Torment", "Flatter", "Will-O-Wisp", "Memento", "Facade", "Focus Punch", "Smelling Salts", "Follow Me", "Nature Power", "Charge", "Taunt", "Helping Hand", "Trick", "Role Play", "Wish", "Assist", "Ingrain", "Superpower", "Magic Coat", "Recycle", "Revenge", "Brick Break", "Yawn", "Knock Off", "Endeavor", "Eruption", "Skill Swap", "Imprison", "Refresh", "Grudge", "Snatch", "Secret Power", "Dive", "Arm Thrust", "Camouflage", "Tail Glow", "Luster Purge", "Mist Ball", "Feather Dance", "Teeter Dance", "Blaze Kick", "Mud Sport", "Ice Ball", "Needle Arm", "Slack Off", "Hyper Voice", "Poison Fang", "Crush Claw", "Blast Burn", "Hydro Cannon", "Meteor Mash", "Astonish", "Weather Ball", "Aromatherapy", "Fake Tears", "Air Cutter", "Overheat", "Odor Sleuth", "Rock Tomb", "Silver Wind", "Metal Sound", "Grass Whistle", "Tickle", "Cosmic Power", "Water Spout", "Signal Beam", "Shadow Punch", "Extrasensory", "Sky Uppercut", "Sand Tomb", "Sheer Cold", "Muddy Water", "Bullet Seed", "Aerial Ace", "Icicle Spear", "Iron Defense", "Block", "Howl", "Dragon Claw", "Frenzy Plant", "Bulk Up", "Bounce", "Mud Shot", "Poison Tail", "Covet", "Volt Tackle", "Magical Leaf", "Water Sport", "Calm Mind", "Leaf Blade", "Dragon Dance", "Rock Blast", "Shock Wave", "Water Pulse", "Doom Desire", "Psycho Boost", "Roost", "Gravity", "Miracle Eye", "Wake-Up Slap", "Hammer Arm", "Gyro Ball", "Healing Wish", "Brine", "Natural Gift", "Feint", "Pluck", "Tailwind", "Acupressure", "Metal Burst", "U-turn", "Close Combat", "Payback", "Assurance", "Embargo", "Fling", "Psycho Shift", "Trump Card", "Heal Block", "Wring Out", "Power Trick", "Gastro Acid", "Lucky Chant", "Me First", "Copycat", "Power Swap", "Guard Swap", "Punishment", "Last Resort", "Worry Seed", "Sucker Punch", "Toxic Spikes", "Heart Swap", "Aqua Ring", "Magnet Rise", "Flare Blitz", "Force Palm", "Aura Sphere", "Rock Polish", "Poison Jab", "Dark Pulse", "Night Slash", "Aqua Tail", "Seed Bomb", "Air Slash", "X-Scissor", "Bug Buzz", "Dragon Pulse", "Dragon Rush", "Power Gem", "Drain Punch", "Vacuum Wave", "Focus Blast", "Energy Ball", "Brave Bird", "Earth Power", "Switcheroo", "Giga Impact", "Nasty Plot", "Bullet Punch", "Avalanche", "Ice Shard", "Shadow Claw", "Thunder Fang", "Ice Fang", "Fire Fang", "Shadow Sneak", "Mud Bomb", "Psycho Cut", "Zen Headbutt", "Mirror Shot", "Flash Cannon", "Rock Climb", "Defog", "Trick Room", "Draco Meteor", "Discharge", "Lava Plume", "Leaf Storm", "Power Whip", "Rock Wrecker", "Cross Poison", "Gunk Shot", "Iron Head", "Magnet Bomb", "Stone Edge", "Captivate", "Stealth Rock", "Grass Knot", "Chatter", "Judgment", "Bug Bite", "Charge Beam", "Wood Hammer", "Aqua Jet", "Attack Order", "Defend Order", "Heal Order", "Head Smash", "Double Hit", "Roar of Time", "Spacial Rend", "Lunar Dance", "Crush Grip", "Magma Storm", "Dark Void", "Seed Flare", "Ominous Wind", "Shadow Force", "Hone Claws", "Wide Guard", "Guard Split", "Power Split", "Wonder Room", "Psyshock", "Venoshock", "Autotomize", "Rage Powder", "Telekinesis", "Magic Room", "Smack Down", "Storm Throw", "Flame Burst", "Sludge Wave", "Quiver Dance", "Heavy Slam", "Synchronoise", "Electro Ball", "Soak", "Flame Charge", "Coil", "Low Sweep", "Acid Spray", "Foul Play", "Simple Beam", "Entrainment", "After You", "Round", "Echoed Voice", "Chip Away", "Clear Smog", "Stored Power", "Quick Guard", "Ally Switch", "Scald", "Shell Smash", "Heal Pulse", "Hex", "Sky Drop", "Shift Gear", "Circle Throw", "Incinerate", "Quash", "Acrobatics", "Reflect Type", "Retaliate", "Final Gambit", "Bestow", "Inferno", "Water Pledge", "Fire Pledge", "Grass Pledge", "Volt Switch", "Struggle Bug", "Bulldoze", "Frost Breath", "Dragon Tail", "Work Up", "Electroweb", "Wild Charge", "Drill Run", "Dual Chop", "Heart Stamp", "Horn Leech", "Sacred Sword", "Razor Shell", "Heat Crash", "Leaf Tornado", "Steamroller", "Cotton Guard", "Night Daze", "Psystrike", "Tail Slap", "Hurricane", "Head Charge", "Gear Grind", "Searing Shot", "Techno Blast", "Relic Song", "Secret Sword", "Glaciate", "Bolt Strike", "Blue Flare", "Fiery Dance", "Freeze Shock", "Ice Burn", "Snarl", "Icicle Crash", "V-create", "Fusion Flare", "Fusion Bolt", "Flying Press", "Mat Block", "Belch", "Rototiller", "Sticky Web", "Fell Stinger", "Phantom Force", "Trick-or-Treat", "Noble Roar", "Ion Deluge", "Parabolic Charge", "Forest’s Curse", "Petal Blizzard", "Freeze-Dry", "Disarming Voice", "Parting Shot", "Topsy-Turvy", "Draining Kiss", "Crafty Shield", "Flower Shield", "Grassy Terrain", "Misty Terrain", "Electrify", "Play Rough", "Fairy Wind", "Moonblast", "Boomburst", "Fairy Lock", "King’s Shield", "Play Nice", "Confide", "Diamond Storm", "Steam Eruption", "Hyperspace Hole", "Water Shuriken", "Mystical Fire", "Spiky Shield", "Aromatic Mist", "Eerie Impulse", "Venom Drench", "Powder", "Geomancy", "Magnetic Flux", "Happy Hour", "Electric Terrain", "Dazzling Gleam", "Celebrate", "Hold Hands", "Baby-Doll Eyes", "Nuzzle", "Hold Back", "Infestation", "Power-Up Punch", "Oblivion Wing", "Thousand Arrows", "Thousand Waves", "Land’s Wrath", "Light of Ruin", "Origin Pulse", "Precipice Blades", "Dragon Ascent", "Hyperspace Fury", "Breakneck Blitz", "Breakneck Blitz", "All-Out Pummeling", "All-Out Pummeling", "Supersonic Skystrike", "Supersonic Skystrike", "Acid Downpour", "Acid Downpour", "Tectonic Rage", "Tectonic Rage", "Continental Crush", "Continental Crush", "Savage Spin-Out", "Savage Spin-Out", "Never-Ending Nightmare", "Never-Ending Nightmare", "Corkscrew Crash", "Corkscrew Crash", "Inferno Overdrive", "Inferno Overdrive", "Hydro Vortex", "Hydro Vortex", "Bloom Doom", "Bloom Doom", "Gigavolt Havoc", "Gigavolt Havoc", "Shattered Psyche", "Shattered Psyche", "Subzero Slammer", "Subzero Slammer", "Devastating Drake", "Devastating Drake", "Black Hole Eclipse", "Black Hole Eclipse", "Twinkle Tackle", "Twinkle Tackle", "Catastropika", "Shore Up", "First Impression", "Baneful Bunker", "Spirit Shackle", "Darkest Lariat", "Sparkling Aria", "Ice Hammer", "Floral Healing", "High Horsepower", "Strength Sap", "Solar Blade", "Leafage", "Spotlight", "Toxic Thread", "Laser Focus", "Gear Up", "Throat Chop", "Pollen Puff", "Anchor Shot", "Psychic Terrain", "Lunge", "Fire Lash", "Power Trip", "Burn Up", "Speed Swap", "Smart Strike", "Purify", "Revelation Dance", "Core Enforcer", "Trop Kick", "Instruct", "Beak Blast", "Clanging Scales", "Dragon Hammer", "Brutal Swing", "Aurora Veil", "Sinister Arrow Raid", "Malicious Moonsault", "Oceanic Operetta", "Guardian of Alola", "Soul-Stealing 7-Star Strike", "Stoked Sparksurfer", "Pulverizing Pancake", "Extreme Evoboost", "Genesis Supernova", "Shell Trap", "Fleur Cannon", "Psychic Fangs", "Stomping Tantrum", "Shadow Bone", "Accelerock", "Liquidation", "Prismatic Laser", "Spectral Thief", "Sunsteel Strike", "Moongeist Beam", "Tearful Look", "Zing Zap", "Nature’s Madness", "Multi-Attack", "10,000,000 Volt Thunderbolt", "Mind Blown", "Plasma Fists", "Photon Geyser", "Light That Burns the Sky", "Searing Sunraze Smash", "Menacing Moonraze Maelstrom", "Let’s Snuggle Forever", "Splintered Stormshards", "Clangorous Soulblaze", "Zippy Zap", "Splishy Splash", "Floaty Fall", "Pika Papow", "Bouncy Bubble", "Buzzy Buzz", "Sizzly Slide", "Glitzy Glow", "Baddy Bad", "Sappy Seed", "Freezy Frost", "Sparkly Swirl", "Veevee Volley", "Double Iron Bash", "Max Guard", "Dynamax Cannon", "Snipe Shot", "Jaw Lock", "Stuff Cheeks", "No Retreat", "Tar Shot", "Magic Powder", "Dragon Darts", "Teatime", "Octolock", "Bolt Beak", "Fishious Rend", "Court Change", "Max Flare", "Max Flutterby", "Max Lightning", "Max Strike", "Max Knuckle", "Max Phantasm", "Max Hailstorm", "Max Ooze", "Max Geyser", "Max Airstream", "Max Starfall", "Max Wyrmwind", "Max Mindstorm", "Max Rockfall", "Max Quake", "Max Darkness", "Max Overgrowth", "Max Steelspike", "Clangorous Soul", "Body Press", "Decorate", "Drum Beating", "Snap Trap", "Pyro Ball", "Behemoth Blade", "Behemoth Bash", "Aura Wheel", "Breaking Swipe", "Branch Poke", "Overdrive", "Apple Acid", "Grav Apple", "Spirit Break", "Strange Steam", "Life Dew", "Obstruct", "False Surrender", "Meteor Assault", "Eternabeam", "Steel Beam"]

		await userChannel.send(userid + "```" + pokemon_string + " @ " + item_name[item] +
			"\nGender: " + gender_name[gender] +
			"\nExp: " + str(exp) +
			"\nDynamax Level: " + str(Dlevel) +
			"\nIVs: " + str(iv[0]) + "/" + str(iv[1]) + "/" + str(iv[2]) + "/" + str(iv[3]) + "/" + str(iv[4]) + "/" + str(iv[5]) + 
			"\nEVs: " + str(ev[0]) + "/" + str(ev[1]) + "/" + str(ev[2]) + "/" + str(ev[3]) + "/" + str(ev[4]) + "/" + str(ev[5]) + 
			"\nAbility: " + ability_name[ability] +
			"\nShiny: " + shiny_name[shiny] +
			"\nNature: " + nature_name[nature] +
			"\nStat Nature: " + nature_name[statnature] +
			"\n" + move_name[move[0]] + "/" + move_name[move[1]] + "/" + move_name[move[2]] + "/" + move_name[move[3]] +
			"\n\nOT: " + OT +
			"\nTID: " + str(TID).zfill(6) +
			"\nSID: " + str(SID).zfill(4) +
			"\nPID: " + str(hex(PID)) +
			"\nEC: " + str(hex(EC)) + "```")
		
		time.sleep(1.0)
		await userChannel.send("People remaining in line: " + str(q.size()))
		
	#Send Trade Line
	@commands.command(name="tradeList")
	async def sendList(self, ctx):
		global q
		list_text = "Current Bot trade line.\n```"
		if self.user1 != None:
			list_text += "First Nintendo Switch user" + self.user1.name
		else:
			if is1on():
				list_text += "First Nintendo Switch user : None."
			else:
				list_text += "First Nintendo Switch is offline."

		if self.user2 != None:
			list_text += "\nSecond Nintendo Switch user : " + self.user2.name
		else:
			if is2on():
				list_text += "\nSecond Nintendo Switch user : None."
			else:
				list_text += "\nSecond Nintendo Switch is offline."

		list_text += q.sendList()

		await ctx.send(list_text)

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
		await self.addList(ctx, 0)

	#Check Seed Info
	@commands.command(name="CheckSeedInfo")
	async def checkMySeed2(self, ctx):
		await self.addList(ctx, 1)
			
	#Check Seed Info
	@commands.command(name="CheckPokeInfo")
	async def checkMySeed3(self, ctx):
		await self.addList(ctx, 2)


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
			self.msg1 = await self.userChannel1.send("```Nintendo Switch 1 : I'm writing a private link code for " + self.user1.name + ".```")

		if checkPassword1() and self.person1 != None:
			await self.msg1.delete()
			self.msg1 = await self.userChannel1.send("```Nintendo Switch 1 : I wrote a private link code for " + self.user1.name + " and waiting.```")

		if checkMeet1() and self.person1 != None:
			username = getUserName1()
			await self.msg1.delete()
			self.msg1 = await self.userChannel1.send("```Nintendo Switch 1 : I met " + username + " in link trade!```")

		#Check if user has timed out and checks if a valid userChannel is present
		if checkTimeOut1() and self.userChannel1 != None:
			await self.msg1.delete()
			await self.userChannel1.send(self.id1 + " You have been timed out! You either took too long to respond or you lost connection. People remaining in line: " + str(q.size()))
			self.clearData1()

		#Check if a valid user channel is present and if the dudu client is still running
		if self.userChannel1 != None and not checkDuduStatus1():
			if self.ifdetailed1 != 2:
				self.sendResult(1)
				self.clearData1()
				removePK81()

			else:
				self.sendResult2(1)
				self.clearData1()
				removePK81()


		#FOR 2

		#Checks if lanturn is now searching and if there is a person being served
		if checkSearchStatus2() and self.person2 != None:
			#Gets link code from text file
			code = getCodeString2()

			await self.user2.send("```python\nHi there! Your private link code is: " + code + "\nPlease use it to match up with me in trade!```")
			self.msg2 = await self.userChannel2.send("```Nintendo Switch 2 : I'm writing a private link code for " + self.user2.name + ".```")

		if checkPassword2() and self.person2 != None:
			await self.msg2.delete()
			self.msg2 = await self.userChannel2.send("```Nintendo Switch 2 : I wrote a private link code for " + self.user2.name + " and waiting.```")

		if checkMeet2() and self.person2 != None:
			username = getUserName2()
			await self.msg2.delete()
			self.msg2 = await self.userChannel2.send("```Nintendo Switch 2 : I met " + username + " in link trade!```")

		#Check if user has timed out and checks if a valid userChannel is present
		if checkTimeOut2() and self.userChannel2 != None:
			await self.msg2.delete()
			await self.userChannel2.send(self.id2 + " You have been timed out! You either took too long to respond or you lost connection. People remaining in line: " + str(q.size()))
			self.clearData2()

		#Check if a valid user channel is present and if the dudu client is still running
		if self.userChannel2 != None and not checkDuduStatus2():
			if self.ifdetailed2 != 2:
				self.sendResult(2)
				self.clearData2()
				removePK82()

			else:
				self.sendResult2(2)
				self.clearData2()
				removePK82()
		#await ctx.send("Invoked")		


def setup(client):
	client.add_cog(RaidCommands(client))


