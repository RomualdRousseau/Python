import monad
from monad import do

class AST:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right


class Value:
    def __init__(self, value, ast, stream):
        self.value = value
        self.ast = ast
        self.stream = stream


class Parser(monad.Monad):
    def __or__(self, other):
        if isinstance(self, Accept) or isinstance(self, Error):
            return self
        else:
            return other


class Accept(Parser):
    def __init__(self, value):
        super().__init__(value)

    def pure(v):
        return Accept(v) 

    def withFilter(self, f):
        return self if f(self.value) else NotAccept(self.value)

    def __repr__(self):
        return f"Accept({self.value.value})"


class NotAccept(Parser):
    def __init__(self, value):
        super().__init__(value)

    def map(self, f):
        return self

    def pure(v):
        return NotAccept(v)

    def ap(self, other):
        return self

    def flatMap(self, f):
        return self

    def withFilter(self, f):
        return self

    def __repr__(self):
        return f"NotAccept({self.value.stream})"


class Error(NotAccept):
    def __init__(self, value, msg = None):
        super().__init__(value)
        self.msg = msg

    def pure(v):
        return Error(v)

    def __repr__(self):
        return f"Error({self.value.stream}, {self.msg})"


class ErrorDivisionByZero(Error):
    def __init__(self, value):
        super().__init__(value, "division by zero")


def char(c, v):
    if len(v.stream) > 0 and v.stream[0] == c:
        return Accept(Value(v.value, v.ast, v.stream[1:]))
    else:
        return NotAccept(v)


def digit(v):
    if len(v.stream) > 0 and v.stream[0].isdigit():
        return Accept(Value(int(v.stream[0]), AST(v.stream[0], None, None), v.stream[1:]))
    else:
        return NotAccept(v)


def num(v):
    def num_(v):
        if len(v.stream) > 0 and v.stream[0].isdigit():
            return num_(Value(v.value * 10 + int(v.stream[0]), AST(v.value + v.stream[0], None, None), v.stream[1:]))
        else:
            return Accept(v)
    return digit(v) >> num_


def end(v):
    if len(v.stream) == 0:
        return Accept(v)
    else:
        return Error(v)


def add(x, y):
    return Accept(Value(x.value + y. value, AST("add", x.ast, y.ast), y.stream))


def sub(x, y):
    return Accept(Value(x.value - y.value, AST("sub", x.ast, y.ast), y.stream))


def mul(x, y):
    return Accept(Value(x.value * y.value, AST("mul", x.ast, y.ast), y.stream))


def safe_div(x, y):
    if y.value != 0:
        return Accept(Value(x.value / y.value, AST("div", x.ast, y.ast), y.stream))
    else:
        return ErrorDivisionByZero(x)


def eval(s):
    return expr(Value(0, None, s)) >> end


def expr(v):
    return do(
            term(v), lambda x: do(
            char('+', x),
            expr, 
            monad.function.curry(add)(x))
        ) | do(
            term(v), lambda x: do(
            char('-', x),
            expr,
            monad.function.curry(sub)(x))
        ) | term(v)


def term(v):
    return do(
            factor(v), lambda x: do(
            char('*', x),
            term, 
            monad.function.curry(mul)(x))
        ) | do(
            factor(v), lambda x: do(
            char('/', x),
            term,
            monad.function.curry(safe_div)(x))
        ) | factor(v)


def factor(v):
    return do(
            char('(', v),
            expr,
            monad.function.curry(char)(')')
        ) | num(v)


def print_ast(root, indent = 0):
    print(" " * indent, root.value)
    if root.left != None:
        print_ast(root.left, indent + 4)
    if root.right != None:
        print_ast(root.right, indent + 4)
