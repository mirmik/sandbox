	.file	"avr.cpp"
__SP_H__ = 0x3e
__SP_L__ = 0x3d
__SREG__ = 0x3f
__RAMPZ__ = 0x3b
__tmp_reg__ = 0
__zero_reg__ = 1
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"hello"
	.section	.text.startup,"ax",@progbits
.global	main
	.type	main, @function
main:
	push r28
	push r29
	rcall .
	push __zero_reg__
	in r28,__SP_L__
	in r29,__SP_H__
/* prologue: function */
/* frame size = 4 */
/* stack size = 6 */
.L__stack_usage = 6
	ldi r24,lo8(-1)
	out 0x4,r24
	ldi r24,lo8(18)
	ldi r25,0
	call malloc
	std Y+2,r25
	std Y+1,r24
	ldi r24,lo8(.LC0)
	ldi r25,hi8(.LC0)
	push r25
	push r24
	call printf
	pop __tmp_reg__
	pop __tmp_reg__
.L2:
	in r24,0x5
	com r24
	out 0x5,r24
	std Y+4,__zero_reg__
	std Y+3,__zero_reg__
.L3:
	ldd r24,Y+3
	ldd r25,Y+4
	cpi r24,-24
	sbci r25,3
	brge .L2
	ldd r24,Y+3
	ldd r25,Y+4
	adiw r24,1
	std Y+4,r25
	std Y+3,r24
	rjmp .L3
	.size	main, .-main
	.type	_GLOBAL__sub_I_k, @function
_GLOBAL__sub_I_k:
/* prologue: function */
/* frame size = 0 */
/* stack size = 0 */
.L__stack_usage = 0
	ldi r24,lo8(22)
	ldi r25,0
	sts k+1,r25
	sts k,r24
	ret
	.size	_GLOBAL__sub_I_k, .-_GLOBAL__sub_I_k
	.global __do_global_ctors
	.section .ctors,"a",@progbits
	.p2align	1
	.word	gs(_GLOBAL__sub_I_k)
.global	b
	.section .bss
	.type	b, @object
	.size	b, 1
b:
	.zero	1
.global	k
	.type	k, @object
	.size	k, 2
k:
	.zero	2
	.ident	"GCC: (GNU) 5.4.0"
.global __do_copy_data
.global __do_clear_bss
