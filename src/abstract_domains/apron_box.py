from src.abstract_domains.abstract_domain import AbstractDomain
from src.interpreter.expr import LinearExpr

from apronpy.box import PyBox, PyBoxDManager
from apronpy.coeff import PyDoubleScalarCoeff
from apronpy.environment import PyEnvironment
from apronpy.interval import PyDoubleInterval
from apronpy.linexpr1 import PyLinexpr1
from apronpy.var import PyVar

class ApronBoxDomain(AbstractDomain):
    def _add_var(self, var):
        pyvar = PyVar(var)

        # If var already there, then return
        if pyvar in self._state.environment:
            return
        
        self._state.environment = self._state.environment.add(real_vars=[pyvar])
        self._state = self._state.forget([pyvar])

    def _parse_initial_env(self, initial_env):
        if initial_env == None:
            return
        
        for var, bounds in initial_env.items():
            self._add_var(var)
            new_box = PyBox(self._man, self._state.environment, variables=[PyVar(var)], intervals=[PyDoubleInterval(bounds[0], bounds[1])])
            self._state = self._state.meet(new_box)

    def __init__(self, initial_env = None):
        self._man = PyBoxDManager()
        self._state = PyBox.top(self._man, PyEnvironment())
        self._parse_initial_env(initial_env)

    def print_domain_state(self, domain_state):
        print(domain_state)

    def _linexpr_to_apron_linexpr(self, linexpr:LinearExpr):
        expr = PyLinexpr1(self._state.environment)

        for var, coeff in linexpr.coeffs.items():
            pyvar = PyVar(var)
            expr.set_coeff(pyvar, PyDoubleScalarCoeff(coeff))
        
        expr.set_cst(PyDoubleScalarCoeff(linexpr.offset))

        return expr

    def assign_linexpr(self, var, linexpr:LinearExpr):
        expr = self._linexpr_to_apron_linexpr(linexpr)
        self._add_var(var)
        self._state = self._state.assign(PyVar(var), expr)

    def __repr__(self):
        return str(self._state)