import ply.lex as lex
import ply.yacc as yacc

from ast_nodes import AssignNode, BinOpNode, BlockNode, NumberNode, StringNode, VarNode
from variableC_interface import Variable_Interface


class Interpreter:
    tokens = (
        "NOMBRE",
        "IDENTIFIANT",
        "PLUS",
        "MOINS",
        "EGALE",
        "STRING",
    )

    t_PLUS = r"\+"
    t_MOINS = r"-"
    t_EGALE = r"="
    t_ignore = " \t"

    precedence = (
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
        return t

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        raise Exception(f"Caractere invalide : {t.value[0]}")

    def p_program(self, p):
        """program : program statement
        | statement"""
        if len(p) == 3:
            p[0] = BlockNode(p[1].statements + [p[2]])
        else:
            p[0] = BlockNode([p[1]])

    def p_statement_assign(self, p):
        "statement : IDENTIFIANT EGALE expression"
        p[0] = AssignNode(p[1], p[3])

    def p_statement_expr(self, p):
        "statement : expression"
        p[0] = p[1]

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
a = "frf"
a
"""
    result = interpreter.run(code)
    print("Resultat final =", result)
