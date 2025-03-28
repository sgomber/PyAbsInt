import ast
from typing import Dict

class AbstractExpr:
    pass

class LinearExpr(AbstractExpr):
    def __init__(self, coeffs: Dict[str, float], offset: float):
        self.coeffs = coeffs
        self.offset = offset

    def scale(self, factor: float):
        return LinearExpr({k: v * factor for k, v in self.coeffs.items()}, self.offset * factor)

    @staticmethod
    def combine(lhs, rhs, op):
        coeffs = lhs.coeffs.copy()
        for k, v in rhs.coeffs.items():
            coeffs[k] = coeffs.get(k, 0) + (v if isinstance(op, (ast.Add,)) else -v)
        offset = lhs.offset + (rhs.offset if isinstance(op, (ast.Add,)) else -rhs.offset)
        return LinearExpr(coeffs, offset)

    def __repr__(self):
        terms = [f"{v}*{k}" for k, v in self.coeffs.items()]
        return " + ".join(terms + [str(self.offset)])