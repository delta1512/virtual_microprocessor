import multiprocessing
import time
import processor
import memory

global mem, cpu
mem = memory.mem()
cpu = processor.cpu()

terminal_debug = True

mem.initMem(0xa00)

#def DOS(): #Default Output System

mem_bus = None
while mem.read(0x0) != 0xff:
    if terminal_debug:
        print('DEBUG: Current INS: ' + '\t' + hex(cpu.db[1][1]) + '\t' + str(mem.read(cpu.db[1][1])))
        #print('DEBUG: CPU registers: ', cpu.DEBUG())
    cpu_io = cpu.Tick(mem.read(cpu.db[1][1]), mem_bus)
    if cpu_io != None:
        mem_bus = eval(cpu_io)
    else:
        mem_bus = None
    time.sleep(0.1)

'''
response = cpu.Tick(mem.read(cpu.PC), None)
if response != None:
    cpu.Tick('lco 1', eval(response))
'''
#print(cpu.Tick(mem.read(cpu.PC), None))
#print(cpu.Reg_Access('MBR', None))
