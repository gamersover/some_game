import sys
import pygame
from game import Game
from config import Config as cfg


pygame.init()
screen = pygame.display.set_mode(cfg.SCREEN_SIZE, 0, 32)


def run(g):
    action = "无"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    action = "上"
                if event.key == pygame.K_LEFT:
                    action = "左"
                if event.key == pygame.K_RIGHT:
                    action = "右"
                if event.key == pygame.K_DOWN:
                    action = "k_下"
                if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    action = "无" if action == "pause" else "pause"

        if action != "pause":
            g.game_run(action)
            action = "无"

        pygame.display.update()


if __name__ == '__main__':
    g = Game(screen)
    run(g)