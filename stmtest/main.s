	.cpu arm7tdmi
	.eabi_attribute 20, 1
	.eabi_attribute 21, 1
	.eabi_attribute 23, 3
	.eabi_attribute 24, 1
	.eabi_attribute 25, 1
	.eabi_attribute 26, 1
	.eabi_attribute 30, 4
	.eabi_attribute 34, 0
	.eabi_attribute 18, 4
	.file	"main.c"
	.text
	.section	.text.startup,"ax",%progbits
	.align	1
	.global	main
	.arch armv4t
	.syntax unified
	.code	16
	.thumb_func
	.fpu softvfp
	.type	main, %function
main:
	@ Function supports interworking.
	@ args = 0, pretend = 0, frame = 8
	@ frame_needed = 0, uses_anonymous_args = 0
	@ link register save eliminated.
	movs	r0, #0
	movs	r2, #42
	sub	sp, sp, #8
	str	r0, [sp, #4]
	ldr	r3, [sp, #4]
	ldr	r3, .L2
	str	r2, [r3]
	add	sp, sp, #8
	@ sp needed
	bx	lr
.L3:
	.align	2
.L2:
	.word	.LANCHOR0
	.size	main, .-main
	.text
	.align	1
	.global	malloc
	.syntax unified
	.code	16
	.thumb_func
	.fpu softvfp
	.type	malloc, %function
malloc:
	@ Function supports interworking.
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 0, uses_anonymous_args = 0
	@ link register save eliminated.
	movs	r0, #0
	@ sp needed
	bx	lr
	.size	malloc, .-malloc
	.align	1
	.global	_exit
	.syntax unified
	.code	16
	.thumb_func
	.fpu softvfp
	.type	_exit, %function
_exit:
	@ Function supports interworking.
	@ Volatile: function does not return.
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 0, uses_anonymous_args = 0
	@ link register save eliminated.
.L6:
	b	.L6
	.size	_exit, .-_exit
	.global	i
	.bss
	.align	2
	.set	.LANCHOR0,. + 0
	.type	i, %object
	.size	i, 4
i:
	.space	4
	.ident	"GCC: (GNU Arm Embedded Toolchain 9-2020-q2-update) 9.3.1 20200408 (release)"
