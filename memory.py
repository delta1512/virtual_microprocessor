from __future__ import division
from math import floor

class mem:
	def __init__(self):
		self.Memory = []
		self.MemSize = 0
		self.stderr = ['Memory error log']

	def initMem(self, size, imgname):
		for i, x in enumerate(imgname):
			if x == '.':
				imgname = imgname[:i]
				break
		self.MemSize = size
		imp = 'import ' + imgname
		exec(imp)
		for x in range(0, size):
			self.Memory.append(0)
		if len(eval(imgname + '.image')) >= size:
			print('ERROR: Image too big for memory. Asserting system halt...')
			self.Memory[0] = 0xff
		else:
			for i, x in enumerate(eval(imgname + '.image')):
				self.Memory[i+1] = x

	def read(self, addr):
		try:
			return self.Memory[addr]
		except:
			self.stderr.append('ERROR: A nonexistant part of memory was read at: ' + str(hex(addr)))
			return 0

	def write(self, addr, data):
		try:
			self.Memory[addr] = data
		except:
			self.stderr.append('ERROR: An invalid memory WRITE occurred at: ' + str(hex(addr)))

	def DEBUG(self, size):
		used_blocks = 0
		for x in self.Memory:
			if x != 0:
				used_blocks += 1
		usage = round(used_blocks / self.MemSize, 2)
		graphic = 'Memory usage: ['
		for j in range(0, floor(size * usage)):
			graphic += '|'
			size -= 1
		for i in range(0, size):
			graphic += ' '
		graphic += ']'
		return graphic
