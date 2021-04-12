	.file	"avr.cpp"
__SP_H__ = 0x3e
__SP_L__ = 0x3d
__SREG__ = 0x3f
__RAMPZ__ = 0x3b
__tmp_reg__ = 0
__zero_reg__ = 1
	.text
.global	_Z9cpu_delayx
	.type	_Z9cpu_delayx, @function
_Z9cpu_delayx:
	push r2
	push r3
	push r4
	push r5
	push r6
	push r7
	push r8
	push r9
	push r10
	push r11
	push r12
	push r13
	push r14
	push r15
	push r16
	push r17
	push r28
	push r29
	in r28,__SP_L__
	in r29,__SP_H__
	sbiw r28,16
	in __tmp_reg__,__SREG__
	cli
	out __SP_H__,r29
	out __SREG__,__tmp_reg__
	out __SP_L__,r28
/* prologue: function */
/* frame size = 16 */
/* stack size = 34 */
.L__stack_usage = 34
	std Y+9,r18
	std Y+10,r19
	std Y+11,r20
	std Y+12,r21
	std Y+13,r22
	std Y+14,r23
	std Y+15,r24
	std Y+16,r25
	ldd r24,Y+9
	std Y+1,r24
	ldd r24,Y+10
	std Y+2,r24
	ldd r24,Y+11
	std Y+3,r24
	ldd r24,Y+12
	std Y+4,r24
	ldd r24,Y+13
	std Y+5,r24
	ldd r24,Y+14
	std Y+6,r24
	ldd r24,Y+15
	std Y+7,r24
	ldd r24,Y+16
	std Y+8,r24
.L4:
	ldd r10,Y+1
	ldd r11,Y+2
	ldd r12,Y+3
	ldd r13,Y+4
	ldd r14,Y+5
	ldd r15,Y+6
	ldd r16,Y+7
	ldd r17,Y+8
	mov r18,r10
	mov r19,r11
	mov r20,r12
	mov r21,r13
	mov r22,r14
	mov r23,r15
	mov r24,r16
	mov r25,r17
	ldi r26,lo8(-1)
	call __adddi3_s8
	mov r2,r18
	mov r3,r19
	mov r4,r20
	mov r5,r21
	mov r6,r22
	mov r7,r23
	mov r8,r24
	mov r9,r25
	std Y+1,r2
	std Y+2,r3
	std Y+3,r4
	std Y+4,r5
	std Y+5,r6
	std Y+6,r7
	std Y+7,r8
	std Y+8,r9
	ldi r30,lo8(1)
	mov r18,r10
	mov r19,r11
	mov r20,r12
	mov r21,r13
	mov r22,r14
	mov r23,r15
	mov r24,r16
	mov r25,r17
	ldi r26,0
	call __cmpdi2_s8
	brne .L2
	ldi r30,0
.L2:
	tst r30
	breq .L5
	rjmp .L4
.L5:
	nop
/* epilogue start */
	adiw r28,16
	in __tmp_reg__,__SREG__
	cli
	out __SP_H__,r29
	out __SREG__,__tmp_reg__
	out __SP_L__,r28
	pop r29
	pop r28
	pop r17
	pop r16
	pop r15
	pop r14
	pop r13
	pop r12
	pop r11
	pop r10
	pop r9
	pop r8
	pop r7
	pop r6
	pop r5
	pop r4
	pop r3
	pop r2
	ret
	.size	_Z9cpu_delayx, .-_Z9cpu_delayx
.global	main
	.type	main, @function
main:
	push r28
	push r29
	in r28,__SP_L__
	in r29,__SP_H__
/* prologue: function */
/* frame size = 0 */
/* stack size = 2 */
.L__stack_usage = 2
	ldi r24,lo8(36)
	ldi r25,0
	ldi r18,lo8(-1)
	movw r30,r24
	st Z,r18
	ldi r24,lo8(37)
	ldi r25,0
	ldi r18,lo8(-1)
	movw r30,r24
	st Z,r18
.L7:
	ldi r18,lo8(-96)
	ldi r19,lo8(-122)
	ldi r20,lo8(1)
	ldi r21,0
	ldi r22,0
	ldi r23,0
	ldi r24,0
	ldi r25,0
	call _Z9cpu_delayx
	ldi r24,lo8(37)
	ldi r25,0
	movw r30,r24
	st Z,__zero_reg__
	ldi r18,lo8(-96)
	ldi r19,lo8(-122)
	ldi r20,lo8(1)
	ldi r21,0
	ldi r22,0
	ldi r23,0
	ldi r24,0
	ldi r25,0
	call _Z9cpu_delayx
	ldi r24,lo8(37)
	ldi r25,0
	ldi r18,lo8(-1)
	movw r30,r24
	st Z,r18
	rjmp .L7
	.size	main, .-main
	.ident	"GCC: (GNU) 5.4.0"
