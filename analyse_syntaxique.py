import sys

from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait

class FloParser(Parser):
    # On récupère la liste des lexèmes de l'analyse lexicale
    tokens = FloLexer.tokens

    # gerer les precedences
    precedence = (
            ('left', 'ET'),
            ('left','OU'),
            ('right', 'NON'),
            ('right', 'EGAL'),
            ('left', '<', '>', 'INFERIEUR_EGAL', 'SUPERIEUR_EGAL', 'NON_EGAL'),
            ('left', '+', '-'),
            ('left', '*', '/', '%'),
            ('nonassoc', 'UMINUS'),
    )

    # Règles gramaticales et actions associées

    @_('listeInstructions')
    def prog(self, p):
        return arbre_abstrait.Programme(None,p[0])

    @_('listeFonctions listeInstructions')
    def prog(self, p):
        return arbre_abstrait.Programme(p[0],p[1])

    @_('fonction')
    def listeFonctions(self, p):
        l = arbre_abstrait.ListeFonctions()
        l.fonctions.insert(0,p[0])
        return l

    @_('listeFonctions fonction')
    def listeFonctions(self, p):
        p[0].fonctions.insert(0,p[1])
        return p[0]

    @_('TYPE_ENTIER IDENTIFIANT "(" listeParametres ")" "{" listeInstructions "}"',
       'TYPE_BOOLEEN IDENTIFIANT "(" listeParametres ")" "{" listeInstructions "}"')
    def fonction(self, p):
        return arbre_abstrait.Fonction(p[0],p.IDENTIFIANT,p.listeParametres,p.listeInstructions)

    @_('parametre')
    def listeParametres(self, p):
        l = arbre_abstrait.ListeParametres()
        l.parametres.append(p[0])
        return l

    @_('listeParametres "," parametre')
    def listeParametres(self, p):
        p[0].parametres.append(p[2])
        return p[0]

    @_('TYPE_ENTIER IDENTIFIANT',
       'TYPE_BOOLEEN IDENTIFIANT')
    def parametre(self, p):
        return arbre_abstrait.Parametre(p[0],p.IDENTIFIANT)

    @_('instruction')
    def listeInstructions(self, p):
        l = arbre_abstrait.ListeInstructions()
        l.instructions.append(p[0])
        return l

    @_('instruction listeInstructions')
    def listeInstructions(self, p):
        p[1].instructions.insert(0,p[0])
        return p[1]

    @_('ecrire',
       'declarationVariable',
       'affectation',
       'declarationAffectation',
       'conditionnelle',
       'boucleTantQue',
       'retourner',
       'appelFonction',)
    def instruction(self, p):
        return p[0]

    @_('ECRIRE "(" exprAll ")" ";"')
    def ecrire(self, p):
        return arbre_abstrait.Ecrire(p.exprAll)

    @_('TYPE_ENTIER IDENTIFIANT ";"',
       'TYPE_BOOLEEN IDENTIFIANT ";"')
    def declarationVariable(self, p):
        return arbre_abstrait.DeclarationVariable(p[0],p.IDENTIFIANT)

    @_('IDENTIFIANT "=" exprAll ";"')
    def affectation(self, p):
        return arbre_abstrait.Affectation(p.IDENTIFIANT,p.exprAll)

    @_('TYPE_ENTIER IDENTIFIANT "=" exprAll ";"',
         'TYPE_BOOLEEN IDENTIFIANT "=" exprAll ";"')
    def declarationAffectation(self, p):
        return arbre_abstrait.DeclarationAffectation(p[0],p.IDENTIFIANT,p.exprAll)

    @_('SI "(" exprAll ")" "{" listeInstructions "}"',
       'SI "(" exprAll ")" "{" listeInstructions "}" listeSinonSi',
       'SI "(" exprAll ")" "{" listeInstructions "}" SINON "{" listeInstructions "}"',
       'SI "(" exprAll ")" "{" listeInstructions "}" listeSinonSi SINON "{" listeInstructions "}"'
       )
    def conditionnelle(self, p):
        if len(p) == 7:
            return arbre_abstrait.Conditionnelle(p[2],p[5],None,None)
        elif len(p) == 8:
            return arbre_abstrait.Conditionnelle(p[2],p[5],p[7],None)
        elif len(p) == 11:
            return arbre_abstrait.Conditionnelle(p[2],p[5],None,p[9])
        elif len(p) == 12:
            return arbre_abstrait.Conditionnelle(p[2],p[5],p[7],p[10])


    @_('listeSinonSi SINON SI "(" exprAll ")" "{" listeInstructions "}"')
    def listeSinonSi(self, p):
        return arbre_abstrait.Conditionnelle(p[4],p[7],p[0],None)

    @_('SINON SI "(" exprAll ")" "{" listeInstructions "}"')
    def listeSinonSi(self, p):
        return arbre_abstrait.Conditionnelle(p[3],p[6],None,None)

    @_('TANT_QUE "(" exprAll ")" "{" listeInstructions "}"')
    def boucleTantQue(self, p):
        return arbre_abstrait.BoucleTantQue(p[2],p[5])

    @_("RETOURNER exprAll ';' ")
    def retourner(self, p):
        return arbre_abstrait.Retourner(p.exprAll)

    @_('IDENTIFIANT "(" listeExpr ")" ";"')
    def appelFonction(self, p):
        return arbre_abstrait.AppelFonction(p.IDENTIFIANT,p.listeExpr)


    @_('exprAll')
    def listeExpr(self, p):
        l = arbre_abstrait.ListeExpressions()
        l.expressions.append(p[0])
        return l

    @_('exprAll "," listeExpr')
    def listeExpr(self, p):
        p[2].expressions.insert(0,p[0])
        return p[2]


    @_('booleen')
    def exprAll(self, p):
        return p[0]

    @_('VRAI',
       'FAUX')
    def booleen(self, p):
        return arbre_abstrait.Booleen(p[0])

    @_('expr')
    def booleen(self, p):
        return p[0]

    @_('booleen ET booleen',
       'booleen OU booleen')
    def booleen(self, p):
        return arbre_abstrait.Operation(p[1],p[0],p[2])

    @_('NON booleen')
    def booleen(self, p):
        return arbre_abstrait.Operation(p[0],p[1],None)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return arbre_abstrait.Operation("*",arbre_abstrait.Entier(-1),p.expr) #p.expr = p[1]

    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr',
       'expr "%" expr',
       'expr "<" expr',
       'expr ">" expr',
       'expr EGAL expr',
       'expr NON_EGAL expr',
       'expr INFERIEUR_EGAL expr',
       'expr SUPERIEUR_EGAL expr',)
    def expr(self, p):
        return arbre_abstrait.Operation(p[1],p[0],p[2])

    @_('"(" booleen ")"')
    def expr(self, p):
        return p[1]

    @_('ENTIER')
    def facteur(self, p):
        return arbre_abstrait.Entier(p.ENTIER) #p.ENTIER = p[0]

    @_('IDENTIFIANT')
    def facteur(self, p):
        return arbre_abstrait.Variable(p.IDENTIFIANT)


    @_('facteur')
    def expr(self,p):
        return p[0]

    @_('LIRE "(" ")"')
    def facteur(self,p):
        return arbre_abstrait.Lire()

    @_('IDENTIFIANT "(" listeExpr ")"')
    def facteur(self,p):
        return arbre_abstrait.AppelFonction(p.IDENTIFIANT,p.listeExpr)

    @_('IDENTIFIANT "(" ")"')
    def facteur(self,p):
        return arbre_abstrait.AppelFonction(p.IDENTIFIANT,arbre_abstrait.ListeExpressions())




if __name__ == '__main__':
    lexer = FloLexer()
    parser = FloParser()
    if len(sys.argv) < 2:
        print("usage: python3 analyse_syntaxique.py NOM_FICHIER_SOURCE.flo")
    else:
        with open(sys.argv[1],"r") as f:
            data = f.read()
            try:
                arbre = parser.parse(lexer.tokenize(data))
                arbre.afficher()
            except EOFError:
                exit()