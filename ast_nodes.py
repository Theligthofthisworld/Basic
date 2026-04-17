# ast_nodes.py
<<<<<<< HEAD
from variableC_interface import Variable_Interface
import ctypes
=======

>>>>>>> temp_merge_66e54ad

class StringNode:
    def __init__(self, value):
        self.value = value

    def eval(self, ctx):
        return self.value


class BoolNode:
    def __init__(self, value):
        self.value = value

    def eval(self, ctx):
        return self.value


class NumberNode:
    def __init__(self, value):
        self.value = value

    def eval(self, ctx):
        return self.value


class VarNode:
    def __init__(self, name):
        self.name = name

    def eval(self, ctx):
        found, var = ctx["var_mng"].search_var(self.name, ctx["hashmap"])
        if not found:
            raise Exception(f"Variable '{self.name}' non definie")

        v = ctx["var_mng"].get_pointer_value(var)
        if v.type == 0:
            return v.value.i
        elif v.type == 1:
            return v.value.f
        elif v.type == 2:
            return ctx["var_mng"].get_string_value(v.value.s)
        elif v.type == 3:
            return bool(v.value.b)

        raise Exception("Type de variable inconnu")


class CompareNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def eval(self, ctx):
        l = self.left.eval(ctx)
        r = self.right.eval(ctx)
        if self.op == "==":
            return l == r
        elif self.op == "!=":
            return l != r
        elif self.op =="<=":
            return l<=r
        elif self.op==">=":
            return l>=r
        elif self.op=="<":
            return l<r
        elif self.op==">":
            return l>r

        raise Exception("Operateur de comparaison inconnu")


class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def eval(self, ctx):
        l = self.left.eval(ctx)
        r = self.right.eval(ctx)

        if self.op == "+":
            if type(l) == float or type(r) == float:
                temp_l = ctx["var_mng"].lib.make(l)
                temp_r = ctx["var_mng"].lib.make(r)
                return ctx["var_mng"].lib.add_double(temp_l, temp_r)
            return l + r

        if self.op == "-":
            return l - r

        raise Exception("Operateur inconnu")


class AssignNode:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def _store_variable(self, ctx, var):
        old_var = ctx["var_mng"].lib.hashmap_set(ctx["hashmap"], var)
        if old_var != ctx["var_mng"].ffi.NULL:
            ctx["var_mng"].lib.Var_free(old_var)

    def eval(self, ctx):
        value = self.expr.eval(ctx)

        if type(value) == bool:
            var = ctx["var_mng"].lib.CREATE_BOOL(
                int(value),
                self.name.encode("utf-8")
            )
            self._store_variable(ctx, var)
        elif type(value) == int:
            var = ctx["var_mng"].lib.CREATE_INTEGER(
                value,
                self.name.encode("utf-8")
            )
            self._store_variable(ctx, var)
        elif type(value) == float:
            var = ctx["var_mng"].lib.CREATE_FLOAT(
                value,
                self.name.encode("utf-8")
            )
            self._store_variable(ctx, var)
        elif type(value) == str:
            var = ctx["var_mng"].lib.CREATE_STRING(
                value.encode("utf-8"),
                self.name.encode("utf-8")
            )
            self._store_variable(ctx, var)

        return value


class IfNode:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def eval(self, ctx):
        if self.condition.eval(ctx):
            return self.then_branch.eval(ctx)
        if self.else_branch is not None:
            return self.else_branch.eval(ctx)
        return None


class BlockNode:
    def __init__(self, statements):
        self.statements = statements

    def eval(self, ctx):
        last = None
        for stmt in self.statements:
            last = stmt.eval(ctx)
        return last
<<<<<<< HEAD

if __name__=="__main__":
    a=Variable_Interface("vg-01.dll")
    hasmap=a.lib.Create_hashmap()
    s=a.lib.CREATE_STRING(b"hashmap",b"hff")
    print(a.get_string_value(s.name))
=======
>>>>>>> temp_merge_66e54ad
