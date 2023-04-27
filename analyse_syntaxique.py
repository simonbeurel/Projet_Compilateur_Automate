import sys
from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait

class FloParser(Parser):
    # On récupère la liste des lexèmes de l'analyse lexicale
    tokens = FloLexer.tokens
    debugfile = 'parser.out'

    # Règles gramaticales et actions associées

    @_('listeInstructions')
    def prog(self, p):
        return arbre_abstrait.Programme(p[0])

    @_('instruction')
    def listeInstructions(self, p):
        l = arbre_abstrait.ListeInstructions()
        l.instructions.append(p[0])
        return l

    @_('instruction listeInstructions')
    def listeInstructions(self, p):
        p[1].instructions.append(p[0])
        return p[1]

    @_('ecrire')
    def instruction(self, p):
        return p[0]

    @_('ECRIRE "(" expr ")" ";"')
    def ecrire(self, p):
        return arbre_abstrait.Ecrire(p.expr)  # p.expr = p[2]

    @_('booleen')
    def expr(self, p):
        return p[0]

    @_('BOOLEEN')
    def booleen(self, p):
        return arbre_abstrait.Booleen(p[0])
    @_('somme')
    def booleen(self,p):
        return p[0]
    @_('somme EGAL_EGAL somme')
    def booleen(self, p):
        return arbre_abstrait.Operation('==', p[0], p[2])
    @_('somme DIFFERENT somme')
    def booleen(self, p):
        return arbre_abstrait.Operation('!=', p[0], p[2])
    @_('somme INFERIEUR somme')
    def booleen(self, p):
        return arbre_abstrait.Operation('<', p[0], p[2])
    @_('somme INFERIEUR_OU_EGAL somme')
    def booleen(self, p):
        return arbre_abstrait.Operation('<=', p[0], p[2])
    @_('somme SUPERIEUR somme')
    def booleen(self, p):
        return arbre_abstrait.Operation('>', p[0], p[2])
    @_('somme SUPERIEUR_OU_EGAL somme')
    def booleen(self, p):
        return arbre_abstrait.Operation('>=', p[0], p[2])

    @_('produit')
    def somme(self,p):
        return p[0]
    @_('expr "-" produit')
    def somme(self,p):
        return arbre_abstrait.Operation('-', p[0], p[2])
    @_('expr "+" produit')
    def somme(self, p):
        return arbre_abstrait.Operation('+', p[0], p[2])
    @_('"-" facteur')
    def somme(self, p):
        return arbre_abstrait.Operation('-', arbre_abstrait.Entier(0), p[1])

    @_('facteur')
    def produit(self, p):
        return p[0]
    @_('produit "*" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('*', p[0], p[2])
    @_('produit "/" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('/', p[0], p[2])
    @_('produit "%" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('%', p[0], p[2])


    @_('variable')
    def facteur(self, p):
        return p[0]
    @_('IDENTIFIANT "(" argument ")" ')
    def facteur(self, p):
        return arbre_abstrait.nomFonction(p[0], p[2])
    @_('IDENTIFIANT "(" ")"')
    def facteur(self, p):
        return arbre_abstrait.nomFonction(p[0], [])
    @_('LIRE "(" ")"')
    def facteur(self, p):
        return arbre_abstrait.Lire()
    @_('ENTIER')
    def facteur(self, p):
        return arbre_abstrait.Entier(p.ENTIER)
    @_('"(" expr ")"')
    def facteur(self, p):
        return p.expr


    @_('IDENTIFIANT')
    def variable(self, p):
        return arbre_abstrait.Variable(p[0])


    @_('expr "," argument')
    def argument(self, p):
        return [p[0]] + p[2]
    @_('expr')
    def argument(self, p):
        return [p[0]]


    '''
    @_('ECRIRE "(" expr ")" ";"')
    def ecrire(self, p):
        return arbre_abstrait.Ecrire(p.expr)  # p.expr = p[2]

    @_('expr "+" produit')
    def expr(self, p):
        return arbre_abstrait.Operation('+', p[0], p[2])

    @_('produit "*" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('*', p[0], p[2])

    @_('"(" expr ")"')
    def facteur(self, p):
        return p.expr  # ou p[1]

    @_('ENTIER')
    def facteur(self, p):
        return arbre_abstrait.Entier(p.ENTIER)  # p.ENTIER = p[0]

    @_('facteur')
    def produit(self, p):
        return p[0]

    @_('produit')
    def expr(self, p):
        return p[0]

    @_('produit "/" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('/', p[0], p[2])

    @_('"-" facteur')
    def expr(self, p):
        return arbre_abstrait.Operation('-', arbre_abstrait.Entier(0), p[1])

    @_('produit "%" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('%', p[0], p[2])

    @_('expr "-" produit')
    def expr(self, p):
        return arbre_abstrait.Operation('-', p[0], p[2])

    @_('LIRE "(" ")"')
    def facteur(self, p):
        return arbre_abstrait.Lire();

    @_('IDENTIFIANT ')
    def facteur(self,p):
        return arbre_abstrait.Variable(p[0])

    @_('IDENTIFIANT "(" ")"')
    def facteur(self,p):
        return arbre_abstrait.nomFonction(p[0],[])

    
    @_('expr "," argument')
    def argument(self,p):
        return [p[0]]+p[2]

    @_('expr')
    def argument(self, p):
        return [p[0]]

    @_('IDENTIFIANT "(" argument ")"')
    def facteur(self,p):
        return arbre_abstrait.nomFonction(p[0],p[2])
    '''


if __name__ == '__main__':
    lexer = FloLexer()
    parser = FloParser()
    if len(sys.argv) < 2:
        print("usage: python3 analyse_syntaxique.py NOM_FICHIER_SOURCE.flo")
    else:
        with open(sys.argv[1], "r") as f:
            data = f.read()
            try:
                arbre = parser.parse(lexer.tokenize(data))
                arbre.afficher()
            except EOFError:
                exit()