from abc import ABC, abstractmethod
from src.interpreter.expr import LinearExpr

class AbstractDomain(ABC):
    @abstractmethod
    def print_domain_state(self, domain_state):
        pass

    @abstractmethod
    def assign_linexpr(self, var, linexpr:LinearExpr):
        pass