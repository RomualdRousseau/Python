import math

class Variable:

	def __init__(self, v_):
		self.value = v_
		self.prime = 1

	def __neg__(self):
		self.prime *= -1.0
		self.value *= -1.0
		return self

	def __add__(self, a):
		self.prime += a.prime
		self.value += a.value
		return self
		
	def __sub__(self, a):
		self.prime -= a.prime
		self.value -= a.value
		return self
		
	def __mul__(self, a):
		self.prime = a.value * self.prime
		self.value = a.value * self.value
		return self
		
	def __pow__(self, a):
		self.prime = a * (self.value ** (a - 1)) * self.prime
		self.value = self.value ** a
		return self

	def exp(self):
		self.prime = math.exp(self.value) * self.prime
		self.value = math.exp(self.value)
		return self

	def get_value(self):
		return self.value

	def get_prime(self):
		return self.prime
		
class Constant(Variable):
	def __init__(self, v_):
		self.value = v_
		self.prime = 0

	def __mul__(self, a):
		self.prime = self.value * a.prime
		self.value = self.value * a.value
		return self

def exp(v):
	v.prime = math.exp(v.value) * v.prime
	v.value = math.exp(v.value)
	return v

def log(v):
	v.prime = v.prime / v.value
	v.value = math.log(v.value)
	return v

cost = lambda y, yhat: -Constant(0.5) * ((Constant(y) - Variable(yhat)) ** 2)
print(cost(1, 0.5).get_value())
print(cost(1, 0.5).get_prime())

sigmoid = lambda x: (Constant(1) + exp(-Variable(x))) ** -1
print(sigmoid(0.5).get_value())
print(sigmoid(0.5).get_prime())

test = lambda y, yhat: -Constant(y) * log(sigmoid(yhat))
print(test(1, 0.5).get_value())
print(test(1, 0.5).get_prime())
