import sys
import math
from telnetlib import theNULL
import time
import threading

sys.path.append("math")
from cframe import *

# force
class Force:
    all_forces = []
    next_id = 0

    def __init__(self, x=0, y=5):
        self.force = Vector2(x, y)
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

    def __init__(self, obj):
        self._forces = []
        self.obj = obj
        self.id = RigidBody.next_id
        RigidBody.next_id += 1

        RigidBody.all_bodies.append(self)

    def __eq__(self, other):
        if type(other) != RigidBody:
            return False

        return self.id == other.id

    def update(self, dt):
        self.calculate_normal_forces()

        acceleration = self.net_force / self.obj.mass
        self.obj.velocity += acceleration * dt
        self.obj.position += self.obj.velocity * dt

    def calculate_normal_forces(self):
        objects = RigidBody.all_bodies.copy()
        for other in objects:
            if other == self.obj:
                continue

            # checking collision
            points = self.obj.calculate_points()
            o_points = other.obj.calculate_points()

            is_colliding = False
            for point in points:
                if other.obj.point_in_box(point):
                    is_colliding = True
                    break

            if not is_colliding:
                for o_point in o_points:
                    if self.obj.point_in_box(point):
                        is_colliding = True
                        break

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

    @property
    def forces(self):
        return self._forces.copy()

    @property
    def net_force(self):
        final_force = Vector2()
        for force in self.forces:
            final_force += force.force

        return final_force