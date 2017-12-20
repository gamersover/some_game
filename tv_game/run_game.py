import pygame
import sys
from grid_class import Grid

SCREEN_SIZE = (400, 400)
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)


def run(game_rate):
    grid.game_start(game_rate)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                action = None
                if event.key == pygame.K_r:
                    print("push r button")
                    grid.reset_game()
                    break
                if event.key == pygame.K_q:
                    print('quit game')
                    sys.exit(0)
                if event.key == pygame.K_s:
                    game_rate = int(input("please input new game rate(1-2):"))
                    grid.reset_game(game_rate)
                    break
                if event.key == pygame.K_UP:
                    action = 'up'
                if event.key == pygame.K_DOWN:
                    action = 'down'
                if event.key == pygame.K_LEFT:
                    action = 'left'
                if event.key == pygame.K_RIGHT:
                    action = 'right'
                grid.step(action)
        grid.draw_view()
        pygame.display.update()

if __name__ == '__main__':
    print("#----------------------------------------------------------------------------------#")
    print("#game info:                                                                        #")
    print("#   red grid: source                                                               #")
    print("#   blue grid: destination                                                         #")
    print("#   black grid: barrier                                                            #")
    print("#   green grid: trap                                                               #")
    print("#----------------------------------------------------------------------------------#")
    print("                                                                                    ")
    print("#how to play:                                                                      #")
    print("# use keyboard up down left right to control red to the blue, and don't touch green#") 
    print("#                                                                                  #")
    print("# some tips                                                                        #")
    print("#   press 'r' to reset                                                             #")
    print("#   press 's' to select level                                                      #")
    print("#   press 'q' to quit                                                              #")
    print("#                                    Good luck!!                                   #")
    grid = Grid(screen)
    game_rate = 1
    run(game_rate)
        
