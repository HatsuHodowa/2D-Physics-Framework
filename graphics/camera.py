import sys

sys.path.append("math")
from cframe import *

# class
class Camera:
    def __init__(self, **kwargs):
        self.cframe = CFrame()
        self.screen = None

        self._zoom = 10
        self._zoom_min = 1
        self._zoom_max = 100

        for kw in kwargs:
            if hasattr(self, kw):
                setattr(self, kw, kwargs[kw])

    def adjust_zoom(self, magnitude):
        self._zoom = min(max(self.zoom * (1 + (magnitude/10)), self.zoom_min), self.zoom_max)

    def point_on_camera(self, point):
        if not self.screen:
            print("Camera has no screen attribute")
            return

        w, h = self.screen.get_size()
        cam_point = self.cframe.inverse() * point
        cam_point *= self.zoom
        cam_point *= Vector2(1, -1)
        cam_point += Vector2(w/2, h/2)

        return cam_point

    @property
    def zoom(self):
        return self._zoom

    @property
    def zoom_min(self):
        return self._zoom_min

    @property
    def zoom_max(self):
        return self._zoom_max