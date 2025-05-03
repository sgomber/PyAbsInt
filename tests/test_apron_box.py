import unittest

from apronpy.interval import PyDoubleInterval
from apronpy.var import PyVar

from src.abstract_domains.apron_box_handler import ApronBoxDomain
from src.interpreter.engine import AbstractInterpreterConfig, AbstractInterpreter

class TestApronBox(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.test_programs_folder = "../test_programs/"
        self.box_handler=ApronBoxDomain()
        self.config = AbstractInterpreterConfig(domain_handler=self.box_handler)
        self.abs_interpreter = AbstractInterpreter(self.config)
    
    def _compare_states(self, expected_env, output):
        same_keys = set(expected_env.keys()) == set(expected_env.keys())
        self.assertTrue(same_keys, "Output and expected ans have different keys")

        for k in expected_env:
            expected_interval = PyDoubleInterval(expected_env[k][0], expected_env[k][1])
            self.assertTrue(expected_interval == output.box.bound_variable(PyVar(k)), f"For {k}, {expected_interval} != {output.box.bound_variable(PyVar(k))}")

    def test_1(self):
        filename = self.test_programs_folder + "t1.py"
        funcname = "func"
        initial_env = {
            'x': (0, 5),
            'y': (0, 5)
        }

        expected_output_env = {
            'x': (0, 5),
            'y': (0, 5),
            'a': (0, 10),
            'b': (-5, 5),
            'c': (-5, 15),
            'd': (2, 2)
        }

        final_state = self.abs_interpreter.execute(filename, funcname, initial_env)
        self._compare_states(expected_output_env, final_state)

    def test_2(self):
        filename = self.test_programs_folder + "t2.py"
        funcname = "func"
        initial_env = {
            'x': (0, 5),
            'y': (0, 5)
        }

        expected_output_env = {
            'x': (0, 5),
            'y': (0, 5),
            'a': (0, 10),
            'b': (-5, 5),
            'c': (-5, 15),
            'd': (1, 2)
        }

        final_state = self.abs_interpreter.execute(filename, funcname, initial_env)
        self._compare_states(expected_output_env, final_state)

    def test_3(self):
        filename = self.test_programs_folder + "t3.py"
        funcname = "func"
        initial_env = {
            'x': (0, 5),
            'y': (0, 5)
        }

        expected_output_env = {
            'x': (1, float('inf')),
            'y': (32, float('inf')),
        }

        final_state = self.abs_interpreter.execute(filename, funcname, initial_env)
        self._compare_states(expected_output_env, final_state)

    def test_4(self):
        filename = self.test_programs_folder + "t4.py"
        funcname = "func"
        initial_env = {
            'x': (0, 5),
            'y': (0, 5)
        }

        expected_output_env = {
            'x': (2, float('inf')),
            'y': (1, float('inf')),
            'c': (16, float('inf')),
        }

        final_state = self.abs_interpreter.execute(filename, funcname, initial_env)
        self._compare_states(expected_output_env, final_state)

if __name__ == "__main__":
    unittest.main()