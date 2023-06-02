import sys
from analyse_lexicale import FloLexer
from analyse_syntaxique import FloParser
import arbre_abstrait

num_etiquette_courante = -1 #Permet de donner des noms différents à toutes les étiquettes (en les appelant e0, e1,e2,...)

afficher_table = False
afficher_nasm = False
"""
Un print qui ne fonctionne que si la variable afficher_table vaut Vrai.
(permet de choisir si on affiche le code assembleur ou la table des symboles)
"""
def printifm(*args,**kwargs):
    if afficher_nasm:
        print(*args,**kwargs)

"""
Un print qui ne fonctionne que si la variable afficher_table vaut Vrai.
(permet de choisir si on affiche le code assembleur ou la table des symboles)
"""
def printift(*args,**kwargs):
    if afficher_table:
        print(*args,**kwargs)

"""
Fonction locale, permet d'afficher un commentaire dans le code nasm.
"""
def nasm_comment(comment):
    if comment != "":
        printifm("\t\t ; "+comment)#le point virgule indique le début d'un commentaire en nasm. Les tabulations sont là pour faire jolie.
    else:
        printifm("")
"""
Affiche une instruction nasm sur une ligne
Par convention, les derniers opérandes sont nuls si l'opération a moins de 3 arguments.
"""
def nasm_instruction(opcode, op1="", op2="", op3="", comment=""):
    if op2 == "":
        printifm("\t"+opcode+"\t"+op1+"\t\t",end="")
    elif op3 =="":
        printifm("\t"+opcode+"\t"+op1+",\t"+op2+"\t",end="")
    else:
        printifm("\t"+opcode+"\t"+op1+",\t"+op2+",\t"+op3,end="")
    nasm_comment(comment)


"""
Retourne le nom d'une nouvelle étiquette
"""
def nasm_nouvelle_etiquette():
    global num_etiquette_courante
    num_etiquette_courante+=1
    return "e"+str(num_etiquette_courante)

"""
Affiche le code nasm correspondant à tout un programme
"""
def gen_programme(programme):
    printifm('%include\t"io.asm"')
    printifm('section\t.bss')
    printifm('sinput:	resb	255	;reserve a 255 byte space in memory for the users input string')
    printifm('v$a:	resd	1')
    printifm('section\t.text')
    printifm('global _start')
    printifm('_start:')
    gen_listeInstructions(programme.listeInstructions)
    nasm_instruction("mov", "eax", "1", "", "1 est le code de SYS_EXIT")
    nasm_instruction("int", "0x80", "", "", "exit")

"""
Affiche le code nasm correspondant à une suite d'instructions
"""
def gen_listeInstructions(listeInstructions):
    for instruction in listeInstructions.instructions:
        gen_instruction(instruction)

"""
Affiche le code nasm correspondant à une instruction
"""
def gen_instruction(instruction):
    if type(instruction) == arbre_abstrait.Ecrire:
        gen_ecrire(instruction)
    elif type(instruction) == arbre_abstrait.Lire:
        gen_lire(instruction)
    else:
        print("type instruction inconnu",type(instruction))
        exit(0)

"""
Affiche le code nasm correspondant au fait d'envoyer la valeur entière d'une expression sur la sortie standard
"""	
def gen_ecrire(ecrire):
    gen_expression(ecrire.exp) #on calcule et empile la valeur d'expression
    nasm_instruction("pop", "eax", "", "", "") #on dépile la valeur d'expression sur eax
    nasm_instruction("call", "iprintLF", "", "", "") #on envoie la valeur d'eax sur la sortie standard

"""
Affiche le code nasm correspondant au fait de lire une entrée utilisateur grâce à la fonction lire 
"""
def gen_lire(lire):
    #gen_expression(lire.exp)
    nasm_instruction("mov", "eax", "sinput", "", "")
    nasm_instruction("call", "readline", "", "", "On va lire l'entree de l'utilisateur")
    nasm_instruction("call", "atoi", "", "", "Transformer la chaine de caractère lue")
    nasm_instruction("push", "eax", "", "", "")

"""
Affiche le code nasm pour calculer et empiler la valeur d'une expression
"""
def gen_expression(expression):
    if isinstance(expression, arbre_abstrait.Operation):
        if expression.op in ["==", "!=", "<", ">", "<=", ">="]:
            gen_comparaison(expression)  # Appel à la fonction de génération de code pour les comparaisons
        else:
            gen_operation(expression)  # Génération de code pour les autres opérations
    elif isinstance(expression, arbre_abstrait.Entier):
        nasm_instruction("push", str(expression.valeur), "", "", "push integer value")
    elif isinstance(expression, arbre_abstrait.Lire):
        gen_lire(expression)  # Génération de code pour la lecture d'une entrée utilisateur
    elif isinstance(expression, arbre_abstrait.Booleen):
        gen_booleen(expression)  # Génération de code pour les valeurs booléennes
    else:
        print("type d'expression inconnu", type(expression))
        exit(0)


