import unittest
from monad import *
from main import *

f = lambda x: x * 2
g = lambda x: x + 2
h = lambda x, y: x + y
u = Monad(f)
v = Monad(g)

class TestMonadMethods(unittest.TestCase):

    def test_allTrue(self):
        self.assertAllTrue(lambda a: a == a, "All are true")

    def test_compose(self):
        self.assertEqual(function.compose(f)(g)(5), f(g(5)))

    def test_curry(self):
        self.assertEqual(h(2, 3), 5)
        self.assertEqual(function.curry(h)(2)(3), h(2, 3))

    def test_applicative(self):
        # Identity
        r = lambda a: Monad.pure(function.identity) << Monad(a) == Monad(a)
        self.assertAllTrue(r, "Identity")
        # Composition
        r = lambda a: Monad.pure(function.compose) << u << v << Monad(a) == u << (v << Monad(a))
        self.assertAllTrue(r, "Composition") 
        # Homomorphism
        r = lambda a: Monad(f) << Monad(a) == Monad(f(a))
        self.assertAllTrue(r, "Homomorphism")
        # Interchange
        r = lambda a: u << Monad(a) == Monad.pure(function.apply(a)) << u
        self.assertAllTrue(r, "Interchange")

    def test_monad(self):
        i = Kleisli(Monad.pure)
        m = Kleisli(lambda x: Monad(x + 1))
        k = Kleisli(lambda x: Monad(x * 2))
        h = Kleisli(lambda x: Monad(x / 2))
        # Identity
        r = lambda a: (i >> k == k)(a) and (k >> i == k)(a)
        self.assertAllTrue(r, "Identity")
        # Associative
        r = lambda a: (m >> (k >> h) == (m >> k) >> h)(a)
        self.assertAllTrue(r, "Associative")

    def test_Parser(self):
        # char
        self.assertEqual(char("+", Value(0, None, "+2")), Accept(Value(0, None, "2")))
        self.assertEqual(char("+", Value(0, None, "*2")), NotAccept(Value(0, None, "*2")))
        self.assertEqual(char("+", Value(0, None, "")), NotAccept(Value(0, None, "")))
        # digit
        self.assertEqual(digit(Value(0, None, "3+2")), Accept(Value(3, None, '+2')))
        self.assertEqual(digit(Value(0, None, "a+2")), NotAccept(Value(0, None, "a+2")))
        self.assertEqual(digit(Value(0, None, "")), NotAccept(Value(0, None, "")))
        # end
        self.assertEqual(end(Value(0, None, "")), Accept(Value(0, None, "")))
        self.assertEqual(end(Value(0, None, "3+2")), Error(Value(0, None, "3+2")))
        # eval
        self.assertEqual(eval("2+3"), Accept(Value(5, None, '')))
        self.assertEqual(eval("2*3"), Accept(Value(6, None, '')))
        self.assertEqual(eval("2+3*4"), Accept(Value(14, None, '')))
        self.assertEqual(eval("(2+3)*4"), Accept(Value(20, None, '')))
        self.assertEqual(eval("((2+3)*4/2+3+2)/2"), Accept(Value(7.5, None, '')))
        self.assertEqual(eval("2/0"), ErrorDivisionByZero(Value(2, None, '/0')))
        self.assertEqual(eval("2/(3-3)"), ErrorDivisionByZero(Value(2, None, '/(3-3)')))
        self.assertEqual(eval("2+x"), Error(Value(2, None, '+x')))
        self.assertEqual(eval("2*x"), Error(Value(2, None, '*x')))

    def assertAllTrue(self, p, msg = None):
        for a in range(-1000, 1000):
            with self.subTest(a=a):
                self.assertTrue(p(a), msg)


if __name__ == '__main__':
    unittest.main()
