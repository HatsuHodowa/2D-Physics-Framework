import sys

sys.path.append("math")
from cframe import *
from body import *

class Raycast:
	def __init__(self, screen, start, direction, filter_list=[], filter_type="Blacklist"):
		self.surface = screen
		self.start = start
		self.end = self.start + direction
		
		self.intersections = []
		self.first_intersection = None
		self.normal = None

		# looping bodies
		for body in RigidBody.all_bodies:
			obj = body.obj
			if (filter_type == "Blacklist" and not obj in filter_list) or (filter_type == "Whitelist" and obj in filter_list):

				# looping edges
				points = obj.calculate_points()
				for i, point2 in enumerate(points):
					point1 = points[i - 1]
					
					# finding all variables
					x1, y1, x2, y2 = self.start.x, self.start.y, self.end.x, self.end.y
					x3, y3, x4, y4 = point1.x, point1.y, point2.x, point2.y

					# finding variables
					d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
					if d == 0:
						continue

					u = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
					t = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / d

					# collision detected
					if u <= 1 and u >= 0 and t <= 1 and t >= 0:
						self.intersections.append(Vector2(x1 + u * (x2 - x1), y3 + t * (y4 - y3)))

						if not self.first_intersection or (self.start - self.first_intersection).magnitude > (self.intersections[-1] - self.start).magnitude:
							self.first_intersection = self.intersections[-1]
							
							# calculating edge normal
							edge_dir = (point2 - point1).unit
							self.normal = Vector2(edge_dir.y, -edge_dir.x)