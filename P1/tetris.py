import pygame
import random

# Game configuration
CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS
FPS = 60

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0)     # Z
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]]
]

def rotate(shape):
    return [ [ shape[y][x] for y in range(len(shape)) ] for x in range(len(shape[0]) - 1, -1, -1) ]

def collide(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= COLS or y + off_y >= ROWS:
                    return True
                if y + off_y >= 0 and board[y + off_y][x + off_x]:
                    return True
    return False

def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0 for _ in range(COLS)])
    return new_board, lines_cleared

def new_piece():
    idx = random.randint(0, len(SHAPES) - 1)
    return SHAPES[idx], COLORS[idx]

def draw_board(screen, board, piece, offset, color):
    screen.fill(BLACK)
    # Draw board
    for y in range(ROWS):
        for x in range(COLS):
            if board[y][x]:
                pygame.draw.rect(screen, board[y][x], (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw current piece
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:
                px = (x + offset[0]) * CELL_SIZE
                py = (y + offset[1]) * CELL_SIZE
                if y + offset[1] >= 0:
                    pygame.draw.rect(screen, color, (px, py, CELL_SIZE, CELL_SIZE))
    # Draw grid
    for x in range(COLS):
        pygame.draw.line(screen, GRAY, (x*CELL_SIZE, 0), (x*CELL_SIZE, HEIGHT))
    for y in range(ROWS):
        pygame.draw.line(screen, GRAY, (0, y*CELL_SIZE), (WIDTH, y*CELL_SIZE))

def animate_line_clear(screen, board, lines_to_clear, piece, offset, color):
    # Flash the lines white a few times
    for _ in range(3):
        temp_board = [row[:] for row in board]
        for y in lines_to_clear:
            temp_board[y] = [WHITE for _ in range(COLS)]
        draw_board(screen, temp_board, piece, offset, color)
        pygame.display.flip()
        pygame.time.delay(80)
        draw_board(screen, board, piece, offset, color)
        pygame.display.flip()
        pygame.time.delay(80)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    shape, color = new_piece()
    offset = [COLS // 2 - len(shape[0]) // 2, -2]
    fall_time = 0
    fall_speed = 0.5
    score = 0
    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        fall_time += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_offset = [offset[0] - 1, offset[1]]
                    if not collide(board, shape, new_offset):
                        offset = new_offset
                elif event.key == pygame.K_RIGHT:
                    new_offset = [offset[0] + 1, offset[1]]
                    if not collide(board, shape, new_offset):
                        offset = new_offset
                elif event.key == pygame.K_DOWN:
                    new_offset = [offset[0], offset[1] + 1]
                    if not collide(board, shape, new_offset):
                        offset = new_offset
                elif event.key == pygame.K_UP:
                    new_shape = rotate(shape)
                    if not collide(board, new_shape, offset):
                        shape = new_shape
        if fall_time > fall_speed:
            fall_time = 0
            new_offset = [offset[0], offset[1] + 1]
            if not collide(board, shape, new_offset):
                offset = new_offset
            else:
                # Place piece
                for y, row in enumerate(shape):
                    for x, cell in enumerate(row):
                        if cell and y + offset[1] >= 0:
                            board[y + offset[1]][x + offset[0]] = color
                # Find lines to clear
                lines_to_clear = [i for i, row in enumerate(board) if all(row)]
                if lines_to_clear:
                    animate_line_clear(screen, board, lines_to_clear, shape, offset, color)
                board, lines = clear_lines(board)
                score += lines
                # Check if any cell in the top row(s) is filled
                if any(board[0][x] != 0 for x in range(COLS)) or any(board[1][x] != 0 for x in range(COLS)):
                    running = False
                else:
                    shape, color = new_piece()
                    offset = [COLS // 2 - len(shape[0]) // 2, -2]
                    if collide(board, shape, offset):
                        running = False
        draw_board(screen, board, shape, offset, color)
        pygame.display.flip()
    print(f"Game Over! Your score: {score}")
    pygame.quit()

if __name__ == '__main__':
    main()
