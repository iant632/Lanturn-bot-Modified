class ArrayQueue:
	def __init__(self, capacity = 40):
		self._data = []
		self._size = 0
		self._capacity = capacity

	def enqueue(self, person):
		self._size += 1
		self._data.insert(0, person)

	def removeQueue(self, person):
		if self.indexOf(person) >= 0:
			self._size -= 1
			del self._data[self.indexOf(person)]

	#return self.sz < max queue size
	def availableSpace(self):
		return self._size < self.capacity()

	def dequeue(self):
		self._size -= 1
		return self._data.pop()

	def capacity(self):
		return self._capacity

	def size(self):
		return self._size

	def isEmpty(self):
		return self._size == 0

	def getQueue(self):
		return self._data

	def contains(self, person):
		return self.indexOf(person) >= 0
	
	def sendList(self):
		table = "\n"
		if self._size == 0:
			table += "No people in line.```"
			return table
		i = 0
		while i < self.size() :
			i += 1
			table += str(i) + " : " + self._data[self._size - i].user.display_name + "\n"
		table += "```"
		return table

	def indexOf(self, person):
		i = 0
		while i < self._size:
			if self._data[i].id == person.id:
				return i
			i += 1
		return -1
