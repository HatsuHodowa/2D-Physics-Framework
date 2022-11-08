from vector2 import *
import math

class CFrame:
	def __init__(self, x=0, y=0):
		if type(x) == Vector2:
			x, y = x.x, x.y

		# creating components
		m11, m12, m13 = 1, 0, x
		m21, m22, m23 = 0, 1, y
		m31, m32, m33 = 0, 0, 1
		self.__components = [m11, m12, m13, m21, m22, m23, m31, m32, m33]

	def __str__(self):
		
		# making numbers presentable
		comps = self.__components.copy()
		max_length = 0

		for comp in comps:
			comp_str = str(round(comp*1000)/1000)
			max_length = max(len(comp_str), max_length)

		max_length += 1
		for i, comp in enumerate(comps):
			comp_str = str(round(comp*1000)/1000)
			comps[i] = comp_str + " "*(max_length - len(comp_str))

		m11, m12, m13, m21, m22, m23, m31, m32, m33 = comps

		# returning string
		tab = "  "
		return f"CF(\n{tab}{m11}{m12}{m13}\n{tab}{m21}{m22}{m23}\n{tab}{m31}{m32}{m33}\n)"

	def __add__(self, other):
		if type(other) == Vector2:
			new_cf = CFrame()
			s11, s12, s13, s21, s22, s23, s31, s32, s33 = self.components
			
			m11, m12, m13 = s11, s12, s13 + other.x
			m21, m22, m23 = s21, s22, s23 + other.y
			m31, m32, m33 = s31, s32, s33

			new_cf.__components = [m11, m12, m13, m21, m22, m23, m31, m32, m33]
			return new_cf

		else:
			print(f"{type(other)} was not a valid type for cframe add")

	def __sub__(self, other):
		if type(other) == Vector2:
			new_cf = CFrame()
			s11, s12, s13, s21, s22, s23, s31, s32, s33 = self.components
			
			m11, m12, m13 = s11, s12, s13 - other.x
			m21, m22, m23 = s21, s22, s23 - other.y
			m31, m32, m33 = s31, s32, s33

			new_cf.__components = [m11, m12, m13, m21, m22, m23, m31, m32, m33]
			return new_cf

		else:
			print(f"{type(other)} was not a valid type for cframe sub")

	def __mul__(self, other):
		if type(other) == CFrame:
			new_cf = CFrame()

			# finding components
			s11, s12, s13, s21, s22, s23, s31, s32, s33 = self.components
			o11, o12, o13, o21, o22, o23, o31, o32, o33 = other.components

			s_rows = [[s11, s12, s13], [s21, s22, s23], [s31, s32, s33]]
			o_columns = [[o11, o21, o31], [o12, o22, o32], [o13, o23, o33]]

			# multiplying
			new_comps = []
			for row in s_rows:
				for column in o_columns:
					new = 0
					for i in range(3):
						new += row[i] * column[i]

					new_comps.append(new)

			# finalizing cframe and returning
			new_cf.__components = new_comps
			return new_cf

		if type(other) == Vector2:
			m11, m12, m13, m21, m22, m23, m31, m32, m33 = self.components
			x, y = other.x, other.y

			new_x = m11 * x + m12 * y + m13
			new_y = m21 * x + m22 * y + m23

			return Vector2(new_x, new_y)

	def inverse(self):
		determinant = self.determinant
		if determinant == 0:
			return None

		# transposing
		m11, m12, m13, m21, m22, m23, m31, m32, m33 = self.components
		m11, m12, m13, m21, m22, m23, m31, m32, m33 = m11, m21, m31, m12, m22, m32, m13, m23, m33

		# finding adjoint
		rows = [[m11, m12, m13], [m21, m22, m23], [m31, m32, m33]]
		columns = [[m11, m21, m31], [m12, m22, m32], [m13, m23, m33]]

		adjoint_components = []
		for ri, row in enumerate(rows):
			for ci, comp in enumerate(row):

				# finding 2x2 determinant
				matrix = []
				for ri2, row in enumerate(rows):
					for ci2, comp in enumerate(row):
						if ri2 != ri and ci2 != ci:
							matrix.append(comp)
							
				minor = matrix[0] * matrix[3] - matrix[1] * matrix[2]
				adjoint_components.append(minor)

		# cofactor
		a11, a12, a13, a21, a22, a23, a31, a32, a33 = adjoint_components
		a11, a12, a13, a21, a22, a23, a31, a32, a33 = a11, -a12, a13, -a21, a22, -a23, a31, -a32, a33
		adjoint_components = [a11, a12, a13, a21, a22, a23, a31, a32, a33]

		# finding inverse
		inv_components = []
		for comp in adjoint_components:
			inv_components.append(comp * determinant)

		# creating inverse cframe
		inverse = CFrame()
		inverse.__components = inv_components
		return inverse

	def get_angle(self):
		if self.right_vector.y >= 0:
			return math.acos(self.right_vector.x)
		else:
			return math.pi*2 - math.acos(self.right_vector.x)

	def angle(angle):
		new_cf = CFrame()
		
		# creating components
		m11, m12, m13 = math.cos(angle), math.cos(angle + math.pi/2), new_cf.x
		m21, m22, m23 = math.sin(angle), math.sin(angle + math.pi/2), new_cf.y
		m31, m32, m33 = 0, 0, 1
		new_cf.__components = [m11, m12, m13, m21, m22, m23, m31, m32, m33]

		return new_cf

	def look_at(pos1, pos2):

		# finding angle
		direction = (pos2 - pos1).unit
		angle = None

		if direction.y >= 0:
			angle = math.acos(direction.x)
		else:
			angle = math.pi*2 - math.acos(direction.x)

		# returning cframe
		return CFrame(pos1) * CFrame.angle(angle)

	@property
	def components(self):
		m11, m12, m13, m21, m22, m23, m31, m32, m33 = self.__components
		return [m11, m12, m13, m21, m22, m23, m31, m32, m33]

	@property
	def position(self):
		m11, m12, m13, m21, m22, m23, m31, m32, m33 = self.components
		return Vector2(m13, m23)

	@property
	def right_vector(self):
		m11, m12, m13, m21, m22, m23, m31, m32, m33 = self.components
		return Vector2(m11, m21)

	@property
	def up_vector(self):
		m11, m12, m13, m21, m22, m23, m31, m32, m33 = self.components
		return Vector2(m12, m22)

	@property
	def x(self):
		return self.position.x

	@property
	def y(self):
		return self.position.y

	@property
	def determinant(self):
		m11, m12, m13, m21, m22, m23, m31, m32, m33 = self.components
		return m11 * (m22 * m33 - m23 * m32) - m12 * (m21 * m33 - m23 * m31) + m13 * (m21 * m32 - m22 * m31)

	@property
	def rotation(self):
		return self - self.position