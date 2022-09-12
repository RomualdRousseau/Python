class Kleisli:
    def __init__(self, f):
        self.f = f

    def __rshift__(self, other):
        return Kleisli(lambda a: self.f(a) >> other.f)

    def __eq__(self, other):
        return lambda a: self.f(a) == other.f(a)
