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
	;f(x,y,z) = *(y&z) | (y&*z) | (x&*y) | (x&z) | (*x&y)
	call get_inverse

	;*(y&z) -> stack
	mov A, R6
	anl A, R7
	cpl A
	mov R0, A
	push 00H

	;(y&*z) -> stack
	mov A, R6
	anl A, R4
	mov R0, A
	push 00H

	;(x&*y) -> stack
	mov A, R5
	anl A, R3
	mov R0, A
	push 00H

	;(x&z) -> stack
	mov A, R5
	anl A, R7
	mov R0, A
	push 00H

	;(*x&y) -> stack
	mov A, R2
	anl A, R6
	mov R0, A
	push 00H

	pop 04H
	pop 03H
	pop 02H
	pop 01H
	pop 00H

	mov A, R0
	orl A, R1
	orl A, R2
	orl A, R3
	orl A, R4

	;return R0 as result
	mov R0, A
	ret

func2:
	;func2(x,y,z) = (*x&y&z) | (x&*y&*z) | (x&*y&z) | (x&y&z)
	call get_inverse

	;(*x&y&z) -> stack
	mov A, R2
	anl A, R6
	anl A, R7
	mov R0, A
	push 00H

	;(x&*y&*z) -> stack
	mov A, R5
	anl A, R3
	anl A, R4
	mov R0, A
	push 00H

	;(x&*y&z) -> stack
	mov A, R5
	anl A, R3
	anl A, R7
	mov R0, A
	push 00H

	;(x&y&z) -> stack
	mov A, R5
	anl A, R6
	anl A, R7
	mov R0, A
	push 00H

	pop 03H
	pop 02H
	pop 01H
	pop 00H

	mov A, R0
	orl A, R1
	orl A, R2
	orl A, R3

	;return R0 as result
	mov R0, A
	ret

startup:
	;Set R5-R7 as params
	mov R5, #11110000B
	mov R6, #11001100B
	mov R7, #10101010B

	; func1 -> R0, func2 -> R1
	call func2
	push 00H
	call func1
	pop 01H


	mov A, R0
	mov B, R1

third_stage:
	cjne A, B, noequal

equal:
	mov R0, 00H
	jmp finish

noequal:
	jc A_less_then_B
	
A_more_then_B:
	jmp finish

A_less_then_B:
	mov R0, B
	mov R1, #2
	mov B, R1
	mul AB
	mov B, R0
	jmp third_stage

finish: 
	;RESULT -> R0
	jmp finish

traploop:
       	jmp traploop

END