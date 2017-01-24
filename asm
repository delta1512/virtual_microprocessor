jmp	0x023
mov	SP, MBR		#function start
mwr	0x9f6
mrd	0x9fb
mov	MBR, SP
lco	1
mrd	SP
mov	MBR, r2
sub	SP, SP
mrd	SP
mov	MBR, r1
sub	SP, SP
mrd	SP
mov	MBR, r0
lco	2
add	r0, r0
sub	r1, r1
mul	r2, r2
lco	1
mov	r0, MBR
mwr	SP
mwr	0x0
add	SP, SP
mov	r1, MBR
mwr	SP
mwr	0x0
add	SP, SP
mov	r2, MBR
mwr	SP
mwr	0x0
mrd	0x9f6
mov	MBR, SP
mrd	SP
jmp	MBR		#function end
lco 	0x9fc		#load stacks
mov 	ACC, MBR
mwr 	0x9fb
lco 	0x9f7
mov 	ACC, MBR
mwr 	0x9f6
lco	3
mrd	0x9fb		#prepare vstack access by getting pointer
mov	MBR, SP		
mov	ACC, MBR	#prepare a constant
lco	1		#prepare SP increment
mwr	SP		#write 3 to the stack 3 times
add	SP, SP
mwr	SP
add	SP, SP
mwr	SP
mov	SP, MBR		#place pointer at header
mwr	0x9fb
mrd 	0x9f6		#prepare fstack access by getting pointer
mov	MBR, SP
lco	3
add	PC, MBR		#prepare return address on the fstack
mwr	SP
jmp	0x002		#jump to function
mrd	0x9f6
mov	MBR, SP
lco	3
add	PC, MBR
mwr	SP
jmp	0x002
mrd     0x9f6
mov     MBR, SP
lco     3
add     PC, MBR
mwr     SP
jmp	0x002
lco	0xff
mov	ACC, MBR
mwr	0x0

#fstack @ 0x9f6
#vstack @ 0x9fb
