import ply.lex as lex
import ply.yacc as yacc

from ast_nodes import *
from variableC_interface import Variable_Interface

# ---------- CONTEXTE ----------
Variable_mng = Variable_Interface("vg-01.dll")
hashmap = Variable_mng.lib.Create_hashmap()

CTX = {
    "var_mng": Variable_mng,
    "hashmap": hashmap
}

# ---------- TOKENS ----------
tokens = (
    'NOMBRE',
    'IDENTIFIANT',
    'PLUS',
    'MOINS',
    'EGALE'
)

t_PLUS   = r'\+'
t_MOINS  = r'-'
t_EGALE  = r'='
t_ignore = ' \t'


def t_NOMBRE(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t



def t_IDENTIFIANT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


def t_error(t):
    raise Exception(f"Caractère invalide : {t.value[0]}")


# ---------- PARSER ----------
precedence = (
    ('left', 'PLUS', 'MOINS'),
)

def p_program(p):
    '''program : program statement
               | statement'''
    if len(p) == 3:
        p[0] = BlockNode(p[1].statements + [p[2]])
    else:
        p[0] = BlockNode([p[1]])


def p_statement_assign(p):
    'statement : IDENTIFIANT EGALE expression'
    p[0] = AssignNode(p[1], p[3])


def p_statement_expr(p):
    'statement : expression'
    p[0] = p[1]


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MOINS expression'''
    p[0] = BinOpNode(p[1], p[2], p[3])


def p_expression_number(p):
    'expression : NOMBRE'
    p[0] = NumberNode(p[1])


def p_expression_var(p):
    'expression : IDENTIFIANT'
    p[0] = VarNode(p[1])


def p_error(p):
    raise Exception("Erreur de syntaxe")

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



lexer = lex.lex()
parser = yacc.yacc()

code = """
a = 4
b=a+3
"""

ast = parser.parse(code)
result = ast.eval(CTX)

print("Résultat final =", result)