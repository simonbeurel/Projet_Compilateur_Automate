%include	"io.asm"
section	.bss
sinput:	resb	255	;reserve a 255 byte space in memory for the users input string
v$a:	resd	1
section	.text
global _start
_start:
	push	7				 ; push integer value
	push	4				 ; push integer value
	push	3				 ; push integer value
	pop	ebx				 ; pop the first operand into eax
	pop	eax				 ; pop the second operand into ebx
	add	eax,	ebx			 ; performing eax + ebx and putting the result in eax
	push	eax				 ; push the result
	pop	ebx				 ; pop the second operand into ebx
	pop	eax				 ; pop the first operand into eax
	cmp	eax,	ebx			 ; compare eax and ebx
	je	e0				 ; jump to etiquette_vrai if equal
	push	0				 ; push 0 as false
	jmp	e1				 ; jump to etiquette_fin
	e0:					 ; label for true condition
	push	1				 ; push 1 as true
	e1:					 ; label for end of comparison
	pop	eax		
	call	iprintLF		
	push	3				 ; push integer value
	push	2				 ; push integer value
	pop	ebx				 ; pop the first operand into eax
	pop	eax				 ; pop the second operand into ebx
	imul	ebx				 ; performing eax * ebx and putting the result in eax
	push	eax				 ; push the result
	push	6				 ; push integer value
	push	1				 ; push integer value
	pop	ebx				 ; pop the first operand into eax
	pop	eax				 ; pop the second operand into ebx
	imul	ebx				 ; performing eax * ebx and putting the result in eax
	push	eax				 ; push the result
	pop	ebx				 ; pop the second operand into ebx
	pop	eax				 ; pop the first operand into eax
	cmp	eax,	ebx			 ; compare eax and ebx
	jne	e2				 ; jump to etiquette_vrai if not equal
	push	0				 ; push 0 as false
	jmp	e3				 ; jump to etiquette_fin
	e2:					 ; label for true condition
	push	1				 ; push 1 as true
	e3:					 ; label for end of comparison
	pop	eax		
	call	iprintLF		
	mov	eax,	1			 ; 1 est le code de SYS_EXIT
	int	0x80				 ; exit
