import sys
import pygame
from game_rate import get_grids


# color    R    G    B
WHITE = [255, 255, 255] 
BLACK = [  0,   0,   0]
RED   = [255,   0,   0]
BLUE  = [  0,   0, 255]
GREEN = [  0, 255,   0]

# grid num of row or col
GRID_NUM = 12
GAME_LEVEL = 2

class Grid:
    def __init__(self, screen):
        """
        Args:
            screen: game screen
            screen_size: the size of game screen
            grid_size: the size of a grid
            grid_arr: array consist of all grids
        """
        self.screen = screen
        self.screen_size = self.screen.get_size()[0]
        self.grid_size = self.screen_size // GRID_NUM
        self.grid_arr = [(i,j) for i in range(GRID_NUM) for j in range(GRID_NUM)]
        
    def game_start(self, game_rate):
        """
        Args:
            game_rate: what rate of current game
            src_grid: source grid that you have to control it
            trap_grid: trap grid that you can't over it, if you over it, the game over
            barr_grid: barrier grid that will stop you
            des_grid: destination grid that you hava to reach it
            terminal: is the game over?
            game_result: result of game   win or fail?
        """
        self.game_rate = game_rate
        print('you are rate {}'.format(self.game_rate))

        self.src_grid, self.trap_grid, self.barr_grid, self.des_grid = get_grids(self.game_rate)

        self.terminal = False
        self.game_result = None
    
    def game_over(self):
        if self.terminal:
            print(self.game_result)
            sys.exit()
        if self.game_result == 'win':
            if self.game_rate < GAME_LEVEL:
                self.game_rate += 1
                self.game_start(self.game_rate)
            else:
                print("you pass all rate of the game")
                sys.exit()
    
    def reset_game(self, game_rate=None):
        if not game_rate:
            game_rate = self.game_rate
        self.game_start(game_rate)      
            
    def draw_view(self):
        self.screen.fill(WHITE)
        
        for i in range(GRID_NUM):
            pygame.draw.line(self.screen, BLACK, (self.grid_size*(i+1),0), (self.grid_size*(i+1),self.screen_size), 1)
            pygame.draw.line(self.screen, BLACK, (0,self.grid_size*(i+1)), (self.screen_size,self.grid_size*(i+1)), 1)
        
        for grid in self.grid_arr:
            if grid in self.src_grid:
                pygame.draw.rect(self.screen, RED, (grid[0]*self.grid_size, grid[1]*self.grid_size, self.grid_size, self.grid_size), 3)
            elif grid in self.des_grid:
                pygame.draw.rect(self.screen, BLUE, (grid[0]*self.grid_size, grid[1]*self.grid_size, self.grid_size, self.grid_size), 3)
            elif grid in self.barr_grid:
                pygame.draw.rect(self.screen, BLACK, (grid[0]*self.grid_size, grid[1]*self.grid_size, self.grid_size, self.grid_size), 0)
            elif grid in self.trap_grid:
                pygame.draw.rect(self.screen, GREEN, (grid[0]*self.grid_size, grid[1]*self.grid_size, self.grid_size, self.grid_size), 0)
    
    def step(self, action):
        self.game_over()

        if action == 'up':
            self.go_up()
        elif action == 'down':
            self.go_down()
        elif action == 'left':
            self.go_left()
        elif action == 'right':
            self.go_right()

        self.src_grid = sorted(self.src_grid)
        if self.src_grid == self.des_grid:
            self.game_result = 'win'

    def go_up(self):
        sort_src_grid = sorted(self.src_grid, key=lambda x:x[1], reverse=False)

        for i in range(len(sort_src_grid)):
            new_grid = (sort_src_grid[i][0], sort_src_grid[i][1]-1)
            if new_grid in self.grid_arr:
                if new_grid in self.trap_grid:
                    self.game_result = 'failed'
                    self.terminal = True
                    sort_src_grid[i] = new_grid
                if new_grid not in self.barr_grid+sort_src_grid[:i]:
                    sort_src_grid[i] = new_grid

        self.src_grid = sort_src_grid
    
    def go_down(self):
        sort_src_grid = sorted(self.src_grid, key=lambda x:x[1], reverse=True)

        for i in range(len(sort_src_grid)):
            new_grid = (sort_src_grid[i][0], sort_src_grid[i][1]+1)
            if new_grid in self.grid_arr:
                if new_grid in self.trap_grid:
                    self.game_result = 'failed'
                    self.terminal = True
                    sort_src_grid[i] = new_grid
                if new_grid not in self.barr_grid+sort_src_grid[:i]:
                    sort_src_grid[i] = new_grid

        self.src_grid = sort_src_grid        
    
    def go_left(self):
        sort_src_grid = sorted(self.src_grid, key=lambda x:x[0], reverse=False)

        for i in range(len(sort_src_grid)):
            new_grid = (sort_src_grid[i][0]-1, sort_src_grid[i][1])
            if new_grid in self.grid_arr:
                if new_grid in self.trap_grid:
                    self.game_result = 'failed'
                    self.terminal = True
                    sort_src_grid[i] = new_grid
                if new_grid not in self.barr_grid+sort_src_grid[:i]:
                    sort_src_grid[i] = new_grid

        self.src_grid = sort_src_grid
    
    def go_right(self):
        sort_src_grid = sorted(self.src_grid, key=lambda x:x[0], reverse=True)

        for i in range(len(sort_src_grid)):
            new_grid = (sort_src_grid[i][0]+1, sort_src_grid[i][1])
            if new_grid in self.grid_arr:
                if new_grid in self.trap_grid:
                    self.game_result = 'failed'
                    self.terminal = True
                    sort_src_grid[i] = new_grid
                if new_grid not in self.barr_grid+sort_src_grid[:i]:
                    sort_src_grid[i] = new_grid
                    
        self.src_grid = sort_src_grid
