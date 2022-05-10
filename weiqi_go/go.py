import sys
import math
from copy import deepcopy
import pygame
import pygame.gfxdraw

BLACK = (0, 0, 0)
YELLOW = (255, 239, 213)
WHITE = (255, 255, 255)
NUM_LINES = 19
LINE_WIDTH = 50
RIGHT_PANEL_WIDTH = 100
PANEL_ELEMENTS = 2
PANEL_SIZE = (NUM_LINES - 1) * LINE_WIDTH // PANEL_ELEMENTS
FONT_SIZE = LINE_WIDTH // 3
DELTA = LINE_WIDTH // 2
PIECE_RAIDUS = int(LINE_WIDTH * 0.45)
SCREEN_HEIGHT = (NUM_LINES - 1) * LINE_WIDTH + 2 * DELTA
SCREEN_WIDTH = SCREEN_HEIGHT + RIGHT_PANEL_WIDTH


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

black_piece = pygame.image.load("weiqi_go/asset/black_piece.png")
black_piece.convert()
black_piece = pygame.transform.smoothscale(black_piece, (2 * PIECE_RAIDUS, 2 * PIECE_RAIDUS))

white_piece = pygame.image.load("weiqi_go/asset/white_piece.png")
white_piece.convert()
white_piece = pygame.transform.smoothscale(white_piece, (2 * PIECE_RAIDUS, 2 * PIECE_RAIDUS))
rect = black_piece.get_rect()


def draw_antialias_circles(screen, color, center, radius):
    pygame.gfxdraw.aacircle(screen, center[0], center[1], radius, color)
    pygame.gfxdraw.filled_circle(screen, center[0], center[1], radius, color)


def get_star_pos():
    if NUM_LINES == 9:
        all_star = [2, 4, 6]
    elif NUM_LINES == 13:
        all_star = [3, 6, 9]
    elif NUM_LINES == 19:
        all_star = [3, 9, 15]
    return all_star


class HistoryPool:
    def __init__(self):
        self.history = []
        self.poped_items = []

    def add(self, item):
        self.history.append(item)
        self.poped_items = []

    def recover_history_back(self):
        if len(self.history) > 0:
            poped_item = self.history.pop()
            self.poped_items.append(poped_item)
            return self.history[-1]

    def recover_history_forward(self):
        if len(self.poped_items) > 0:
            curr_item = self.poped_items.pop()
            self.history.append(curr_item)
            return curr_item


class PieceGroup:
    def __init__(self):
        self.group_pieces = set()       # 相连棋子群
        self.group_chis = set()         # 棋子的气
        self.group_dead_chis = set()    # 棋子死掉的气 （被敌方占领的气）


