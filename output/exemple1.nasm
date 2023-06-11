%include	"io.asm"
section	.bss
sinput:	resb	255	;reserve a 255 byte space in memory for the users input string
v$a:	resd	1
section	.text
global _start
_start:
	push	1				 ; On détecte le booleen Vrai
	pop	eax				 ; Dépiler la valeur de la condition dans eax
	cmp	eax,	0			 ; Comparer la valeur de la condition avec 0
	je	e0				 ; Sauter à l'étiquette_fin si la condition est fausse
	push	1				 ; push integer value
	pop	eax		
	call	iprintLF		
	jmp	e0				 ; Sauter à l'étiquette_fin après l'exécution de la liste d'instructions
	e0:					 ; Étiquette pour la fin de l'instruction Conditionnelle
	push	0				 ; push integer value
	pop	eax		
	call	iprintLF		
	mov	eax,	1			 ; 1 est le code de SYS_EXIT
	int	0x80				 ; exit
