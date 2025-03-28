import ast
from src.interpreter.engine import AbstractInterpreter
from src.abstract_domains.apron_box import ApronBoxDomain

code = """
def func():
    x = 2*a - b - 3
    y = -2*x + 1
"""

tree = ast.parse(code)
func = tree.body[0]

initial_env = {
    'a': (-2, -1),
    'b': (0, 4)
}

domain = ApronBoxDomain(initial_env)
interpreter = AbstractInterpreter(domain)
interpreter.visit(func)

print("Final state:", domain)