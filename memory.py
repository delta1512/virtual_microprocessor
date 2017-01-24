import asmimage
class mem:
	def __init__(self):
		self.Memory = []

	def initMem(self, size):
		for x in range(0, size):
			self.Memory.append(0)
		if len(asmimage.image) >= size:
			print('ERROR: Image too big for memory. Asserting system halt...')
			self.Memory[0] = 0xff
		else:
			for i, x in enumerate(asmimage.image):
				self.Memory[i+1] = x

	def read(self, addr):
		try:
			return self.Memory[addr]
		except:
			print('ERROR: A nonexistant part of memory was read. Returning 0 to the caller...')
			return 0

	def write(self, addr, data):
		try:
			self.Memory[addr] = data
		except:
			print('ERROR: An invalid memory WRITE occurred. Doing nothing...')

	def DEBUG(self):
		print('DOS > ' + str(self.Memory[0x0]))
