	.cpu cortex-m4
	.eabi_attribute 20, 1
	.eabi_attribute 21, 1
	.eabi_attribute 23, 3
	.eabi_attribute 24, 1
	.eabi_attribute 25, 1
	.eabi_attribute 26, 1
	.eabi_attribute 30, 4
	.eabi_attribute 34, 1
	.eabi_attribute 18, 4
	.file	"main.c"
	.text
	.section	.text.startup,"ax",%progbits
	.align	1
	.global	main
	.arch armv7e-m
	.syntax unified
	.thumb
	.thumb_func
	.fpu softvfp
	.type	main, %function
main:
	@ Volatile: function does not return.
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 0, uses_anonymous_args = 0
	@ link register save eliminated.
	ldr	r3, .L3
	movs	r2, #42
	str	r2, [r3]
.L2:
	b	.L2
.L4:
	.align	2
.L3:
	.word	.LANCHOR0
	.size	main, .-main
	.text
	.align	1
	.global	malloc
	.syntax unified
	.thumb
	.thumb_func
	.fpu softvfp
	.type	malloc, %function
malloc:
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 0, uses_anonymous_args = 0
	@ link register save eliminated.
	movs	r0, #0
	bx	lr
	.size	malloc, .-malloc
	.align	1
	.global	_exit
	.syntax unified
	.thumb
	.thumb_func
	.fpu softvfp
	.type	_exit, %function
_exit:
	@ Volatile: function does not return.
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 0, uses_anonymous_args = 0
	@ link register save eliminated.
.L7:
	b	.L7
	.size	_exit, .-_exit
	.global	i
	.bss
	.align	2
	.set	.LANCHOR0,. + 0
	.type	i, %object
	.size	i, 4
i:
	.space	4
	.ident	"GCC: (15:9-2019-q4-0ubuntu1) 9.2.1 20191025 (release) [ARM/arm-9-branch revision 277599]"
