import struct
import sys
import z3
from XoroShiro import *


#Functions originally from Admiral-Fish's script
#Some modifications made to accomodate the bot's purpose
class seedgen:
	def __init__(self):
		pass

	def sym_xoroshiro128plus(self, sym_s0, sym_s1, result):
		sym_r = (sym_s0 + sym_s1) & 0xFFFFFFFF	
		condition = sym_r == result

		sym_s0, sym_s1 = self.sym_xoroshiro128plusadvance(sym_s0, sym_s1)

		return sym_s0, sym_s1, condition

	def sym_xoroshiro128plusadvance(self, sym_s0, sym_s1):    
		sym_s1 ^= sym_s0
		sym_s0 = z3.RotateLeft(sym_s0, 24) ^ sym_s1 ^ ((sym_s1 << 16) & 0xFFFFFFFFFFFFFFFF)
		sym_s1 = z3.RotateLeft(sym_s1, 37)

		return sym_s0, sym_s1

	def get_models(self, s):
		result = []
		while s.check() == z3.sat:
			m = s.model()
			result.append(m)

			# Constraint that makes current answer invalid
			d = m[0]
			c = d()
			s.add(c != m[d])

		return result

	def find_seeds(self, ec, pid):
		solver = z3.Solver()
		start_s0 = z3.BitVecs('start_s0', 64)[0]

		sym_s0 = start_s0
		sym_s1 = 0x82A2B175229D6A5B

		# EC call
		sym_s0, sym_s1, condition = self.sym_xoroshiro128plus(sym_s0, sym_s1, ec)
		solver.add(condition)

		# TID/SID call
		sym_s0, sym_s1 = self.sym_xoroshiro128plusadvance(sym_s0, sym_s1)

		# PID call
		sym_s0, sym_s1, condition = self.sym_xoroshiro128plus(sym_s0, sym_s1, pid)
		solver.add(condition)

		models = self.get_models(solver)
		return [ model[start_s0].as_long() for model in models ]

	def find_seed(self, seeds, ivs):
		for seed in seeds:
			for iv_count in range(1, 6):
				rng = XoroShiro(seed)

				# ec, tid/sid, pid
				for i in range(3):
					rng.nextInt(0xffffffff, 0xffffffff)

				check_ivs = [None]*6
				count = 0
				while count < iv_count:
					stat = rng.nextInt(6, 7)
					if check_ivs[stat] is None:
						check_ivs[stat] = 31
						count += 1

				for i in range(6):
					if check_ivs[i] is None:
						check_ivs[i] = rng.nextInt(32, 31)

				if ivs == check_ivs:
					return seed

		return None

	def search(self, ec, pid, ivs):
		#print("")
		seeds = self.find_seeds(ec, pid)
		if len(seeds) > 0:
			seed, iv_count = self.find_seed(seeds, ivs)
			if seed != None:
				return hex(seed)
				#return "```Raid seed: " + str(hex(seed)) + " \nNumber of IVs: " + str(iv_count) + "```"

		seedsXor = self.find_seeds(ec, pid ^ 0x10000000) # Check for shiny lock
		if len(seedsXor) > 0:
			seed, iv_count = self.find_seed(seedsXor, ivs)
			if seed != None:
				return hex(seed)

		return -1, -1

def searchPKM():
	file_name = sys.argv[1]
	with open(file_name, "rb") as f:
		data = f.read()
	pkm = PK8(data)

	ec = pkm.getEC()
	pid = pkm.getPID()
	ivs = [ pkm.getHP(), pkm.getAtk(), pkm.getDef(), pkm.getSpA(), pkm.getSpD(), pkm.getSpe() ]

	return search(ec, pid, ivs)

