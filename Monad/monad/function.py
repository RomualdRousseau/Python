def identity(x):
    return x


def compose(f):
    return lambda g: lambda x: f(g(x))


def apply(a):
    return lambda f: f(a)


def curry(f):
    return lambda x: lambda y: f(x, y)
