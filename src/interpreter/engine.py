import ast
from dataclasses import dataclass

from src.abstract_domains.abstract_domain_handler import AbstractDomainHandler
from src.interpreter.expr_cons import LinearConstraint, LinearExpr, Op
from src.interpreter.parser import parse_cons, parse_expr
from src.utils import get_function_ast, read_code_from_file

@dataclass
class AbstractInterpreterConfig:
    # Required fields
    domain_handler: AbstractDomainHandler

class AbstractInterpreter(ast.NodeVisitor):
    def __init__(self, config:AbstractInterpreterConfig):
        super().__init__()
        self.domain_handler = config.domain_handler
        self._init_state = None
        self._curr_state = None

    def execute(self, code_filename, function_name, init_state_config = None):
        # Parse code and get function
        code = read_code_from_file(code_filename)
        func_ast = get_function_ast(code, function_name)

        # Set initial and current state
        self._init_state = self.domain_handler.get_init_state(init_state_config)
        self._curr_state = self._init_state

        self.visit(func_ast)

        return self._curr_state

    def visit_FunctionDef(self, node):
        for stmt in node.body:
            self.visit(stmt)

    def visit_arg(self, node):
        # Ignore argument nodes completely for now
        pass

    def visit_Assign(self, node):
        var = node.targets[0].id
        expr = parse_expr(node.value)
        if isinstance(expr, LinearExpr):
            self.domain_handler.assign_linexpr(self._curr_state, var, expr)

    def visit_If(self, node):
        condition = parse_cons(node.test)

        if not isinstance(condition, LinearConstraint):
            raise NotImplementedError("Non-linear cons: " + condition)
        
        if_cond_copy = self.domain_handler.copy_state(self._curr_state)
        else_cond_copy = self.domain_handler.copy_state(self._curr_state)

        # If branch
        self.domain_handler.meet_lincons(if_cond_copy, condition)
        self._curr_state = if_cond_copy
        self.visit(node.body)
        if_cond_copy = self.domain_handler.copy_state(self._curr_state)

        # Else branch
        condition.op = Op.negate(condition.op)
        self.domain_handler.meet_lincons(else_cond_copy, condition)
        self._curr_state = else_cond_copy
        self.visit(node.orelse)
        else_cond_copy = self.domain_handler.copy_state(self._curr_state)

        # Join
        self._curr_state = self.domain_handler.join(if_cond_copy, else_cond_copy)

    def visit_list(self, node):
        return [self.visit(elt) for elt in node]

    ##
    ## generic_visit is unimplemented so that we know what happens exactly.
    ## The other functions that call generic_visit are set on purpose.
    ##
    def generic_visit(self, node):
        raise NotImplementedError(f"Visit to node type {type(node)} not implemented.")
    
    def visit_Module(self, node: ast.Module):
        return super().generic_visit(node)

    def visit_FunctionDef(self, node: ast.Module):
        return super().generic_visit(node)

    def visit_arguments(self, node: ast.Module):
        return super().generic_visit(node)