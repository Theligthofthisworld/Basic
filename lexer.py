import ply.lex as lex
import ply.yacc as yacc

from ast_nodes import *
from variableC_interface import Variable_Interface


class Interpreter:
    reserved = {
        "si": "IF",
        "alors": "THEN",
        "sinon": "ELSE",
    }

    tokens = (
        "NOMBRE",
        "IDENTIFIANT",
        "PLUS",
        "MOINS",
        "EGALE",
        "DOUBLE_EGALE",
        "INFERIEUR_EGALE",
        "SUPERIEUR_EGALE",
        "INFERIEUR",
        "SUPERIEUR",
        "DIFFERENT",
        "STRING",
        "LPAREN",
        "RPAREN",
        "LBRACE",
        "RBRACE",
        "IF",
        "THEN",
        "ELSE",
    )

    t_PLUS = r"\+"
    t_MOINS = r"-"
    t_DOUBLE_EGALE = r"=="
    t_INFERIEUR_EGALE=r"<="
    t_SUPERIEUR_EGALE=r">="
    t_INFERIEUR=r"<"
    t_SUPERIEUR=r">"
    t_DIFFERENT=r"!="
    t_EGALE = r"="
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_LBRACE = r"\{"
    t_RBRACE = r"\}"
    t_ignore = " \t"

    precedence = (
        ("left", "DOUBLE_EGALE", "INFERIEUR_EGALE", "SUPERIEUR_EGALE", "INFERIEUR", "SUPERIEUR","DIFFERENT"),
        ("left", "PLUS", "MOINS"),
    )

    def __init__(self, dll_path="vg-01.dll"):
        self.var_mng = Variable_Interface(dll_path)
        self.hashmap = self.var_mng.lib.Create_hashmap()
        self.ctx = {
            "var_mng": self.var_mng,
            "hashmap": self.hashmap,
        }
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

    def reset_context(self):
        self.hashmap = self.var_mng.lib.Create_hashmap()
        self.ctx = {
            "var_mng": self.var_mng,
            "hashmap": self.hashmap,
        }

    def t_NOMBRE(self, t):
        r"-?\d+(\.\d+)?"
        if "." in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'"([^"\\]|\\.)*"'
        t.value = t.value[1:-1]
        return t

    def t_IDENTIFIANT(self, t):
        r"[a-zA-Z_][a-zA-Z0-9_]*"
        t.type = self.reserved.get(t.value, "IDENTIFIANT")
        return t

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        raise Exception(f"Caractere invalide : {t.value[0]}")

    def p_program(self, p):
        "program : statements"
        p[0] = BlockNode(p[1])

    def p_statements_many(self, p):
        "statements : statements statement"
        p[0] = p[1] + [p[2]]

    def p_statements_one(self, p):
        "statements : statement"
        p[0] = [p[1]]

    def p_statement_assign(self, p):
        "statement : IDENTIFIANT EGALE expression"
        p[0] = AssignNode(p[1], p[3])

    def p_statement_if(self, p):
        "statement : IF expression THEN statement"
        p[0] = IfNode(p[2], p[4])

    def p_statement_if_else(self, p):
        "statement : IF expression THEN statement ELSE statement"
        p[0] = IfNode(p[2], p[4], p[6])

    def p_statement_block(self, p):
        "statement : block"
        p[0] = p[1]

    def p_statement_expr(self, p):
        "statement : expression"
        p[0] = p[1]

    def p_block_many(self, p):
        "block : LBRACE statements RBRACE"
        p[0] = BlockNode(p[2])

    def p_block_empty(self, p):
        "block : LBRACE RBRACE"
        p[0] = BlockNode([])

    def p_expression_compare(self, p):
        """expression : expression DOUBLE_EGALE expression
        | expression INFERIEUR_EGALE expression
        | expression SUPERIEUR_EGALE expression
        | expression INFERIEUR expression
        | expression SUPERIEUR expression
        | expression DIFFERENT expression"""
        p[0] = CompareNode(p[1], p[2], p[3])


    def p_expression_binop(self, p):
        """expression : expression PLUS expression
        | expression MOINS expression"""
        p[0] = BinOpNode(p[1], p[2], p[3])

    def p_expression_number(self, p):
        "expression : NOMBRE"
        p[0] = NumberNode(p[1])

    def p_expression_var(self, p):
        "expression : IDENTIFIANT"
        p[0] = VarNode(p[1])

    def p_expression_string(self, p):
        "expression : STRING"
        p[0] = StringNode(p[1])

    def p_expression_group(self, p):
        "expression : LPAREN expression RPAREN"
        p[0] = p[2]

    def p_error(self, p):
        raise Exception("Erreur de syntaxe")

    def parse(self, code):
        return self.parser.parse(code, lexer=self.lexer)

    def run(self, code):
        ast = self.parse(code)
        return ast.eval(self.ctx)


if __name__ == "__main__":
    interpreter = Interpreter()
    code = """
a = 1
si (a == 4) alors {
    b = "ok"
    c = "bloc"
    c
} sinon {
    si a<4 alors b="non"
}
b
"""
    result = interpreter.run(code)
    print("Resultat final =", result)
