dseg
        org     030h            ; Start filling the data segment from here

cseg
        org     0               ; Reset
        jmp     startup

        org     030h            ; Start filling the code segment from here

get_inverse:
	;R5-R7 as params. R2-R4 as result
	mov A, R5
	cpl A
	mov R2, A

	mov A, R6
	cpl A
	mov R3, A

	mov A, R7
	cpl A
	mov R4, A

	ret

func1:
	;f(x,y,z) = ((x & y) | (x* & y* & z*)) & ((x & y) | (y & z*))
	call get_inverse

	;(x & y) -> R0
	mov A, R5
	anl A, R6
	mov R0, A

	;(x* & y* & z*) -> R1
	mov A, R2
	anl A, R3
	anl A, R4
	mov R1, A

	;(x & y) | (x* & y* & z*) -> R1
	mov A, R0
	orl A, R1
	mov R1, A

	;store (x & y) | (x* & y* & z*)
	push 01H

	;(y & z*) -> R1
	mov A, R6
	anl A, R2
	mov R1, A

	;(x & y) | (y & z*) -> R1
	mov A, R0
	orl A, R1
	mov R1, A

	;((x & y) | (x* & y* & z*)) & ((x & y) | (y & z*)) -> R0
	mov A, R1
	pop 00H
	anl A, R0
	mov R0, A

	;return R0 as result
	ret

func2:
	;func2(x,y,z) = ((x&y) | (x&z) | (*y&z)) & ((y&z)|(*x&*y&z))
	call get_inverse

	;(x&y) | (x&z) | (*y&z) -> R1
	mov A, R5
	anl A, R6
	mov R0, A
	mov A, R5
	anl A, R7
	mov R1, A
	mov A, R3
	anl A, R7
	orl A, R0
	orl A, R1
	mov R1, A

	;store (x&y) | (x&z) | (*y&z)
	push 01H

	;(y&z)|(*x&*y&z) -> R1
	mov A, R6
	anl A, R7
	mov R0, A
	mov A, R2
	anl A, R3
	anl A, R7
	orl A, R0
	mov R1, A

	;((x&y) | (x&z) | (*y&z)) & ((y&z)|(*x&*y&z)) -> R0
	pop 00H
	mov A, R0
	anl A, R1
	mov R0, A

	ret

startup:
	;Set R5-R7 as params
	mov R5, #11110000B
	mov R6, #11001100B
	mov R7, #10101010B

	call func2
	push 00H

	call func1
	pop 01H

	; func1 -> R0, func2 -> R1

	mov A, R0
	mov B, R1
	cjne A, B, noequal

equal:
	mov R0, 00H
	jmp finish

noequal:
	jc less
more:
	mov A, R0
	subb A, R1
	mov R0, A
	jmp finish

less:
	mov A, R1
	subb A, R0
	mov R0, A
	jmp finish

finish: 
	;RESULT -> R0
	jmp finish

traploop:
       	jmp traploop

END