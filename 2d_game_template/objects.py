import math

class Obj(object):

    def __init__(self, pos, size, img):
        self.pos = [pos[0], pos[1]]
        self.size = [size[0], size[1]]
        self.def_img = img
        self.img = img
        self.collision = False
        self.movable = True
        self.angle = 0

    def is_colliding_with(self, objects):
        collisions = []
        fsx = self.size[0]
        fsy = self.size[1]
        fx = self.pos[0] - fsx / 2
        fy = self.pos[1] - fsy / 2
        for obj in objects:
            if obj != self:
                if obj.collision:
                    ssx = obj.size[0]
                    ssy = obj.size[1]
                    sx = obj.pos[0] - ssx / 2
                    sy = obj.pos[1] - ssy / 2
                    if sx + ssx > fx > sx or sx + ssx > fx + fsx > sx or fx + fsx > sx > fx or fx + fsx > sx + ssx > fx:
                        if sy + ssy > fy > sy or sy + ssy > fy + fsy > sy or fy + fsy > sy > fy or fy + fsy > sy + ssy > fy:
                            collisions.append(obj)
        return collisions

    def collision_detection(self, game_objects,tick):
        pass

class Dummy(Obj):

    def __init__(self, pos, size, img):
        Obj.__init__(self, pos, size, img)
        self.pos = [pos[0], pos[1]]
        self.size = [size[0], size[1]]
        self.img = img
        self.collision = True

    def collision_detection(self, game_objects,tick):
        collisions = self.is_colliding_with(game_objects)
        if collisions:
            for obj in collisions:
                self.relative_move(obj.pos, tick)


class Bullet(Obj):

    def __init__(self, pos, size, img):
        Obj.__init__(self, pos, size, img)
        self.pos = [pos[0], pos[1]]
        self.size = [size[0], size[1]]
        self.img = img
        self.collision = True
        self.speed = 10

class Character(Obj):

    def __init__(self, pos, size, speed, img):
        Obj.__init__(self, pos, size, img)
        self.alive = True
        self.speed = speed
        self.direction = [0, 0]
        self.collision = True

    def update(self, tick, objects_to_render, mouse_pos, pos_on_screen):
        self.move(tick)
        self.collision_detection(tick, objects_to_render)
        self.angle = 360 - math.atan2(mouse_pos[1] - pos_on_screen[1], mouse_pos[0] - pos_on_screen[0]) * 180 / math.pi

    def move(self, tick, direc=None):
        if direc is None:
            direc = self.direction
        self.pos[0] += direc[0] * self.speed * tick / 1000
        self.pos[1] += direc[1] * self.speed * tick / 1000

    def key_press(self, key):
        if self.movable:
            if key == 0: self.direction[1] -= 1
            if key == 1: self.direction[0] -= 1
            if key == 2: self.direction[1] += 1
            if key == 3: self.direction[0] += 1

    def key_release(self,key):
        if self.movable:
            if key == 0: self.direction[1] += 1
            if key == 1: self.direction[0] += 1
            if key == 2: self.direction[1] -= 1
            if key == 3: self.direction[0] -= 1

    def relative_move(self, dest, tick):
        direction = self.relative_direction(dest, -1)
        self.move(tick, direction)

    def relative_direction(self, dest, speed):
        dx = dest[0] - self.pos[0]
        dy = dest[1] - self.pos[1]
        if abs(dx) > abs(dy):
            if dx > 0: return [+speed, 0]
            else: return [-speed, 0]
        else:
            if dy > 0: return [0, +speed]
            else: return [0, -speed]

    def collision_detection(self, tick, objects_to_render):
        collisions = self.is_colliding_with(objects_to_render)
        if collisions:
            for obj in collisions:
                self.relative_move(obj.pos,tick)