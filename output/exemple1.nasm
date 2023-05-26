%include	"io.asm"
section	.bss
sinput:	resb	255	;reserve a 255 byte space in memory for the users input string
v$a:	resd	1
section	.text
global _start
_start:
	push	1				 ; On détecte le booleen Vrai
	pop	ebx				 ; pop the second operand into ebx
	pop	eax				 ; pop the first operand into eax
	xor	eax,	1			 ; performing non on eax and putting the result in eax
	push	eax				 ; push the result
	pop	eax		
	call	iprintLF		
	mov	eax,	1			 ; 1 est le code de SYS_EXIT
	int	0x80				 ; exit
