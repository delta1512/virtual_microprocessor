asmcode = open('asm', 'r')
length = len(asmcode.readlines())
asmcode.close()
asmcode = open('asm', 'r')

imgout = open('asmimage.py', 'w')
imgout.write('image = [')

aftercomma = False
newline = "," + '\n'
for lnnum in range(0, length):
	line = asmcode.readline()
	out = ''
	for x in line:
		if x == '\t':
			out += ' '
		elif x == '\n':
			pass
		elif x == ',':
			after_comma = True
			out += x
		elif x == ' ' and after_comma:
			out += x
			after_comma = False
		elif x == ' ':
			pass
		elif x == '#':
			break
		else:
			out += x
	if lnnum == length-1:
		newline = ''
	if out != '':
		imgout.write("'" + out + "'" + newline)
	else:
		imgout.write('0' + newline)

imgout.write(']' + '\n')
asmcode.close()
imgout.close()
