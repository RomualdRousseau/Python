from functools import reduce

import monad

class Monad:
    def __init__(self, value):
        self.value = value

    # Functor

    def map(self, f):
        return self.__class__.pure(f(self.value))

    def __gt__(self, f):
        return self.map(f)

    # Applicative

    def pure(a):
        return Monad(a)

    def ap(self, other):
        return self >> (lambda fab: other > fab)

    def __lshift__(self, other):
        return self.ap(other)

    # Monad

    def flatMap(self, f):
        return f(self.value)

    def __rshift__(self, f):
        return self.flatMap(f)

    # Filter

    def withFilter(self, f):
        pass

    def __mod__(self, f):
        return self.withFilter(f)

    def __eq__(self, other):
        return str(self) == str(other)

    def __repr__(self):
        return f"Monad({self.value})"


def do(*args):
    """ Do comprehension ala haskell allowing PF with "effects"
    """
    return reduce(lambda r, a: r >> a, args)
