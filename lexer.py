import ply.lex as lex
import ply.yacc as yacc
from variableC_interface import CInterface_V

if __name__=="__main__":
    CInterface=CInterface_V(r"vg-01.dll")
    hashmap=CInterface.lib.Create_hashmap()



# ----- TOKENS -----
tokens = ('NOMBRE', 'IDENTIFIANT', 'PLUS', 'MOINS', 'EGALE')

t_PLUS = r'\+'
t_MOINS = r'-'
t_EGALE = r'='
t_ignore = ' \t'

def t_NOMBRE(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIANT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_error(t):
    print(f"Caractère inconnu: {t.value[0]}")
    t.lexer.skip(1)

# ----- PARSER -----
def p_expression_plus(p):
    'expression : expression PLUS expression'
    p[0] = p[1] + p[3]

def p_expression_nombre(p):
    'expression : NOMBRE'
    p[0] = p[1]
def p_expression_identifiant(p):
    'expression : IDENTIFIANT EGALE NOMBRE'
    p[0]=[p[1],p[3]]
    varr=CInterface.lib.CREATE_INTEGER(p[3],bytes(p[1].encode()))
    CInterface.lib.hashmap_set(hashmap,varr)

def p_error(p):
    print("Erreur de syntaxe !")

# ----- CONSTRUCTION -----
lexer = lex.lex()
parser = yacc.yacc()

# ----- TEST -----
resultat = parser.parse(" name = 15 ")
print("Résultat =", resultat)
arr=CInterface.ffi.new("struct Variable *")
arr.type=0
arr.name=CInterface.ffi.new("char[]",b"name")
varr=CInterface.lib.hashmap_get(hashmap,arr)
var_ptr = CInterface.get_pointer_value(varr)
print(CInterface.get_string_value(var_ptr.name))



