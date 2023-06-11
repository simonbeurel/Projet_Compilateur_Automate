"""
Affiche une chaine de caractère avec une certaine identation
"""
def afficher(s,indent=0):
    print(" "*indent+s)


class Programme:
    def __init__(self,ListeFonctions ,listeInstructions):
        self.listeFonctions = ListeFonctions
        self.listeInstructions = listeInstructions
    def afficher(self,indent=0):
        afficher("<programme>",indent)
        if self.listeFonctions != None:
            self.listeFonctions.afficher(indent+1)
        self.listeInstructions.afficher(indent+1)
        afficher("</programme>",indent)

class ListeInstructions:
    def __init__(self):
        self.instructions = []
    def afficher(self,indent=0):
        afficher("<listeInstructions>",indent)
        for instruction in self.instructions:
            instruction.afficher(indent+1)
        afficher("</listeInstructions>",indent)

class Ecrire:
    def __init__(self,exp):
        self.exp = exp
    def afficher(self,indent=0):
        afficher("<ecrire>",indent)
        self.exp.afficher(indent+1)
        afficher("</ecrire>",indent)

class Operation:
    def __init__(self,op,exp1,exp2):
        self.exp1 = exp1
        self.op = op
        self.exp2 = exp2
    def afficher(self,indent=0):
        afficher("<operation "+ "\"" + self.op + "\" >", indent)
        self.exp1.afficher(indent+1)
        if self.exp2 != None:
            self.exp2.afficher(indent+1)
        afficher("</operation>",indent)
class Entier:
    def __init__(self,valeur):
        self.valeur = valeur
    def afficher(self,indent=0):
        afficher("[Entier:"+str(self.valeur)+"]",indent)

class Variable:
    def __init__(self,nom):
        self.nom = nom
    def afficher(self,indent=0):
        afficher("[Variable:"+self.nom+"]",indent)

class Booleen:
    def __init__(self,valeur):
        self.valeur = valeur
    def afficher(self,indent=0):
        afficher("[Booleen:"+self.valeur+"]",indent)

class AppelFonction:
    def __init__(self,nom,listeExpressions):
        self.nom = nom
        self.listeExpressions = listeExpressions
    def afficher(self,indent=0):
        afficher("[AppelFonction:"+self.nom+"]",indent)
        if self.listeExpressions != None:
            self.listeExpressions.afficher(indent+1)



class Lire:
    def __init__(self):
        self.nom = "Lire"
    def afficher(self,indent=0):
        afficher("<Lire>",indent)
        afficher("</Lire>",indent)

class ListeExpressions:
    def __init__(self):
        self.expressions = []
    def afficher(self,indent=0):
        afficher("<listeExpressions>",indent)
        for expression in self.expressions:
            expression.afficher(indent+1)
        afficher("</listeExpressions>",indent)

class DeclarationVariable:
    def __init__(self,type,nom):
        self.type = type
        self.nom = nom
    def afficher(self,indent=0):
        afficher("<declarationVariable type=\""+self.type+"\" nom=\""+self.nom+"\"/>",indent)

class Affectation:
    def __init__(self,nom,expression):
        self.nom = nom
        self.expression = expression
    def afficher(self,indent=0):
        afficher("<affectation nom=\""+self.nom+"\""+ ">",indent)
        self.expression.afficher(indent+1)
        afficher("</affectation>",indent)

class DeclarationAffectation:
    def __init__(self,type,nom,expression):
        self.type = type
        self.nom = nom
        self.expression = expression
    def afficher(self,indent=0):
        afficher("<declarationAffectation type=\""+self.type+"\" nom=\""+self.nom+"\""+ ">",indent)
        self.expression.afficher(indent+1)
        afficher("</declarationAffectation>",indent)


class Conditionnelle:
    def __init__(self, condition, listeInstructionsSi, listeSinonSi, listeInstructionsSinon):
        self.condition = condition
        self.listeInstructionsSi = listeInstructionsSi
        self.listeSinonSi = listeSinonSi
        self.listeInstructionsSinon = listeInstructionsSinon

    def afficher(self, indent=0):
        afficher("<conditionnelle>", indent)
        afficher("<Si>", indent)
        self.condition.afficher(indent + 1)
        afficher("</Si>", indent)
        afficher("<Alors>", indent)
        self.listeInstructionsSi.afficher(indent + 1)
        afficher("</Alors>", indent)
        if self.listeSinonSi is not None:
            afficher("<SinonSi>", indent)
            self.listeSinonSi.afficher(indent + 1)
            afficher("</SinonSi>", indent)
        if self.listeInstructionsSinon is not None:
            afficher("<Sinon>", indent)
            self.listeInstructionsSinon.afficher(indent + 1)
            afficher("</Sinon>", indent)
        afficher("</conditionnelle>", indent)



class BoucleTantQue:
    def __init__(self,expr,listeInstructions):
        self.expr = expr
        self.listeInstructions = listeInstructions
    def afficher(self,indent=0):
        afficher("<boucleTantQue>",indent)
        afficher("<conditionTantQue>",indent)
        self.expr.afficher(indent+1)
        afficher("</conditionTantQue>",indent)
        afficher("<instructionsTantQue>",indent)
        self.listeInstructions.afficher(indent+1)
        afficher("</instructionsTantQue>",indent)
        afficher("</boucleTantQue>",indent)


class Retourner:
    def __init__(self,expression):
        self.expression = expression
    def afficher(self,indent=0):
        afficher("<retourner>",indent)
        self.expression.afficher(indent+1)
        afficher("</retourner>",indent)


class ListeFonctions:
    def __init__(self):
        self.fonctions = []
    def afficher(self,indent=0):
        afficher("<listeFonctions>",indent)
        for fonction in self.fonctions:
            fonction.afficher(indent+1)
        afficher("</listeFonctions>",indent)


class Fonction:
    def __init__(self,type,nom,listeParametres,listeInstructions):
        self.type = type
        self.nom = nom
        self.listeParametres = listeParametres
        self.listeInstructions = listeInstructions
    def afficher(self,indent=0):
        afficher("<fonction type=\""+self.type+"\" nom=\""+self.nom+"\""+ ">",indent)
        if self.listeParametres != None:
            self.listeParametres.afficher(indent+1)
        self.listeInstructions.afficher(indent+1)
        afficher("</fonction>",indent)


class ListeParametres:
    def __init__(self):
        self.parametres = []
    def afficher(self,indent=0):
        afficher("<listeParametres>",indent)
        for parametre in self.parametres:
            parametre.afficher(indent+1)
        afficher("</listeParametres>",indent)


class Parametre:
    def __init__(self,type,nom):
        self.type = type
        self.nom = nom
    def afficher(self,indent=0):
        afficher("<parametre type=\""+self.type+"\" nom=\""+self.nom+"\""+ "/>",indent)