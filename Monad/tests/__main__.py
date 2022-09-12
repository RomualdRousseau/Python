import unittest
from monad import *
from main import *

f = lambda x: x * 2
g = lambda x: x + 2
u = Monad(f)
v = Monad(g)

class TestMonadMethods(unittest.TestCase):

    def test_allTrue(self):
        self.assertAllTrue(lambda a: a == a, "All are true")

    def test_compose(self):
        r = lambda a: function.compose(f)(g)(a) == f(g(a))
        self.assertAllTrue(r)

    def test_curry(self):
        r = lambda x, y: x + y
        self.assertEqual(add(2, 3), 5)
        r = function.curry(r)
        self.assertEqual(r(2)(3), add(2, 3))

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
        self.assertEqual(char("+", (0, "+2")), Accept((0, '2')))
        self.assertEqual(char("+", (0, "*2")), Error((0, '*2')))
        self.assertEqual(char("+", (0, "")), Error((0, '')))
        # digit
        self.assertEqual(digit((0, "3+2")), Accept((3, '+2')))
        self.assertEqual(digit((0, "a+2")), Error((0, 'a+2')))
        self.assertEqual(digit((0, "")), Error((0, '')))
        # end
        self.assertEqual(end((0, "")), Accept((0, '')))
        self.assertEqual(end((0, "3+2")), Error((0, '3+2')))
        # eval
        self.assertEqual(eval("2+3"), Accept((5, '')))
        self.assertEqual(eval("2*3"), Accept((6, '')))
        self.assertEqual(eval("2+3*4"), Accept((14, '')))
        self.assertEqual(eval("(2+3)*4"), Accept((20, '')))
        self.assertEqual(eval("((2+3)*4/2+3+2)/2"), Accept((7.5, '')))
        self.assertEqual(eval("2/0"), Error((2, '/0')))
        self.assertEqual(eval("2/(3-3)"), Error((2, '/(3-3)')))
        self.assertEqual(eval("2+x"), Error((2, '+x')))
        self.assertEqual(eval("2*x"), Error((2, '*x')))

    def assertAllTrue(self, p, msg = None):
        for a in range(-1000, 1000):
            with self.subTest(a=a):
                self.assertTrue(p(a), msg)


if __name__ == '__main__':
    unittest.main()
