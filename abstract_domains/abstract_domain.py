from abc import ABC, abstractmethod
from interpreter.expr import LinearExpr

class AbstractDomain(ABC):
    @abstractmethod
    def assign_linexpr(self, var, linexpr:LinearExpr):
        pass