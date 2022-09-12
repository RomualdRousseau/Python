import monad

class Parser(monad.Monad):
    def __or__(self, other):
        if isinstance(self, Accept):
            return self
        else:
            return other


class Accept(Parser):
    def __init__(self, value):
        super().__init__(value)

    def pure(v):
        return Accept(v) 

    def withFilter(self, f):
        return self if f(self.value) else Error(self.value)

    def __repr__(self):
        return f"Accept({self.value})"


class Error(Parser):
    def __init__(self, value):
        super().__init__(value)

    def map(self, f):
        return Error(self.value)

    def pure(v):
        return Error(v)

    def ap(self, other):
        return Error(self.value)

    def flatMap(self, f):
        return Error(self.value)

    def withFilter(self, f):
        return Error(self.value)

    def __repr__(self):
        return f"Error({self.value})"


def char(c, v):
    acc, stream = v
    if len(stream) > 0 and stream[0] == c:
        return Accept((acc, stream[1:]))
    else:
        return Error(v)


def digit(v):
    acc, stream = v
    if len(stream) > 0 and stream[0].isdigit():
        return Accept((int(stream[0]), stream[1:]))
    else:
        return Error(v)


def num(v):
    acc, stream = v
    if len(stream) > 0 and stream[0].isdigit():
        return num((acc * 10 + int(stream[0]), stream[1:]))
    else:
        return Accept(v)


def end(v):
    acc, stream = v
    if len(stream) == 0:
        return Accept((acc, ""))
    else:
        return Error(v)


def add(x, y):
    return x + y


def sub(x, y):
    return x - y


def mul(x, y):
    return x * y


def div(x, y):
    return x / y


def op(f):
    return lambda x: lambda y: Accept((f(x[0], y[0]), y[1]))


def safe_div(x):
    return lambda y: Accept((div(x[0], y[0]), y[1])) if y[0] != 0 else Error(x)


def eval(s):
    return expr((0, s)) >> end


def expr(v):
    return monad.do(
            term(v), lambda x: monad.do(
            monad.function.curry(char)('+')(x),
            expr,
            op(add)(x))
        ) | monad.do(
            term(v), lambda x: monad.do(
            monad.function.curry(char)('-')(x),
            expr,
            op(sub)(x))
        ) | term(v)


def term(v):
    return monad.do(
            factor(v), lambda x: monad.do(
            monad.function.curry(char)('*')(x),
            term,
            op(mul)(x))
        ) | monad.do(
            factor(v), lambda x: monad.do(
            monad.function.curry(char)('/')(x),
            term,
            safe_div(x))
        ) | factor(v)


def factor(v):
    return monad.do(
            monad.function.curry(char)('(')(v),
            expr,
            monad.function.curry(char)(')')
        ) | monad.do(
            digit(v),
            num
        )
