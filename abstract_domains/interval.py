from abstract_domains.abstract_domain import AbstractDomain

class Interval:
    def __init__(self, lo, hi):
        self.lo = lo
        self.hi = hi

    def __add__(self, other):
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def __sub__(self, other):
        return Interval(self.lo - other.hi, self.hi - other.lo)

    def __mul__(self, other):
        vals = [self.lo * other.lo, self.lo * other.hi,
                self.hi * other.lo, self.hi * other.hi]
        return Interval(min(vals), max(vals))

    def __repr__(self):
        return f"[{self.lo}, {self.hi}]"


class IntervalDomain(AbstractDomain):
    def __init__(self, initial_env):
        self.env = initial_env  # dict: var -> Interval

    def assign_linexpr(self, var, linexpr):
        result = Interval(0, 0)
        for v, c in linexpr.coeffs.items():
            if v not in self.env:
                raise ValueError(f"Variable {v} not in environment")
            val = self.env[v]
            result = result + val.__mul__(Interval(c, c))
        result = result + Interval(linexpr.offset, linexpr.offset)
        self.env[var] = result

    def __repr__(self):
        return str(self.env)