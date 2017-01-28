from sys import argv
#import multiprocessing (might be used later on)
import time
import os
import processor
import memory

global mem, cpu, memsize
mem = memory.mem()
cpu = processor.cpu()

debug = True
memsize = 0x100

mem.initMem(memsize, argv[1])

def Debugger():
    lines = []
    DOSval = mem.read(0x0)
    if type(DOSval) is int:
        DOSval = hex(DOSval)
    os.system('cls' if os.name == 'nt' else 'clear')

    #Default Debug
    start = 'Current: ' + hex(cpu.regdb[1][1]) + '\t' + str(mem.read(cpu.regdb[1][1])) + '\t'
    ins = mem.read(cpu.regdb[1][1])[:3]
    if ins == 'mrd' or ins == 'mwr' or ins == 'lco' or ins == 'jmp':
        start += '\t'
    lines.append(start + '|\t' + 'Memory info: ' + hex(memsize) + '(' + str(memsize) + ')Blocks\t' + 'DOS: ' + DOSval)
    lines.append('-' * 119)

    #CPU Debug
    for reg in cpu.DEBUG():
        if reg[0] == 'r':
            for i, alt in enumerate(reg[1]):
                lines.append('r' + str(i) + ':\t' + hex(alt) + '\t|')
        else:
            lines.append(reg[0] + ':\t' + hex(reg[1]) + '\t|')

    #Memory Debug
    lines[2] += mem.DEBUG(86)
    while len(mem.stderr) > cpu.regcount:
        del mem.stderr[0]
    mem.stderr.reverse()
    lnptr = 3
    for x in range(0, cpu.regcount - 1):
        if len(mem.stderr) != 0 and x < len(mem.stderr):
            if x == 0:
                indent = '> '
            else:
                indent = ' '
            lines[lnptr] += indent + mem.stderr[x]
            lnptr += 1
        else:
            break
    mem.stderr.reverse()

    #Print all the debugging information
    for ln in lines:
        print(ln)

#MAIN LOOP
mem_bus = None
while mem.read(0x0) != 0xff: #While the halt value is not in the DOS
    if debug:
        Debugger()
    cpu_io = cpu.Tick(mem.read(cpu.regdb[1][1]), mem_bus) #Tick the CPU
    if cpu_io != None: #Handle the response
        mem_bus = eval(cpu_io) #Takes python code and executes in main's scope
    else:
        mem_bus = None
    time.sleep(1) #Clock speed
