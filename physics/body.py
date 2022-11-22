import sys
import time
import threading
from xmlrpc.client import MAXINT

sys.path.append("math")
from cframe import *

# force
class Force:
	all_forces = []
	next_id = 0

	def __init__(self, x=0, y=5, one_frame=False):
		if type(x) == Vector2:
			x, y = x.x, x.y

		self.force = Vector2(x, y)
		self.one_frame = one_frame
		self.id = Force.next_id
		Force.next_id += 1

		Force.all_forces.append(self)

	def __eq__(self, other):
		if type(other) != Force:
			return False

		return self.id == other.id

# rigid body
class RigidBody:
	all_bodies = []
	next_id = 0

	def __init__(self, obj, use_gravity=True):
		self._forces = []
		self.obj = obj
		self.id = RigidBody.next_id
		RigidBody.next_id += 1

		self.anchored = False
		self.gravity = Force()
		self.use_gravity = use_gravity

		RigidBody.all_bodies.append(self)

	def __eq__(self, other):
		if type(other) != RigidBody:
			return False

		return self.id == other.id

	def destroy(self):
		RigidBody.all_bodies.remove(self)

	def update(self, dt):
		self.clear_temp_forces()
		
		# adding gravity
		if self.use_gravity and not self.anchored:
			self.gravity = Force(0, -9.8 * self.mass)
			self.add_force(self.gravity, True)
		else:
			self.gravity = Force()

		# calculating velocity and position
		self.calculate_normal_forces()
		acceleration = self.net_force / self.mass
		self.obj.velocity += acceleration * dt

		# moving body
		self.obj.position += self.obj.velocity * dt

	def calculate_normal_forces(self):
		objects = RigidBody.all_bodies.copy()
		for other in objects:
			if other.obj == self.obj:
				continue

			# checking collision
			collides, coll_size, normal = self.obj.check_collision(other.obj)
			if collides and self.anchored == False:

				# colliding / normal force
				s_vel = self.obj.velocity
				o_vel = other.obj.velocity

				# velocity
				final_velocity = (s_vel * self.mass + o_vel * other.obj.mass) / (self.mass + other.obj.mass)
				self.obj.velocity = final_velocity
				other.obj.velocity = final_velocity

				# pushing out
				if s_vel.unit:
					s_dot = self.obj.position.dot(normal)
					o_dot = other.obj.position.dot(normal)

					# finding distance
					dist = 0
					if normal == Vector2(1, 0):
						dist = coll_size.x
					elif normal == Vector2(0, 1):
						dist = coll_size.y

					if s_dot >= o_dot:
						self.obj.position += normal*dist
					else:
						self.obj.position -= normal*dist

	def remove_force(self, force):
		self._forces.remove(force)

	def add_force(self, force, last=None):
		self._forces.append(force)

		if last:
			def delay_remove():
				time.sleep(last)
				self.remove_force(force)

			thread = threading.Thread(target=delay_remove)
			thread.start()

	def clear_temp_forces(self):
		for force in self.forces:
			if force.one_frame:
				self.remove_force(force)

	@property
	def mass(self):
		return self.obj.mass

	@property
	def forces(self):
		return self._forces.copy()

	@property
	def net_force(self):
		final_force = Vector2()
		for force in self.forces:
			final_force += force.force

		return final_force