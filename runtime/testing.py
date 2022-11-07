box1 = Box(screen=surface, size=Vector2(4, 2), position=Vector2(0, 10), color=(255, 0, 0))
box2 = Box(screen=surface, size=Vector2(2, 4), position=Vector2(0, -10), color=(0, 0, 255))

box1.velocity = Vector2(0, -5)

points = box1.calculate_points()

while True:
    time.sleep(0.1)
    
    #collision = box2.box_in_box(box1)