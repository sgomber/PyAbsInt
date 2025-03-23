import ast
from interpreter.expr import LinearExpr
from interpreter.parser import parse_expr

class AbstractInterpreter(ast.NodeVisitor):
    def __init__(self, domain):
        self.domain = domain

    def visit_FunctionDef(self, node):
        for stmt in node.body:
            self.visit(stmt)

    def visit_Assign(self, node):
        var = node.targets[0].id
        expr = parse_expr(node.value)
        if isinstance(expr, LinearExpr):
            self.domain.assign_linexpr(var, expr)