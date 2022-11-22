import pygame
import time
import sys
import os
import threading

sys.path.append("math")
sys.path.append("graphics")
sys.path.append("objects")
sys.path.append("physics")
from cframe import *
from box import *
from camera import *
from body import *
from raycast import *

pygame.init()

# initiating screen
surface = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
pygame.display.set_caption("2D Physics Framework")

clock = pygame.time.Clock()
background_color = (150, 200, 255)

camera = Camera(screen=surface)

# runtime scripts
on_run = os.path.join(os.path.dirname(__file__), "runtime")
for file_name in os.listdir(on_run):
	f = os.path.join(on_run, file_name)
	if os.path.isfile(f):
		py = open(f, "r")
		def ex():
			exec(py.read())

		# running thread
		thread = threading.Thread(target=ex, name=file_name)
		thread.start()

# frame rendering
window_active = True
while window_active:

	# time ------------------------------------------
	t1 = time.time()
	time.sleep(0.01)#clock.tick(60)
	t2 = time.time()
	dt = (t2 - t1)

	# events ---------------------------------------
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			window_active = False
			exit()
		elif event.type == pygame.MOUSEWHEEL:
			camera.adjust_zoom(event.y)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				camera.cframe = CFrame(camera.cframe.position)

	# input --------------------------------------
	keys = pygame.key.get_pressed()

	# camera movement
	camera_dir = Vector2()
	camera_speed = 20
	if keys[pygame.K_w]:
		camera_dir += Vector2(0, 1)
	if keys[pygame.K_s]:
		camera_dir += Vector2(0, -1)
	if keys[pygame.K_a]:
		camera_dir += Vector2(-1, 0)
	if keys[pygame.K_d]:
		camera_dir += Vector2(1, 0)

	if camera_dir.magnitude != 0:
		camera_dir = camera_dir.unit
	camera.cframe *= CFrame(camera_dir*camera_speed*dt)

	# camera rotate
	rotate_speed = math.pi/4
	cam_rotate = 0
	if keys[pygame.K_q]:
		cam_rotate += rotate_speed
	if keys[pygame.K_e]:
		cam_rotate -= rotate_speed

	camera.cframe *= CFrame.angle(cam_rotate*dt)

	# physics --------------------------------------------
	for body in RigidBody.all_bodies:
		body.update(dt)
		
	# rendering ------------------------------------------
	surface.fill(background_color)

	for box in Box.all_boxes:
		box.draw(camera)

	# updating frame ----------------------------------------
	pygame.display.flip()