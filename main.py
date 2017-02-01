from sys import argv
#import multiprocessing (might be used later on)
import time
import os
import processor
import memory

#DOS == Default Output System

global mem, cpu, memsize, columns
mem = memory.mem()
cpu = processor.cpu()
rows, columns = os.popen('stty size', 'r').read().split()

debug = False
try:
    if argv[2] == '-d':
        debug = True
except:
    pass
memsize = 0xa00

mem.initMem(memsize, argv[1])

def Debugger():
    lines = []
    DOSval = mem.read(0x0)
    if type(DOSval) is int:
        DOSval = hex(DOSval)
    os.system('cls' if os.name == 'nt' else 'clear')

    #Default Debug
    start = 'Current: ' + hex(cpu.regdb[1][1]) + '\t' + str(mem.read(cpu.regdb[1][1])) + '\t'
    if type(mem.read(cpu.regdb[1][1])) is int:
        ins = mem.read(cpu.regdb[1][1])
    else:
        ins = mem.read(cpu.regdb[1][1])[:3]
    if ins == 'mrd' or ins == 'mwr' or ins == 'lco' or ins == 'jmp': #Tabbing is still broken
        start += '\t'
    lines.append(start + '|\t' + 'Memory info: ' + hex(memsize) + '(' + str(memsize) + ')Blocks\t' + 'DOS: ' + DOSval)
    lines.append('-' * int(columns))

    #CPU Debug
    for reg in cpu.DEBUG():
        if reg[0] == 'r':
            for i, alt in enumerate(reg[1]):
                lines.append('r' + str(i) + ':\t' + hex(alt) + '\t|')
        else:
            lines.append(reg[0] + ':\t' + hex(reg[1]) + '\t|')

    #Memory Debug
    lines[2] += mem.DEBUG(50)
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
prev = 0
mem_bus = None
while mem.read(0x0) != 0xff: #While the halt value is not in the DOS
    if debug: #Calls debugger if debugger is set
        Debugger()
    else: #Prints any changes to the DOS
        current = mem.read(0x0)
        if current != prev:
            print(current)
        prev = current
    cpu_io = cpu.Tick(mem.read(cpu.regdb[1][1]), mem_bus) #Tick the CPU
    if cpu_io != None: #Handle the response
        mem_bus = eval(cpu_io) #Takes python code and executes in main's scope
    else:
        mem_bus = None
    time.sleep(1) #Clock speed
