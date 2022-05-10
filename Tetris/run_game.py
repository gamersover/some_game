import sys
import pygame
from game import Game
from config import Config as cfg


pygame.init()
screen = pygame.display.set_mode(cfg.SCREEN_SIZE, 0, 32)


# TODO: 长按的速度慢一点

def run(g):
    action = "无"
    is_down = False
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
                    print("按键按下", action)
                    action = "下"
                    is_down = True
                if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    action = "无" if action == "pause" else "pause"
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    print("按键提起", action)
                    action = "无"
                    is_down = False

        if action != "pause":
            # print(action)
            g.game_run(action)
            if not is_down:
                action = "无"

        pygame.display.update()


if __name__ == '__main__':
    g = Game(screen)
    run(g)