# TODO: 重置游戏按钮
# TODO: group_chis的变更改为类方式
# TODO: 黑子白子的最后一步棋的位置及步数，需要historypool记录？


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.piece_color = [BLACK, WHITE]
        self.font = pygame.font.SysFont("SimHei", FONT_SIZE)
        self.game_reset()

    def game_reset(self):
        self.curr_color = 0
        self.num_steps = 0
        self.board_state = [[-1 for _ in range(NUM_LINES)] for _ in range(NUM_LINES)]
        self.poped_states = []
        self.white_group_chis = []
        self.black_group_chis = []
        self.board_state_history = HistoryPool()
        self.board_state_history.add(deepcopy(self.board_state))
        self.white_group_chis_history = HistoryPool()
        self.white_group_chis_history.add(deepcopy(self.white_group_chis))
        self.black_group_chis_history = HistoryPool()
        self.black_group_chis_history.add(deepcopy(self.black_group_chis))
        self.is_dajie = False   # 是否打劫

    def init_gui(self):
        self.screen.fill(YELLOW)
        for i in range(0, NUM_LINES):
            pygame.draw.line(self.screen, BLACK, (DELTA, DELTA+LINE_WIDTH * i), (DELTA+(NUM_LINES-1)*LINE_WIDTH, DELTA+LINE_WIDTH * i))

        for i in range(0, NUM_LINES):
            pygame.draw.line(self.screen, BLACK, (DELTA+LINE_WIDTH * i, DELTA), (DELTA+LINE_WIDTH * i, DELTA+(NUM_LINES-1)*LINE_WIDTH))

        all_star = get_star_pos()
        for i in all_star:
            for j in all_star:
                center_x = i * LINE_WIDTH + DELTA
                center_y = j * LINE_WIDTH + DELTA
                # pygame.draw.circle(self.screen, BLACK, (center_x, center_y), PIECE_RAIDUS // 5)
                draw_antialias_circles(self.screen, BLACK, (center_x, center_y), PIECE_RAIDUS // 5)

    def _get_pos_chis(self, pos):
        pos_chis = set()
        pos_dead_chis = set()
        neighbor_flag = []
        all_neighbors = [
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1)
        ]
        for neighbor in all_neighbors:
            if 0 <= neighbor[0] < NUM_LINES and 0 <= neighbor[1] < NUM_LINES:
                if self.board_state[neighbor[0]][neighbor[1]] == -1:
                    pos_chis.add(neighbor)
                if self.board_state[neighbor[0]][neighbor[1]] == 1 - self.curr_color:
                    neighbor_flag.append(True)
                    pos_dead_chis.add(neighbor)
                else:
                    neighbor_flag.append(False)
        return pos_chis, pos_dead_chis, all(neighbor_flag)

    def _is_forbidden_point(self, pos):
        all_neighbors = [
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1)
        ]
        neighbor_flag = []
        for neighbor in all_neighbors:
            if 0 <= neighbor[0] < NUM_LINES and 0 <= neighbor[1] < NUM_LINES:
                if self.board_state[neighbor[0]][neighbor[1]] == 1 - self.curr_color:
                    neighbor_flag.append(True)
                else:
                    neighbor_flag.append(False)
        return all(neighbor_flag)

    def _can_take_pieces(self, black_group_chis, white_group_chis):
        def _get_take_groups(group_chis):
            take_groups, not_take_groups = [], []
            for group in group_chis:
                if len(group["group_chis"]) == 0:
                    take_groups.append(group)
                else:
                    not_take_groups.append(group)
            return take_groups, not_take_groups

        def _update_group_chis(same_color_group, diff_color_group):
            take_groups, diff_color_group = _get_take_groups(diff_color_group)
            take_pieces = []
            for take_group in take_groups:
                for piece in take_group["group_pieces"]:
                    take_pieces.append(piece)
                    for group in same_color_group:
                        if piece in group["group_dead_chis"]:
                            group["group_chis"].add(piece)
                            group["group_dead_chis"].remove(piece)
            return take_groups, take_pieces, same_color_group, diff_color_group

        if self.curr_color == 0:
            take_groups, take_pieces, black_group_chis, white_group_chis = _update_group_chis(
                                                                                black_group_chis,
                                                                                white_group_chis
                                                                            )
        else:
            take_groups, take_pieces, white_group_chis, black_group_chis = _update_group_chis(
                                                                                white_group_chis,
                                                                                black_group_chis
                                                                            )
        return take_groups, take_pieces, black_group_chis, white_group_chis

    def _update_same_color_group(self, pos, pos_chis, pos_dead_chis, groups_chis):
        pos_groups = {}
        new_groups_chis = []
        find_group = False
        for group in groups_chis:
            group_pieces = group["group_pieces"]
            group_chis = group["group_chis"]
            group_dead_chis = group["group_dead_chis"]
            if pos in group_chis:
                find_group = True
                if pos in pos_groups:
                    group_pieces |= pos_groups[pos][0]
                    group_chis |= pos_groups[pos][1]
                    group_dead_chis |= pos_groups[pos][2]
                pos_groups[pos] = [group_pieces, group_chis, group_dead_chis]
            else:
                new_groups_chis.append(group)

        if not find_group:
            pos_groups[pos] = [set(), set(), set()]

        for pos, v in pos_groups.items():
            new_groups_chis.append({
                "group_pieces": v[0] | {pos},
                "group_chis": (v[1] | pos_chis) - {pos},
                "group_dead_chis": v[2] | pos_dead_chis
            })
        return new_groups_chis

    def _update_diff_color_group(self, pos, pos_chis, pos_dead_chis, groups_chis):
        for group in groups_chis:
            group_chis = group["group_chis"]
            group_dead_chis = group["group_dead_chis"]
            if pos in group_chis:
                group_chis -= {pos}
                group_dead_chis |= {pos}
        return groups_chis

    def _update_chis(self, pos, pos_chis, pos_dead_chis):
        if self.curr_color == 0:
            new_black_group_chis = self._update_same_color_group(
                pos,
                pos_chis,
                pos_dead_chis,
                deepcopy(self.black_group_chis)
            )
            new_white_group_chis = self._update_diff_color_group(
                pos,
                pos_chis,
                pos_dead_chis,
                deepcopy(self.white_group_chis)
            )
        else:
            new_white_group_chis = self._update_same_color_group(
                pos,
                pos_chis,
                pos_dead_chis,
                deepcopy(self.white_group_chis)
            )
            new_black_group_chis = self._update_diff_color_group(
                pos,
                pos_chis,
                pos_dead_chis,
                deepcopy(self.black_group_chis)
            )
        return new_black_group_chis, new_white_group_chis

    def _can_move(self, pos):
        if pos[0] < 0 or pos[0] >= NUM_LINES:
            return False
        if pos[1] < 0 or pos[1] >= NUM_LINES:
            return False
        if self.board_state[pos[0]][pos[1]] != -1:
            return False
        return True

    def recover_history_back(self):
        board_state = self.board_state_history.recover_history_back()
        self.black_group_chis = deepcopy(self.black_group_chis_history.recover_history_back())
        self.white_group_chis = deepcopy(self.white_group_chis_history.recover_history_back())
        if board_state:
            self.board_state = deepcopy(board_state)
            self.num_steps -= 1
            self.curr_color = 1 - self.curr_color

    def recover_history_forward(self):
        board_state = deepcopy(self.board_state_history.recover_history_forward())
        self.black_group_chis = deepcopy(self.black_group_chis_history.recover_history_forward())
        self.white_group_chis = deepcopy(self.white_group_chis_history.recover_history_forward())
        if board_state:
            self.board_state = deepcopy(board_state)
            self.num_steps += 1
            self.curr_color = 1 - self.curr_color

    def draw_board(self):
        for i in range(NUM_LINES):
            for j in range(NUM_LINES):
                if self.board_state[i][j] != -1:
                    center_x = i * LINE_WIDTH + DELTA
                    center_y = j * LINE_WIDTH + DELTA
                    rect.center = center_x, center_y
                    if self.board_state[i][j] == 0:
                        screen.blit(black_piece, rect)
                    else:
                        screen.blit(white_piece, rect)
                    # pygame.gfxdraw.aacircle(screen, center_x, center_y, PIECE_RAIDUS, self.piece_color[self.board_state[i][j]])
                    # pygame.draw.circle(self.screen, self.piece_color[self.board_state[i][j]], (center_x, center_y), PIECE_RAIDUS)
                    # draw_antialias_circles(self.screen, self.piece_color[self.board_state[i][j]], (center_x, center_y), PIECE_RAIDUS)

    def _draw_curr_color(self, panel_index):
        center_x = SCREEN_HEIGHT - DELTA + (RIGHT_PANEL_WIDTH + DELTA) // 2
        center_y = PANEL_SIZE * panel_index + PANEL_SIZE // 2 + DELTA
        rect.center = center_x, center_y
        if self.curr_color == 0:
            screen.blit(black_piece, rect)
        else:
            screen.blit(white_piece, rect)
        # draw_antialias_circles(self.screen, self.piece_color[self.curr_color], (center_x, center_y), PIECE_RAIDUS)

    def draw_right_panel(self):
        self._draw_curr_color(0)

    def step(self, x, y):
        no_x = math.ceil((x - DELTA) / LINE_WIDTH + 0.5)
        no_y = math.ceil((y - DELTA) / LINE_WIDTH + 0.5)
        pos = (no_x - 1, no_y - 1)
        if self._can_move(pos):
            pos_chis, pos_dead_chis, is_forbidden = self._get_pos_chis(pos)
            new_black_group_chis, new_white_group_chis = self._update_chis(pos, pos_chis, pos_dead_chis)
            # 判断是否是禁着点，判断是否可以提子，判断是否会打劫
            take_groups, take_pieces, new_black_group_chis, new_white_group_chis = self._can_take_pieces(new_black_group_chis, new_white_group_chis)
            if not is_forbidden or len(take_groups) > 0:
                if len(take_pieces) == 1:
                    if self.is_dajie:
                        if pos == self.dajie_piece:
                            return
                        else:
                            self.is_dajie = False
                    else:
                        self.is_dajie = True
                        self.dajie_piece = take_pieces[0]
                else:
                    self.is_dajie = False

                for take_group in take_groups:
                    for piece in take_group["group_pieces"]:
                        self.board_state[piece[0]][piece[1]] = -1

                self.black_group_chis = new_black_group_chis
                self.white_group_chis = new_white_group_chis
                self.board_state[pos[0]][pos[1]] = self.curr_color
                self.curr_color = 1 - self.curr_color
                self.num_steps += 1

                self.board_state_history.add(deepcopy(self.board_state))
                self.black_group_chis_history.add(deepcopy(self.black_group_chis))
                self.white_group_chis_history.add(deepcopy(self.white_group_chis))

    def draw_view(self):
        self.init_gui()
        self.draw_right_panel()
        self.draw_board()


def run(g: Game):
    while True:
        is_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                is_pressed = False
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                is_pressed = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    g.game_reset()
                elif event.key == pygame.K_z:
                    g.recover_history_back()
                elif event.key == pygame.K_y:
                    g.recover_history_forward()
                elif event.key == pygame.K_q:
                    sys.exit()

        if is_pressed:
            g.step(x, y)
            # print(g.black_group_chis)

        g.draw_view()
        pygame.display.update()


if __name__ == '__main__':
    g = Game(screen)
    run(g)
