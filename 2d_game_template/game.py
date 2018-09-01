import pygame
from constants import Constants
from objects import Character, Dummy, Bullet
from camera import Camera
import math


class Game:

    def __init__(self, screen, unit):
        self.screen = screen
        self.unit = unit
        self.running = True

        self.time = pygame.time.Clock()
        self.ticks = 0
        self.gameloop = True
        self.game_objects = []

    def main(self):
        #generating game objects
        def_img = pygame.image.load('char.png')

        character = Character([500, 500], [10, 10], 20, def_img)
        self.game_objects.append(character)
        dummy = Dummy([480, 480], [8, 8], def_img)
        dummy1 = Dummy([460, 500], [8, 8], def_img)
        self.game_objects.append(dummy)
        self.game_objects.append(dummy1)

        camera = Camera(self.screen, self.unit, character.pos)

        camera.scale(self.game_objects)     #scale all game objects

        #game loop
        while self.running:
            camera.pos = character.pos
            tick = self.time.tick(Constants.FPS)
            self.screen.fill(Constants.WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 or event.button == 6:
                        bullet = Bullet(character.pos, [1, 1], def_img)
                        self.game_objects.append(bullet)
                        camera.scale(bullet)
                    if event.button == 4:
                        camera.zoom(-1)
                        camera.scale(self.game_objects)
                    elif event.button == 5:
                        camera.zoom(+1)
                        camera.scale(self.game_objects)
                elif event.type == pygame.KEYDOWN:
                    key = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_w: key = 0
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a: key = 1
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s: key = 2
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d: key = 3
                    character.key_press(key)
                elif event.type == pygame.KEYUP:
                    key = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_w: key = 0
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a: key = 1
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s: key = 2
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d: key = 3
                    character.key_release(key)

            objects_to_render = camera.in_render_distance(self.game_objects)
            character.update(tick, objects_to_render, pygame.mouse.get_pos(), camera.game_to_screen_pos(character))

            camera.draw(objects_to_render)
            pygame.display.update()