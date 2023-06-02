%include	"io.asm"
section	.bss
sinput:	resb	255	;reserve a 255 byte space in memory for the users input string
v$a:	resd	1
section	.text
global _start
_start:
	push	6				 ; push integer value
	push	8				 ; push integer value
	pop	ebx				 ; pop the second operand into ebx
	pop	eax				 ; pop the first operand into eax
	cmp	eax,	ebx			 ; compare eax and ebx
	jg	e0				 ; jump to etiquette_vrai if greater than
	push	0				 ; push 0 as false
	jmp	e1				 ; jump to etiquette_fin
	e0:					 ; label for true condition
	push	1				 ; push 1 as true
	e1:					 ; label for end of comparison
	pop	eax		
	call	iprintLF		
	mov	eax,	1			 ; 1 est le code de SYS_EXIT
	int	0x80				 ; exit
