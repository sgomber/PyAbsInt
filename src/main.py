import ast
from src.interpreter.engine import AbstractInterpreter
from src.abstract_domains.apron_box_handler import ApronBoxDomain

code = """
def func():
    a = x + y
    b = x - y
    c = a + b
    if c < -6:
        d = 1
    else:
        d = 2
"""

tree = ast.parse(code)
func = tree.body[0]

initial_env = {
    'x': (0, 5),
    'y': (0, 5)
}

domain = ApronBoxDomain()
interpreter = AbstractInterpreter(domain, initial_env)
interpreter.visit(func)

print("Final state:")
domain.print_state(interpreter._curr_state)