import pygame, sys, random
from pygame.math import Vector2
from pynput.keyboard import Key, Controller
import Brain

cell_size = 40
cell_number = 10

clock = pygame.time.Clock()

screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
grids = [Vector2(i, j) for i in range(cell_number) for j in range(cell_number)]


class SNAKE:
    def __init__(self):
        self.body = [Vector2(4, cell_number / 2), Vector2(3, cell_number / 2), Vector2(2, cell_number / 2)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            # pygame.draw.rect(screen, (255, 0, 0), block_rect)
            # screen.blit(screen,block_rect)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5, cell_number / 2), Vector2(4, cell_number / 2), Vector2(3, cell_number / 2)]
        self.direction = Vector2(1, 0)
        self.new_block = False


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:

    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.apple = 0
        self.step = 0
        self.lastapple = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        if self.check_fail() == 1:
            return 1

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):

        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.apple += 1

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def calculate_features(self):

        features = []
        lstop = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        # up right down left
        lst = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        head_diriction = lstop[
            lst.index((int(self.snake.body[0].x) - int(self.snake.body[1].x),
                       int(self.snake.body[0].y) - int(self.snake.body[1].y)))
        ]
        (x, y) = self.snake.body[0]
        x = int(x)
        y = int(y)
        # up
        d1 = [Vector2(x, _) for _ in range(y - 1, -1, -1)]
        # right
        d3 = [Vector2(_, y) for _ in range(x + 1, cell_number)]
        # down
        d5 = [Vector2(x, _) for _ in range(y + 1, cell_number)]
        # left
        d7 = [Vector2(_, y) for _ in range(x - 1, -1, -1)]
        # left-Top
        d8 = [Vector2(x - _, y - _) for _ in range(1, min(x, y) + 1)]
        # right-bottom
        d4 = [Vector2(x + _, y + _) for _ in range(1, min(cell_number - x, cell_number - y))]
        # right-top
        d2 = [Vector2(x + _, y - _) for _ in range(1, 10) if
              Vector2(x + _, y - _) in grids]
        # left-bottom
        d6 = [Vector2(x - _, y + _) for _ in range(1, 10) if
              Vector2(x - _, y + _) in grids]
        d, val = [d1, d2, d3, d4, d5, d6, d7, d8], min(cell_number, cell_number) - 1
        wall_distance = [len(i) / val for i in d]
        food_presence = [(val - j.index(self.fruit.pos)) / val if self.fruit.pos in j else 0 for j in d]
        body_presence = [min([dv.index(v) if v in self.snake.body else val for v in dv]) / val if dv else 0 for dv in d]

        for i in range(8):
            features.append(wall_distance[i])
            features.append(body_presence[i])
            features.append(food_presence[i])

        features = features + head_diriction

        return features

    def check_fail(self):
        if self.snake.body[0].x < 0 or self.snake.body[0].y < 0 or self.snake.body[0].x >= cell_number or \
                self.snake.body[0].y >= cell_number:
            #  self.snake.reset()
            return 1

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                # self.snake.reset()
                return 1

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        bg_rect = pygame.Rect(score_rect.left, score_rect.top, score_rect.width + score_rect.width + 6,
                              score_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)


def run_game(weights):
    pygame.init()

    # SCREEN_UPDATE = pygame.USEREVENT
    # pygame.time.set_timer(SCREEN_UPDATE, 40)

    main_game = MAIN()

    while True:
        screen.fill((175, 215, 70))
        main_game.draw_elements()
        pygame.display.update()
        kb = Controller()
        clock.tick(60)
        if main_game.step >= 100 and main_game.step % 400 == 0:
            if main_game.lastapple < main_game.apple:
                main_game.lastapple = main_game.apple
            else:
                # main_game.apple = 0
                return main_game.apple, main_game.step

        if main_game.update() == 1:
            return main_game.apple, main_game.step

        features = main_game.calculate_features()
        key = Brain.forward(weights, features)

        main_game.step += 1

        if key == 0:
            kb.press(Key.up)
            kb.release(Key.up)
        elif key == 1:
            kb.press(Key.right)
            kb.release(Key.right)
        elif key == 2:
            kb.press(Key.down)
            kb.release(Key.down)
        elif key == 3:
            kb.press(Key.left)  # Presses "left" key
            kb.release(Key.left)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1 and main_game.snake.direction.y != -1:
                        # main_game.step += 1
                        main_game.snake.direction = Vector2(0, -1)
                        # print('up')
                elif event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1 and main_game.snake.direction.x != 1:
                        # main_game.step += 1
                        main_game.snake.direction = Vector2(1, 0)
                        # print('right')
                elif event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != 1 and main_game.snake.direction.y != -1:
                        # main_game.step += 1
                        main_game.snake.direction = Vector2(0, 1)
                        # print('down')
                elif event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != -1 and main_game.snake.direction.x != 1:
                        # main_game.step += 1
                        main_game.snake.direction = Vector2(-1, 0)
                        # print('left')
