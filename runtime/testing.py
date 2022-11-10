ground = Box(screen=surface, position=Vector2(0, -10), size=Vector2(50, 10), color=(0, 255, 0))
ground.body.anchored = True

box1 = Box(screen=surface, position=Vector2(0, 5), size=Vector2(2, 2), color=(255, 0, 0))
box2 = Box(screen=surface, position=Vector2(5, 5), size=Vector2(2, 2), color=(0, 0, 255))

box1.body.add_force(Force(5, 0))