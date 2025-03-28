import ast

from src.abstract_domains.apron_box_handler import ApronBoxDomain
from src.interpreter.engine import AbstractInterpreterConfig, AbstractInterpreter

if __name__ == "__main__":
    box_handler=ApronBoxDomain()
    config = AbstractInterpreterConfig(domain_handler=box_handler)
    abs_interpreter = AbstractInterpreter(config)

    filename = "../tests/t3.py"
    funcname = "func"
    initial_env = {
        'x': (0, 5),
        'y': (0, 5)
    }

    final_state = abs_interpreter.execute(filename, funcname, initial_env)
    box_handler.print_state(final_state)