"""
Affiche le code nasm pour calculer l'opération et la mettre en haut de la pile
"""
def gen_operation(operation):
    # lookup for nasm instruction names
    code = {"+": "add", "*": "imul", "-": "sub", "/": "idiv", "%": "idiv", "et": "and", "ou": "or", "non": "xor"}

    gen_expression(operation.exp1)  # calculate and push the value of exp1
    if operation.op != "non":  # the "non" operation is unary
        nasm_instruction("pop", "eax", "", "", "pop the first operand into eax")
        gen_expression(operation.exp2)  # calculate and push the value of exp2

    nasm_instruction("pop", "eax", "", "", "pop the first operand into eax")
    nasm_instruction("pop", "ebx", "", "", "pop the second operand into ebx")

    if operation.op in ["et", "ou"]:
        # make sure both operands are booleans
        if not isinstance(operation.exp1, arbre_abstrait.Booleen) or not isinstance(operation.exp2, arbre_abstrait.Booleen):
            raise TypeError(f"Invalid operation: {operation.op} with non-boolean type")
        nasm_instruction(code[operation.op], "eax", "ebx", "", f"performing eax {operation.op} ebx and putting the result in eax")
    elif operation.op == "non":
        # make sure the operand is a boolean
        if not isinstance(operation.exp1, arbre_abstrait.Booleen):
            raise TypeError(f"Invalid operation: {operation.op} with non-boolean type")
        nasm_instruction(code[operation.op], "eax", "1", "", f"performing {operation.op} on eax and putting the result in eax")
    else:
        # arithmetic operations
        if isinstance(operation.exp1, arbre_abstrait.Booleen) or isinstance(operation.exp2, arbre_abstrait.Booleen):
            raise TypeError(f"Invalid operation: {operation.op} with boolean type")
        if operation.op in ['+', '-']:
            nasm_instruction(code[operation.op], "eax", "ebx", "", f"performing eax {operation.op} ebx and putting the result in eax")
        elif operation.op == '*':
            nasm_instruction(code[operation.op], "ebx", "", "", f"performing eax {operation.op} ebx and putting the result in eax")
        elif operation.op == '/':
            nasm_instruction("mov", "edx", "0", "", "set edx to 0 for division")
            nasm_instruction(code[operation.op], "ebx", "", "", f"performing eax {operation.op} ebx and putting the result in eax")
        elif operation.op == '%':
            nasm_instruction("mov", "edx", "0", "", "set edx to 0 for division")
            nasm_instruction(code[operation.op], "ebx", "", "", f"performing eax {operation.op} ebx and putting the result in eax")
            nasm_instruction("mov", "eax", "edx", "", "move the remainder of the division into eax")
    nasm_instruction("push", "eax", "", "", "push the result")

def gen_comparaison(comparaison):
    gen_expression(comparaison.exp1)  # Générer le code pour l'expression 1
    gen_expression(comparaison.exp2)  # Générer le code pour l'expression 2

    # Générer une nouvelle étiquette pour le saut
    etiquette_vrai = nasm_nouvelle_etiquette()
    etiquette_fin = nasm_nouvelle_etiquette()

    # Comparaison des valeurs
    nasm_instruction("pop", "ebx", "", "", "Dépiler la deuxième expression dans ebx")
    nasm_instruction("pop", "eax", "", "", "Dépiler la première expression dans eax")
    nasm_instruction("cmp", "eax", "ebx", "", "Comparer eax et ebx")

    # Saut conditionnel en fonction du résultat de la comparaison
    if comparaison.op == "==":
        nasm_instruction("je", etiquette_vrai, "", "", "Sauter à l'étiquette_vrai si égal")
    elif comparaison.op == "!=":
        nasm_instruction("jne", etiquette_vrai, "", "", "Sauter à l'étiquette_vrai si non égal")
    elif comparaison.op == "<":
        nasm_instruction("jl", etiquette_vrai, "", "", "Sauter à l'étiquette_vrai si inférieur")
    elif comparaison.op == ">":
        nasm_instruction("jg", etiquette_vrai, "", "", "Sauter à l'étiquette_vrai si supérieur")
    elif comparaison.op == "<=":
        nasm_instruction("jle", etiquette_vrai, "", "", "Sauter à l'étiquette_vrai si inférieur ou égal")
    elif comparaison.op == ">=":
        nasm_instruction("jge", etiquette_vrai, "", "", "Sauter à l'étiquette_vrai si supérieur ou égal")

    # Si la comparaison est fausse, mettre 0 sur la pile
    nasm_instruction("push", "0", "", "", "Mettre 0 sur la pile pour la condition fausse")

    # Saut inconditionnel à l'étiquette_fin
    nasm_instruction("jmp", etiquette_fin, "", "", "Sauter à l'étiquette_fin")

    # Étiquette pour le cas où la comparaison est vraie
    nasm_instruction(etiquette_vrai + ":", "", "", "", "Étiquette pour la condition vraie")

    # Mettre 1 sur la pile pour représenter le résultat vrai de la comparaison
    nasm_instruction("push", "1", "", "", "Mettre 1 sur la pile pour la condition vraie")

    # Étiquette pour la fin de la comparaison
    nasm_instruction(etiquette_fin + ":", "", "", "", "Étiquette pour la fin de la comparaison")



"""
Generation de code quand on rencontre un booleen dans notre programme
"""
def gen_booleen(booleen):
    if booleen.valeur == "Vrai":
        nasm_instruction("push", "1", "", "", "On détecte le booleen Vrai");  # on met sur la pile la valeur entière
    else:
        nasm_instruction("push", "0", "", "", "On détecte le booleen Faux")


if __name__ == "__main__":
    afficher_nasm = True
    lexer = FloLexer()
    parser = FloParser()
    if len(sys.argv) < 3 or sys.argv[1] not in ["-nasm","-table"]:
        print("usage: python3 generation_code.py -nasm|-table NOM_FICHIER_SOURCE.flo")
        exit(0)
    if sys.argv[1]  == "-nasm":
        afficher_nasm = True
    else:
        afficher_tableSymboles = True
    with open(sys.argv[2],"r") as f:
        data = f.read()
        try:
            arbre = parser.parse(lexer.tokenize(data))
            gen_programme(arbre)
        except EOFError:
            exit()
