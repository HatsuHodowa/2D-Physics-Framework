ground = Box(screen=surface, position=Vector2(0, -20), size=Vector2(500, 10), color=(0, 50, 0), use_gravity=False)
ground.body.anchored = True

boxes = []
for i in range(10):
	box = Box(screen=surface, position=Vector2(i*10 - 50, 20), size=Vector2(5, 5), color=(255, 0, 0))
	boxes.append(box)

	box.body.add_force(Force((i % 2) * 100, 0))