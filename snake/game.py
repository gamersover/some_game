import sys
import time
import random
import pygame
from snake import Snake
from config import Config as cfg

fpsclock = pygame.time.Clock()


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.get_info()
        self.init_state()
        self.score = 0

    def get_info(self):
        self.screen_x, self.screen_y = self.screen.get_size()
        self.grid_nums = (self.screen_x // cfg.BODY_SIZE, self.screen_y // cfg.BODY_SIZE)
        self.all_position = set((x, y) for x in range(self.grid_nums[0]) for y in range(self.grid_nums[1]))

    def init_state(self):
        self.init_snake_pos = (self.grid_nums[0]//2, self.grid_nums[1]//2)
        self.init_action = "右"
        self.snake = Snake(self.init_snake_pos, self.init_action)
        self.egg = self.generate_egg()

    def init_gui(self):
        self.screen.fill(cfg.WHITE)
        pygame.draw.line(self.screen, cfg.BLACK, (0, 0), (self.screen_x, 0), 1)
        pygame.draw.line(self.screen, cfg.BLACK, (0, self.screen_y), (self.screen_x, self.screen_y), 1)
        pygame.draw.line(self.screen, cfg.BLACK, (0, 0), (0, self.screen_y), 1)
        pygame.draw.line(self.screen, cfg.BLACK, (self.screen_x, 0), (self.screen_x, self.screen_y), 1)

    def draw_egg(self):
        pygame.draw.circle(self.screen, cfg.RED,
                           (cfg.BODY_SIZE*self.egg[0]+cfg.BODY_SIZE//2, cfg.BODY_SIZE*self.egg[1]+cfg.BODY_SIZE//2),
                           cfg.BODY_SIZE//2, 0)

    def draw_snake(self):
        pygame.draw.rect(self.screen, cfg.BLUE,
                         (cfg.BODY_SIZE * self.snake.head.x, cfg.BODY_SIZE * self.snake.head.y, cfg.BODY_SIZE, cfg.BODY_SIZE),
                         1)
        for body in self.snake.bodies[1:]:
            pygame.draw.rect(self.screen, cfg.BLUE,
                             (cfg.BODY_SIZE*body.x, cfg.BODY_SIZE*body.y, cfg.BODY_SIZE, cfg.BODY_SIZE), 0)

    def generate_egg(self):
        self.remain_position = self.all_position - self.snake.get_area()
        if len(self.remain_position) == 0:
            return None
        return random.choice(list(self.remain_position))

    def step(self, action):
        self.update_action_and_move(action)
        safe = self.is_safe()
        if safe:
            self.draw_snake()
            self.draw_egg()
        else:
            time.sleep(2)
            sys.exit()

    def update_action_and_move(self, action):
        self.snake.add_action(action)
        self.is_eat_egg = (self.snake.head.x == self.egg[0]) and (self.snake.head.y == self.egg[1])
        if not self.is_eat_egg:
            self.snake.pop_action()
        else:
            self.snake.eat_egg(self.egg)
            self.egg = self.generate_egg()
            self.score += 1
            print("your score:", self.score)
        self.snake.move()

    def is_safe(self):
        return (0 <= self.snake.head.x < self.grid_nums[0]) and (0 <= self.snake.head.y < self.grid_nums[1]) and \
             self.snake.is_safe()

    def game_run(self, action):
        self.init_gui()
        self.step(action)
        fpsclock.tick(cfg.FPS)


