import pygame
from constants import Constants


class Camera(object):

    def __init__(self, screen, unit, pos):
        self.zoom_step = Constants.ZOOM_STEP
        self.screen_units = Constants.SCREEN_UNITS
        self.screen = screen
        self.unit = unit
        self.pos = [pos[0], pos[1]]
        self.objects_in_view = []

    def in_render_distance(self,objects):
        rd = Constants.RENDER_DISTANCE
        ar = Constants.ASPECT_RATIO
        to_render = []
        for obj in objects:
            if abs(obj.pos[0]-self.pos[0]) < rd*ar[0] and abs(obj.pos[1]-self.pos[1]) < rd*ar[1]:
                to_render.append(obj)
        return to_render

    def scale(self, objects):
        if isinstance(objects, (list, tuple)):
            for obj in objects:
                self.scale_object(obj)
        else:
            self.scale_object(objects)

    def scale_object(self, obj):
        obj.img = pygame.transform.scale(obj.def_img, (int(self.unit * obj.size[0]), int(self.unit * obj.size[1])))

    def draw(self, objects):
        if isinstance(objects, (list, tuple)):
            for obj in objects:
                self.draw_object(obj)
        else:
            self.draw_object(objects)

    def draw_object(self, obj):
        self.screen.blit(self.rot_center(obj.img, obj.angle), self.game_to_screen_pos(obj))

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def zoom(self, direction):
        h = self.screen.get_rect()[3]
        self.screen_units += direction * self.zoom_step
        self.unit = h / self.screen_units

    def mouse_collisions(self, mouse_pos, objects):
        collisions = []
        fx = mouse_pos[0]
        fy = mouse_pos[1]
        for obj in objects:
            if obj.collision:
                s_size = self.game_to_screen_size(obj)
                s_pos = self.game_to_screen_pos(obj)
                ssx = s_size[0]
                ssy = s_size[1]
                sx = s_pos[0]
                sy = s_pos[1]
                if sx + ssx > fx > sx:
                    if sy + ssy > fy > sy:
                        collisions.append(obj)
        return collisions

    def game_to_screen_size(self, obj):
        return obj.size[0] * self.unit, obj.size[1] * self.unit

    def game_to_screen_pos(self, obj):
        w = self.screen.get_rect()[2]
        h = self.screen.get_rect()[3]
        return (w / 2 - (self.pos[0] - obj.pos[0]) * self.unit - self.game_to_screen_size(obj)[0] / 2,
                h / 2 - (self.pos[1] - obj.pos[1]) * self.unit - self.game_to_screen_size(obj)[1] / 2)








