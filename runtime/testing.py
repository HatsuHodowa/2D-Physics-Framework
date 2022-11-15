ground = Box(screen=surface, position=Vector2(0, -20), size=Vector2(50, 10), color=(0, 255, 0))
ground.body.anchored = True

boxes = []

for x in range(0, 20, 7):
    for y in range(5, 10, 5):
        box = Box(screen=surface, position=Vector2(x, y), size=Vector2(1, 1), color=(255, 0, 0))
        boxes.append(box)