import pygame
import random

pygame.init()

# Screen dimensions
width, height = 400, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tetris')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
colors = [
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (0, 255, 0),    # Green
    (255, 0, 0),    # Red
    (128, 0, 128)   # Purple
]

# Tetrimino shapes
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1],
     [1, 1]],
    [[0, 1, 1],
     [1, 1, 0]],
    [[1, 1, 0],
     [0, 1, 1]],
    [[1, 1, 1],
     [0, 1, 0]],
    [[1, 1, 1],
     [1, 0, 0]],
    [[1, 1, 1],
     [0, 0, 1]]
]

# Board
board_width, board_height = 10, 20
board = [[0 for _ in range(board_width)] for _ in range(board_height)]

# Tetrimino class
class Tetrimino:
    def __init__(self):
        self.shape = random.choice(shapes)
        self.color = random.choice(colors)
        self.x = board_width // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self):
        for i, row in enumerate(self.shape):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(screen, self.color, pygame.Rect((self.x + j) * 20, (self.y + i) * 20, 20, 20))

def draw_board():
    for y in range(board_height):
        for x in range(board_width):
            if board[y][x]:
                pygame.draw.rect(screen, board[y][x], pygame.Rect(x * 20, y * 20, 20, 20))

def check_collision(shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                try:
                    if board[y + off_y][x + off_x] or x + off_x < 0 or x + off_x >= board_width or y + off_y >= board_height:
                        return True
                except IndexError:
                    return True
    return False

def remove_line():
    full_lines = 0
    for i, row in enumerate(board):
        if 0 not in row:
            full_lines += 1
            del board[i]
            board.insert(0, [0 for _ in range(board_width)])
    return full_lines

def main():
    clock = pygame.time.Clock()
    tetrimino = Tetrimino()
    running = True
    while running:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetrimino.x -= 1
                    if check_collision(tetrimino.shape, (tetrimino.x, tetrimino.y)):
                        tetrimino.x += 1
                if event.key == pygame.K_RIGHT:
                    tetrimino.x += 1
                    if check_collision(tetrimino.shape, (tetrimino.x, tetrimino.y)):
                        tetrimino.x -= 1
                if event.key == pygame.K_DOWN:
                    tetrimino.y += 1
                    if check_collision(tetrimino.shape, (tetrimino.x, tetrimino.y)):
                        tetrimino.y -= 1
                if event.key == pygame.K_UP:
                    tetrimino.rotate()
                    if check_collision(tetrimino.shape, (tetrimino.x, tetrimino.y)):
                        tetrimino.rotate()
                        tetrimino.rotate()
                        tetrimino.rotate()
        tetrimino.y += 1
        if check_collision(tetrimino.shape, (tetrimino.x, tetrimino.y)):
            tetrimino.y -= 1
            for i, row in enumerate(tetrimino.shape):
                for j, val in enumerate(row):
                    if val:
                        board[tetrimino.y + i][tetrimino.x + j] = tetrimino.color
            tetrimino = Tetrimino()
            if check_collision(tetrimino.shape, (tetrimino.x, tetrimino.y)):
                running = False
        full_lines = remove_line()
        draw_board()
        tetrimino.draw()
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()

if __name__ == '__main__':
    main()
