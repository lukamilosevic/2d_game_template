import pygame
from game import Game
from constants import Constants

class Main:


    def __init__(self):
        pygame.init()
        pygame.display.init()

        pygame.display.set_caption(Constants.CAPTION)

        self.w = int(Constants.DEF_WIN_SIZE * Constants.ASPECT_RATIO[0])
        self.h = int(Constants.DEF_WIN_SIZE * Constants.ASPECT_RATIO[1])
        self.screen_size = (self.w, self.h)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.unit = self.h / Constants.SCREEN_UNITS

        # fullscreen
        # self.w = pygame.display.Info().current_w
        # self.h = pygame.display.Info().current_h
        # self.screen_size = (self.w, self.h)
        # self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        # self.unit = self.h / Constants.SCREEN_UNITS

    def main(self):
        self.play_game()

    def play_game(self):
        gm = Game(self.screen, self.unit)
        gm.main()
        return gm.running

def main():
    game = Main()
    game.main()
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()