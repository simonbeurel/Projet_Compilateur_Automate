import sys
from sly import Lexer


class FloLexer(Lexer):

    tokens = {  IDENTIFIANT, ENTIER, ECRIRE, LIRE, TYPE_ENTIER, TYPE_BOOLEEN,
                INFERIEUR_EGAL, SUPERIEUR_EGAL, EGAL, NON_EGAL,
                ET, OU, NON, VRAI, FAUX,
                SI, SINON,TANT_QUE, RETOURNER,
              }

    literals = {'+', '-', '*', '/', '%', '(', ')', ";", '{', '}', '<', '>', '=', '!', ','}
    ignore = ' \t'
    ignore_comment = r'\#.*'
    @_(r'0|[1-9][0-9]*')
    def ENTIER(self, t):
        t.value = int(t.value)
        return t

    # Identifiants
    IDENTIFIANT = r'[a-zA-Z][a-zA-Z0-9_]*' # pour nommer les variables et les fonctions

    # cas particulier
    IDENTIFIANT['si'] = SI

    IDENTIFIANT['sinon'] = SINON
    IDENTIFIANT['tantque'] = TANT_QUE
    IDENTIFIANT['lire'] = LIRE
    IDENTIFIANT['ecrire'] = ECRIRE
    IDENTIFIANT['et'] = ET
    IDENTIFIANT['ou'] = OU
    IDENTIFIANT['non'] = NON
    IDENTIFIANT['Vrai'] = VRAI
    IDENTIFIANT['Faux'] = FAUX
    IDENTIFIANT['retourner'] = RETOURNER

    # type
    IDENTIFIANT['booleen'] = TYPE_BOOLEEN
    IDENTIFIANT['entier'] = TYPE_ENTIER

    # Opérateurs
    INFERIEUR_EGAL = r'<='
    SUPERIEUR_EGAL = r'>='
    EGAL = r'=='
    NON_EGAL = r'!='

    # Instructions

    # OPEN_PAR = r'\(' # a voir si on met
    # CLOSE_PAR = r'\)' # a voir si on met
    # OPEN_ACC = r'\{' # a voir si on met
    # CLOSE_ACC = r'\}' # a voir si on met
    # PVIRGULE = r';' # a voir si on met


    # Permet de conserver les numéros de ligne. Utile pour les messages d'erreurs
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # En cas d'erreur, indique où elle se trouve
    def error(self, t):
        print(f'Ligne{self.lineno}: caractère inattendu "{t.value[0]}"')
        self.index += 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python3 analyse_lexicale.py NOM_FICHIER_SOURCE.flo")
    else:
        with open(sys.argv[1], "r") as f:
            data = f.read()
            lexer = FloLexer()
            for tok in lexer.tokenize(data):
                print(tok)