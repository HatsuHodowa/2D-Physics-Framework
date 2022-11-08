import sys
import pygame
pygame.init()

sys.path.append("math")
sys.path.append("physics")
from cframe import *
from body import *

# class
class Box:
	all_boxes = []
	next_id = 0
	def __init__(self, **kwargs):
		self.size = Vector2(5, 5)
		self.position = Vector2()
		self.velocity = Vector2()

		self.color = (150, 150, 150)
		self.bd_width = 0

		self.id = Box.next_id
		Box.next_id += 1

		self.density = 0.1
		self.body = RigidBody(self)

		# keyword arguments
		self.screen = None
		for kw in kwargs:
			if hasattr(self, kw):
				setattr(self, kw, kwargs[kw])

		# inserting
		Box.all_boxes.append(self)
				
	def __eq__(self, other):
		if type(other) != Box:
			return False

		return self.id == other.id

	def calculate_points(self):
		points = []
		for x in [-1, 1]:
			for y in [-1, 1]:
				v2 = self.position + self.size/2 * Vector2(x, y)
				points.append(v2)

		points[2], points[3] = points[3], points[2]
		return points

	def point_in_box(self, check_point):

		# finding boundaries
		points = self.calculate_points()
		max_x, min_x = None, None
		max_y, min_y = None, None

		for i, point in enumerate(points):
			if i != 0:
				max_x = max(point.x, max_x)
				min_x = min(point.x, min_x)
				max_y = max(point.y, max_y)
				min_y = min(point.y, min_y)
			else:
				max_x = point.x
				min_x = point.x
				max_y = point.y
				min_y = point.y

		# checking boundaries
		x_bool = check_point.x < max_x and check_point.x > min_x
		y_bool = check_point.y < max_y and check_point.y > min_y
		
		return x_bool and y_bool

	def box_collision(self, other):

		# defining bounds & checking collision
		s_bottom, s_top = self.position.y - self.size.y/2, self.position.y + self.size.y/2
		s_left, s_right = self.position.x - self.size.x/2, self.position.x + self.size.x/2

		o_bottom, o_top = other.position.y - other.size.y/2, other.position.y + other.size.y/2
		o_left, o_right = other.position.x - other.size.x/2, other.position.x + other.size.x/2

		xbool = s_left <= o_right and s_right >= o_left
		ybool = s_top >= o_bottom and s_bottom <= o_top

		# checking colliding normal
		axis = None

		if xbool and ybool:
			x_dist = min(abs(s_left - o_right), abs(o_left - s_right))
			y_dist = min(abs(s_bottom - o_top), abs(o_bottom - s_top))
			min_dist = min(x_dist, y_dist)

			if min_dist == x_dist:
				axis = Vector2(1, 0)
			else:
				axis = Vector2(0, 1)

		return xbool and ybool, axis

	@property
	def check_collision(self):
		return self.box_collision

	def draw(self, camera):
		if not self.screen:
			return

		w, h = self.screen.get_size()
		points = self.calculate_points()
		
		cam_points = []
		for v2 in points:
			cam_v2 = camera.point_on_camera(v2)
			cam_points.append((cam_v2.x, cam_v2.y))

		pygame.draw.polygon(self.screen, self.color, cam_points, self.bd_width)

	@property
	def area(self):
		return self.size.x * self.size.y

	@property
	def mass(self):
		return self.area * self.density