import pygame
from collections import deque
import time
import copy

# --- CONFIGURAÇÕES INICIAIS ---
WIDTH, HEIGHT = 500, 550  # espaço extra para os botões
ROWS, COLS = 5, 5
CELL_SIZE = WIDTH // COLS

# --- CORES ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 100, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER = (150, 150, 150)
TEXT_COLOR = (255, 255, 255)

# --- LABIRINTO ---
original_maze = [
    ['S', 0,  1,  0,  0],
    [1,   0, 1,  0,  1],
    [0,   0, 0,  0,  0],
    [0,   1, 1,  1,  0],
    [0,   0, 0,  'E', 0]
]

maze = copy.deepcopy(original_maze)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BFS Maze Solver")
font = pygame.font.SysFont(None, 30)

# --- FUNÇÕES DE BOTÕES ---
def draw_button(rect, text, hover=False):
    color = BUTTON_HOVER if hover else BUTTON_COLOR
    pygame.draw.rect(win, color, rect)
    txt = font.render(text, True, TEXT_COLOR)
    win.blit(txt, (rect.x + 15, rect.y + 10))

# --- FUNÇÕES AUXILIARES ---
def draw_grid():
    for i in range(ROWS):
        for j in range(COLS):
            x, y = j * CELL_SIZE, i * CELL_SIZE
            cell = maze[i][j]
            color = WHITE

            if cell == 1:
                color = BLACK
            elif cell == 'S':
                color = GREEN
            elif cell == 'E':
                color = RED

            pygame.draw.rect(win, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(win, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

def color_cell(pos, color):
    x, y = pos[1] * CELL_SIZE, pos[0] * CELL_SIZE
    pygame.draw.rect(win, color, (x, y, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(win, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

def find_points():
    start = end = None
    for i in range(ROWS):
        for j in range(COLS):
            if maze[i][j] == 'S':
                start = (i, j)
            elif maze[i][j] == 'E':
                end = (i, j)
    return start, end

def bfs_visual():
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    start, end = find_points()
    queue = deque([(start, [start])])
    visited = set()
    visited.add(start)

    while queue:
        pygame.event.pump()
        (x, y), path = queue.popleft()

        if (x, y) != start and (x, y) != end:
            color_cell((x, y), BLUE)
            pygame.display.update()
            time.sleep(0.1)

        if (x, y) == end:
            for pos in path:
                if pos != start and pos != end:
                    color_cell(pos, YELLOW)
                    pygame.display.update()
                    time.sleep(0.05)
            return

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < ROWS and 0 <= ny < COLS:
                if maze[nx][ny] != 1 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))

# --- LOOP PRINCIPAL ---
def main():
    global maze
    running = True
    started = False

    # Botões
    start_button = pygame.Rect(50, HEIGHT - 40, 120, 30)
    reset_button = pygame.Rect(200, HEIGHT - 40, 120, 30)

    while running:
        win.fill((240, 240, 240))

        draw_grid()
        draw_button(start_button, "Iniciar", start_button.collidepoint(pygame.mouse.get_pos()))
        draw_button(reset_button, "Reiniciar", reset_button.collidepoint(pygame.mouse.get_pos()))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos) and not started:
                    started = True
                    bfs_visual()

                elif reset_button.collidepoint(event.pos):
                    maze = copy.deepcopy(original_maze)
                    started = False

    pygame.quit()

if __name__ == "__main__":
    main()
