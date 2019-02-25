import sys
import pygame
from config import Config as cfg
from game import Game


def start(g):
    action = "右"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    action = "上"
                if event.key == pygame.K_s:
                    action = "下"
                if event.key == pygame.K_a:
                    action = "左"
                if event.key == pygame.K_d:
                    action = "右"

        g.game_run(action)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREEN_SIZE, 0, 32)
    g = Game(screen)
    start(g)

