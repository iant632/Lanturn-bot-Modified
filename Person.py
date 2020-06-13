class Person:
	def __init__(self, id, userChannel, user, detailed):
		self.idString = "<@"+str(id)+">"
		self.id = id
		self.userChannel = userChannel
		self.user = user
		self.detailed = detailed

	def getUser(self):
		return self.user

	def getUserChannel(self):
		return self.userChannel

	def getIDString(self):
		return self.idString

	def getID(self):
		return self.id

	def ifdetailed(self):
		return self.detailed