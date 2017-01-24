class cpu:
    def __init__(self):
        self.ACC = 0
        self.PC = 1
        self.MBR = 0
        self.SP = 0

        self.registers = [0, 0, 0]

        self.db = [['ACC', self.ACC], ['PC', self.PC],
                   ['MBR', self.MBR], ['SP', self.SP],
                   ['r', self.registers]]

    def Reg_Access(self, name, data):
        if name[:1] == 'r':
            if data == None:
                return self.db[4][1][int(name[1])]
            else:
                self.db[4][1][int(name[1])] = data
                return
        for i, x in enumerate(self.db):
            if name == x[0]:
                if data == None:
                    return x[1]
                else:
                    self.db[i][1] = data
                    return

    def ALU(self, ins, src, dst):
        if ins == 'add' or ins == 'sub' or ins == 'mul':
            a = self.Reg_Access('ACC', None)
            b = self.Reg_Access(src, None)
        if ins == 'add':
            c = b + a
        elif ins == 'sub':
            c = b - a
        elif ins == 'mul':
            c = b * a
        else:
            c = self.Reg_Access(src, None)
        self.Reg_Access(dst, c)

    def INS_Decoder(self, ins):
        op = ins[:3]
        ins = ins[4:]
        interp = ''
        arg = None
        multi_arg = False
        for i, x in enumerate(ins):
            if x == ',':
                multi_arg = True
                arga = interp
                interp = ''
            elif x == ' ':
                pass
            else:
                interp += x
        if multi_arg:
            argb = interp
        else:
            arg = interp
        if type(arg) is str:
            for x in self.db:
                if arg == x[0]:
                    arg = hex(self.Reg_Access(arg, None))

        if op == 'mov':
            self.ALU('pass', arga, argb)
        if op == 'mrd':
            return 'mem.read(' + str(arg) + ')'
        if op == 'mwr':
            return 'mem.write(' + str(arg) + ', ' + str(self.MBR) + ')'
        if op == 'add':
            self.ALU('add', arga, argb)
        if op == 'sub':
            self.ALU('sub', arga, argb)
        if op == 'mul':
            self.ALU('mul', arga, argb)
        if op == 'lco':
            self.Reg_Access('ACC', int(arg, 16))
        if op == 'jmp':
            self.Reg_Access('PC', int(arg, 16))

    def Tick(self, mem_at_PC, mem_requ):
        if mem_requ != None:
            self.db[2][1] = mem_requ
        request = self.INS_Decoder(mem_at_PC)
        self.db[1][1] += 1
        return request

    def DEBUG(self):
        return self.db
'''
instruction set:

mov     src, dst - Copies the value from one register to another
mrd     addr     - Reads the memory at the value/register value of 'addr' and writes to the MBR
mwr     addr     - Writes the memory at the value/register value of 'addr' and puts result in the MBR
add     src, dst - Register at 'src' + ACC and result is stored in register 'dst'
sub     src, dst - Register at 'src' - ACC and result is stored in register 'dst'
mul     src, dst - Register at 'src' * ACC and result is stored in register 'dst'
lco     val      - Loads the constant 'val' into the ACC
jmp     addr     - Jumps to the instruction at the value/register value of 'addr'
'''
