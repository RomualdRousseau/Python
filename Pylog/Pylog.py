universe = []

class Fact:
	Empty = None

	def __init__(self, name):
		global universe
	
		self.name = name	
		universe = universe + [self]

		if Fact.Empty is None:
			Fact.Empty = EmptyFact()

	def param(self, i):
		return self

	def func(self):
		return lambda x: self == x

	def is_axiom(self):		
		return not(self.is_empty() or self.is_predicate() or self.is_clause())

	def is_empty(self):		
		return isinstance(self, EmptyFact)

	def is_predicate(self):		
		return isinstance(self, Predicate)

	def is_clause(self):		
		return isinstance(self, Clause)

	def derive(self, p = lambda X: X[0], rec = 1):
		if isinstance(p, Fact):
			return self.__solve(p)
		else:
			return self.__query(p, rec)

	def __and__(self, a):
		return BinaryPredicate.reduce(self, a, lambda x, y: AndPredicate(x, y))

	def __or__(self, a):
		return BinaryPredicate.reduce(self, a, lambda x, y: OrPredicate(x, y))

	def __invert__(self):
		return NotPredicate(self)

	def __repr__(self):
		return self.name

	def __solve(self, a):
		return bool(self.func()(a))

	def __query(self, p, rec = 1, args = []):
		result = Fact.Empty		
		if(rec <= 1):
			for a in universe:
				if self.__solve(p([a] + args)):
					result = result & a
		else:
			for a in universe:
				result = result & self.__query(p, rec - 1, [a] + args)

		return result;

class Predicate(Fact):
	pass

class Clause(Fact):
	def __init__(self, body):
		self.body = body

	def param(self, i):
		return Fact.Empty

	def func(self):
		return self.body

class EmptyFact(Fact):
	def __init__(self):
		self.name = 'empty'

	def param(self, i):
		return self

	def func(self):
		return lambda x: False

	def __and__(self, a):
		return a

	def __or__(self, a):
		return a

	def __invert__(self):
		return self

class BinaryPredicate(Predicate):
	def __init__(self, a, b, name):
		self.name = a.name + ' ' + name + ' ' + b.name 
		self.facts = (a, b)

	def param(self, i):
		return self.facts[i] if i <= 2 else Fact.Empty

	def reduce(a, b, predicate):
		return predicate(a, b) if a is not b and b is not Fact.Empty else b if b is not Fact.Empty else a

class AndPredicate(BinaryPredicate):
	def __init__(self, a, b):
		super().__init__(a, b, 'and')

	def func(self):
		a = self.facts[0].func()
		b = self.facts[1].func() 
		return lambda x: a(x.param(0)) and b(x.param(1))

class OrPredicate(BinaryPredicate):
	def __init__(self, a, b):
		super().__init__(a, b, 'or')

	def func(self):
		a = self.facts[0].func()
		b = self.facts[1].func() 
		return lambda x: a(x) or b(x)

class UnaryPredicate(Predicate):
	def __init__(self, a, name):
		self.name = name + ' ' + a.name 
		self.fact = a

	def param(self, i):
		return self.fact

class NotPredicate(UnaryPredicate):
	def __init__(self, a):
		super().__init__(a, 'not')

	def func(self):
		a = self.fact.func()
		return lambda x: not a(x)

mary = Fact('mary')
john = Fact('john')
peter = Fact('peter')

scissors = Fact('scissors')
rock = Fact('rock')
paper = Fact('paper')

bird = mary | john | peter
wounded = ~mary
abnormal = Clause(lambda x: wounded.derive(x))
canfly = Clause(lambda x: bird.derive(x) & ~abnormal.derive(x))

married = mary | john

plays = john & paper | mary & scissors | peter & paper
beats = paper & rock | rock & scissors | scissors & paper
played_by = lambda a: plays.derive(lambda X: a & X[0])
wins = Clause(lambda A: beats.derive(played_by(A[0]) & played_by(A[1])))
possible_winners = wins.derive(lambda X: tuple(X), 2)
winner = Clause(lambda x: possible_winners.derive(x) & possible_winners.is_axiom())

happy = Clause(lambda x: married.derive(x) & canfly.derive(x) & winner.derive(x))

print(canfly.derive(), 'can fly.')

print(married.derive(), 'are married.')

print(winner.derive(), 'is the winner.')

print(happy.derive(), 'is happy.')

