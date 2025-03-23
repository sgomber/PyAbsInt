import ast
from interpreter.engine import AbstractInterpreter
from abstract_domains.interval import Interval, IntervalDomain

code = """
def func():
    x = 2*a - b - 3
    y = -2*x + 1
"""

tree = ast.parse(code)
func = tree.body[0]

initial_env = {
    'a': Interval(-2, -1),
    'b': Interval(0, 4)
}

domain = IntervalDomain(initial_env)
interpreter = AbstractInterpreter(domain)
interpreter.visit(func)

print("Final state:", domain)