box1 = Box(screen=surface, size=Vector2(4, 4), position=Vector2(0, 5), color=(255, 0, 0))
box2 = Box(screen=surface, size=Vector2(4, 2), position=Vector2(0, -5), color=(0, 0, 255))

box1.body.add_force(Force(0, -2))