
import pygame
import sys
import time
from collections import deque

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)

win = pygame.display.set_mode((WIDTH, HEIGHT + 60))
pygame.display.set_caption("Busca em Labirinto: BFS vs DFS")

maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
visited_path = [[0 for _ in range(COLS)] for _ in range(ROWS)]

start = (0, 0)
end = (ROWS - 1, COLS - 1)

font = pygame.font.SysFont("Arial", 20)

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(win, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(win, GRAY, (0, y), (WIDTH, y))

def draw_cell(pos, color):
    x, y = pos
    pygame.draw.rect(win, color, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(win, GRAY, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_maze():
    for i in range(ROWS):
        for j in range(COLS):
            if maze[i][j] == 1:
                draw_cell((i, j), BLACK)
            elif visited_path[i][j] == 1:
                draw_cell((i, j), BLUE)
            else:
                draw_cell((i, j), WHITE)
    draw_cell(start, GREEN)
    draw_cell(end, RED)

def find_start_end():
    return start, end

def visualize_path(path):
    for pos in path[1:-1]:
        draw_cell(pos, YELLOW)
        pygame.display.update()
        time.sleep(0.03)

def show_info(tempo, custo):
    info_text = f"Tempo: {tempo:.4f}s | Custo: {custo} passos"
    pygame.draw.rect(win, (30, 30, 30), (0, HEIGHT, WIDTH, 60))
    text_surface = font.render(info_text, True, ORANGE)
    win.blit(text_surface, (10, HEIGHT + 20))
    pygame.display.update()

def bfs():
    global visited_path
    print("🔎 Executando BFS...")
    s, e = find_start_end()
    start_time = time.time()
    visited_path = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    queue = deque([(s, [s])])
    visited = set([s])

    while queue:
        pygame.event.pump()
        curr, path = queue.popleft()

        if curr == e:
            end_time = time.time()
            tempo = end_time - start_time
            custo = len(path) - 1
            print(f"✅ BFS finalizado. Tempo: {tempo:.4f}s | Custo: {custo}")
            visualize_path(path)
            show_info(tempo, custo)
            return

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = curr[0]+dx, curr[1]+dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and (nx, ny) not in visited:
                if maze[nx][ny] != 1:
                    queue.append(((nx, ny), path + [(nx, ny)]))
                    visited.add((nx, ny))
                    visited_path[nx][ny] = 1
                    if (nx, ny) != e:
                        draw_cell((nx, ny), BLUE)
                        pygame.display.update()
                        time.sleep(0.01)

    show_info(0, 0)
    print("❌ Nenhum caminho encontrado com BFS.")

def dfs():
    global visited_path
    print("🔎 Executando DFS...")
    s, e = find_start_end()
    start_time = time.time()
    visited_path = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    stack = [(s, [s])]
    visited = set([s])

    while stack:
        pygame.event.pump()
        curr, path = stack.pop()

        if curr == e:
            end_time = time.time()
            tempo = end_time - start_time
            custo = len(path) - 1
            print(f"✅ DFS finalizado. Tempo: {tempo:.4f}s | Custo: {custo}")
            visualize_path(path)
            show_info(tempo, custo)
            return

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = curr[0]+dx, curr[1]+dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and (nx, ny) not in visited:
                if maze[nx][ny] != 1:
                    stack.append(((nx, ny), path + [(nx, ny)]))
                    visited.add((nx, ny))
                    visited_path[nx][ny] = 1
                    if (nx, ny) != e:
                        draw_cell((nx, ny), BLUE)
                        pygame.display.update()
                        time.sleep(0.01)

    show_info(0, 0)
    print("❌ Nenhum caminho encontrado com DFS.")

def reset_paths():
    global visited_path
    visited_path = [[0 for _ in range(COLS)] for _ in range(ROWS)]

def main():
    running = True
    draw_maze()
    draw_grid()
    pygame.display.update()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  
                mx, my = pygame.mouse.get_pos()
                if my < HEIGHT:
                    row, col = my // CELL_SIZE, mx // CELL_SIZE
                    if (row, col) != start and (row, col) != end:
                        maze[row][col] = 1
                        draw_cell((row, col), BLACK)
                        pygame.display.update()

            if pygame.mouse.get_pressed()[2]:  
                mx, my = pygame.mouse.get_pos()
                if my < HEIGHT:
                    row, col = my // CELL_SIZE, mx // CELL_SIZE
                    if (row, col) != start and (row, col) != end:
                        maze[row][col] = 0
                        draw_cell((row, col), WHITE)
                        pygame.display.update()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    draw_maze()
                    bfs()
                elif event.key == pygame.K_d:
                    draw_maze()
                    dfs()
                elif event.key == pygame.K_r:
                    reset_paths()
                    draw_maze()
                    pygame.draw.rect(win, (30, 30, 30), (0, HEIGHT, WIDTH, 60))
                    pygame.display.update()

    pygame.quit()
    sys.exit()

main()
