import math

class Vector2:
	def __init__(self, x=0, y=0):
		self.__x = x
		self.__y = y

	def __str__(self):
		round_to = 100
		return f"V2({round(self.x*round_to)/round_to}, {round(self.y*round_to)/round_to})"

	def __add__(self, other):
		if type(other) == Vector2:
			return Vector2(self.x + other.x, self.y + other.y)
		else:
			print(f"{type(other)} was not a valid type for vector addition")

	def __sub__(self, other):
		if type(other) == Vector2:
			return Vector2(self.x - other.x, self.y - other.y)
		else:
			print(f"{type(other)} was not a valid type for vector subtraction")

	def __mul__(self, other):
		if type(other) == Vector2:
			return Vector2(self.x * other.x, self.y * other.y)
		elif type(other) == float or type(other) == int:
			return Vector2(self.x * other, self.y * other)
		else:
			print(f"{type(other)} was not a valid type for vector multiplication")

	def __truediv__(self, other):
		if type(other) == Vector2:
			return Vector2(self.x / other.x, self.y / other.y)
		elif type(other) == int or type(other) == float:
			return Vector2(self.x / other, self.y / other)
		else:
			print(f"{type(other)} was not a valid type for vector division")

	def __neg__(self):
		return Vector2(-self.x, -self.y)

	def __eq__(self, other):
		if type(other) != Vector2:
			return False

		return self.x == other.x and self.y == other.y

	@property
	def magnitude(self):
		return math.sqrt(self.x**2 + self.y**2)

	@property
	def unit(self):
		if self.magnitude != 0:
			return self / self.magnitude
		else:
			return None

	@property
	def x(self):
		return self.__x

	@property
	def y(self):
		return self.__y

	def dot(self, other):
		if type(other) == Vector2:
			return self.x * other.x + self.y * other.y
		else:
			print(f"{type(other)} was not a valid type for vector dot")