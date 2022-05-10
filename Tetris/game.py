import sys
import time
import copy
import random
import pygame
from shape import *
from config import Config as cfg
from collections import Counter

shapes = [LZtype, RZtype, Rect, LLtype, RLtype, Itype, Ttype]
fpsclock = pygame.time.Clock()


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.gene_flag = True
        self.game_shape = []
        self.score = 0
        self.count = 0
        self.init_fall_speed = cfg.FPS
        self.next_shape = self.random_gene_shape()
        self.update_next_shape()
        self.update_fall_speed()
        self.font = pygame.font.SysFont("SimHei", 15)
        self.next_font_fmt = self.font.render("下一个:", 1, cfg.BLACK)
        self.score_font_fmt = self.font.render("得分:", 1, cfg.BLACK)
        self.score_num_fmt = self.font.render(str(self.score), 1, cfg.BLACK)

    def show_gui(self):
        self.screen.fill(cfg.WHITE)
        pygame.draw.line(self.screen, cfg.BLACK, (0, 0), (0, cfg.SCREEN_Y), 1)
        pygame.draw.line(self.screen, cfg.BLACK, (cfg.SCREEN_X, 0), (cfg.SCREEN_X, cfg.SCREEN_Y), 1)
        pygame.draw.line(self.screen, cfg.BLACK, (0, cfg.SCREEN_Y), (cfg.SCREEN_X, cfg.SCREEN_Y), 1)
        pygame.draw.line(self.screen, cfg.BLACK, (cfg.SCREEN_X+cfg.INFO_X, 0), (cfg.SCREEN_X+cfg.INFO_X, cfg.SCREEN_Y))

    def draw_shape(self):
        color = self.curr_shape.color
        for grid in self.curr_shape.area:
            pygame.draw.circle(self.screen, color,
                               (grid[0]*cfg.GRID_SIZE+cfg.GRID_SIZE//2, grid[1]*cfg.GRID_SIZE+cfg.GRID_SIZE//2),
                               cfg.GRID_SIZE//2, 0)

        color = self.next_shape.color
        for grid in self.next_shape.area:
            pygame.draw.circle(self.screen, color,
                               (grid[0] * cfg.GRID_SIZE + cfg.GRID_SIZE // 2,
                                grid[1] * cfg.GRID_SIZE + cfg.GRID_SIZE // 2),
                               cfg.GRID_SIZE // 2, 0)

        for grid in self.game_shape:
            pygame.draw.circle(self.screen, cfg.BLACK,
                               (grid[0] * cfg.GRID_SIZE + cfg.GRID_SIZE // 2,
                                grid[1] * cfg.GRID_SIZE + cfg.GRID_SIZE // 2),
                               cfg.GRID_SIZE // 2, 0)

    def draw_text(self):
        self.screen.blit(self.next_font_fmt, (cfg.SCREEN_X+cfg.GRID_SIZE//2, 10))
        self.screen.blit(self.score_font_fmt, (cfg.SCREEN_X+cfg.GRID_SIZE//2, 150))
        self.screen.blit(self.score_num_fmt, (cfg.SCREEN_X+cfg.INFO_X//2, 170))

    def random_gene_shape(self):
        shape_no = random.randint(0, len(shapes)-1)
        shape_type = random.randint(0, 3)
        color = random.choice([cfg.RED, cfg.BLUE, cfg.GREEN])
        return shapes[shape_no]((cfg.SCREEN_X + cfg.INFO_X//2)//cfg.GRID_SIZE, 2, color, shape_type)

    def update_next_shape(self):
        self.curr_shape = self.next_shape
        self.curr_shape.x_center = (cfg.SCREEN_X//2)//cfg.GRID_SIZE - 1
        self.curr_shape.reset_area()
        self.next_shape = self.random_gene_shape()

    def move(self, action):
        if action == "左":
            self.curr_shape.move_left()
        elif action == "右":
            self.curr_shape.move_right()
        elif action == "上":
            self.curr_shape.rotate()
        elif action == "下":
            self.curr_shape.move_down()

    def add_new_shape(self, shape):
        for area in shape.area:
            self.game_shape.append(area)

    def can_move_part(self, shape_before_step, direction):
        self.move(direction)
        flag = not self.should_stop()
        self.curr_shape = copy.deepcopy(shape_before_step)
        return flag

    def can_move(self, shape_before_step):
        can_move_directions = ["无"]
        if self.can_move_part(shape_before_step, "上"):
            can_move_directions.append("上")
        if self.can_move_part(shape_before_step, "下"):
            can_move_directions.append("下")
        if self.can_move_part(shape_before_step, "左"):
            can_move_directions.append("左")
        if self.can_move_part(shape_before_step,"右"):
            can_move_directions.append("右")
        return can_move_directions

    def check_score(self):
        d = Counter([p[1] for p in self.game_shape]).most_common()
        self.remove_y = sorted([k for k, v in d if v == cfg.SCREEN_X // cfg.GRID_SIZE])
        n_remove = len(self.remove_y)
        if n_remove > 0:
            self.score += pow(2, n_remove-1)
        self.score_num_fmt = self.font.render(str(self.score), 1, cfg.BLACK)
        self.update_fall_speed()
        return n_remove > 0

    def update_fall_speed(self):
        self.fall_speed = max(cfg.MAX_SPEED,
                              int(self.init_fall_speed * pow(cfg.FALL_SPEED_RATE, self.score // cfg.FALL_SPEED_SCORE)))

    def update_game_shape(self):
        new_game_shape = []
        for area in self.game_shape:
            if area[1] not in self.remove_y:
                n = sum(y > area[1] for y in self.remove_y)
                new_game_shape.append((area[0], area[1] + n))
        self.game_shape = new_game_shape

    def game_over(self):
        return any([area in self.game_shape for area in self.curr_shape.area])

    def should_stop(self):
        lx = self.curr_shape.get_left_x()
        rx = self.curr_shape.get_right_x()
        dy = self.curr_shape.get_down_y()
        collision = any([a in self.game_shape for a in self.curr_shape.area])
        return lx < 0 or rx * cfg.GRID_SIZE >= cfg.SCREEN_X or dy * cfg.GRID_SIZE >= cfg.SCREEN_Y or collision

    def draw_game(self):
        self.show_gui()
        self.draw_shape()
        self.draw_text()

    def store_shape(self):
        return copy.deepcopy(self.curr_shape)

    def step(self, action):
        # 显示图形
        self.draw_game()
        # 暂时存储移动前的方块
        shape_before_step = self.store_shape()
        # 是否可以移动，如果可以就移动，如果不行，不移动
        can_move_directions = self.can_move(shape_before_step)
        if action in can_move_directions or "下" in can_move_directions:
            if action in can_move_directions:
                self.move(action)
        else:
            # 更新游戏的形状
            self.add_new_shape(shape_before_step)
            # 判断消除的行并更新游戏形状
            while self.check_score():
                self.update_game_shape()
            # 生成新的方块
            self.update_next_shape()
            # 判断是否结束游戏
            if self.game_over():
                time.sleep(2)
                sys.exit()
        fpsclock.tick(cfg.FPS)

    def game_run(self, action):
        self.count += 1
        if self.count >= self.fall_speed:
            self.step("下")
            self.count = 0
        self.step(action)



