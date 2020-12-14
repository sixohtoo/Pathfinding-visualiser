import pygame
from queue import PriorityQueue
import random

DRAW = 1
IMMEDIATE = 1
FAST = 2
SLOW = 3
# DRAW == 1 is immediate
# DRAW == 2 is quick visualiser
# DRAW == 3 is slow visualiser


DIJKSTRA = 1
ASTAR = 0
ALGORITHM = 2

WIDTH = 800
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding visualiser")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (125, 0, 125)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
LIGHT_BLUE = (0, 191, 255)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.colour == RED

    def is_open(self):
        return self.colour == GREEN

    def is_barrier(self):
        return self.colour == BLACK

    def is_start(self):
        return self.colour == ORANGE

    def is_end(self):
        return self.colour == LIGHT_BLUE

    def is_path(self):
        return self.colour == WHITE

    def is_route(self):
        return self.colour == PURPLE

    def reset(self):
        self.colour = WHITE

    def make_start(self):
        self.colour = ORANGE

    def make_closed(self):
        self.colour = RED

    def make_open(self):
        self.colour = GREEN

    def make_barrier(self):
        self.colour = BLACK

    def make_end(self):
        self.colour = LIGHT_BLUE

    def make_route(self):
        self.colour = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # UP
            self.neighbours.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # DOWN
            self.neighbours.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # LEFT
            self.neighbours.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # RIGHT
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


class Grid():
    def __init__(self, rows, width, win):
        self.rows = rows
        self.width = width
        self.grid = []
        self.win = win

    def make_grid(self):
        grid = []
        gap = self.width // self.rows
        for i in range(self.rows):
            grid.append([])
            for j in range(self.rows):
                spot = Node(i, j, gap, self.rows)
                grid[i].append(spot)
        self.grid = grid

    def get_spot(self, row, col):
        return self.grid[row][col]

    def update_neighbours(self):
        for row in self.grid:
            for spot in row:
                spot.update_neighbours(self.grid)

    def draw_grid(self):
        gap = self.width // self.rows
        for i in range(self.rows):
            pygame.draw.line(win, GREY, (0, i * gap), (self.width, i * gap))
            for j in range(self.rows):
                pygame.draw.line(self.win, GREY, (j * gap, 0), (j * gap, self.width))

    def draw(self):
        win.fill(WHITE)
        for row in self.grid:
            for spot in row:
                if DRAW != IMMEDIATE or not (spot.is_open() or spot.is_closed()):
                    spot.draw(self.win)

        self.draw_grid()
        pygame.display.update()

    def remove_path(self):
        for row in self.grid:
            for spot in row:
                if spot.is_open():
                    spot.reset()
                elif spot.is_closed():
                    spot.reset()
                elif spot.is_route():
                    spot.reset()

    def reconstruct_path(self, came_from, current):
        while current in came_from:
            current = came_from[current]
            current.make_route()
            if DRAW != IMMEDIATE:
                self.draw()

    def dijkstra(self, start, end):
        count = 0
        dist = {spot: float("inf") for row in self.grid for spot in row}
        dist[start] = 0
        # pred = [-1 for _ in range(len(grid) * len(grid[0]))]
        came_from = {}
        open_set = {start}
        open_list = [start]
        if DRAW == 2:
            open_list.append('draw')

        while open_list:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_list.pop(0)
            if current == 'draw':
                # time.sleep(0.1)
                self.draw()
                open_list.append('draw')
                continue
            open_set.remove(current)

            if current == end:
                self.reconstruct_path(came_from, end)
                end.make_end()
                start.make_start()
                return True

            for neighbour in current.neighbours:
                distance = count + 1
                if distance < dist[neighbour]:
                    came_from[neighbour] = current
                    dist[neighbour] = distance
                    if neighbour not in open_set:
                        count += 1  # COULD BE WRONG IDK honestly
                        open_list.append(neighbour)
                        open_set.add(neighbour)
                        neighbour.make_open()
            if DRAW == SLOW:
                self.draw()
            if current != start:
                current.make_closed()
        return False

    @staticmethod
    def h(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def astar(self, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for row in self.grid for spot in row}
        g_score[start] = 0
        f_score = {spot: float("inf") for row in self.grid for spot in row}
        f_score[start] = self.h(start.get_pos(), end.get_pos())
        to_draw = set()

        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                self.reconstruct_path(came_from, end)
                end.make_end()
                start.make_start()
                return True

            for neighbour in current.neighbours:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = temp_g_score
                    f_score[neighbour] = temp_g_score + self.h(neighbour.get_pos(), end.get_pos())
                    if neighbour not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbour], count, neighbour))
                        open_set_hash.add(neighbour)
                        neighbour.make_open()
                        to_draw.add(neighbour)

            if DRAW == SLOW:
                self.draw()
            elif DRAW == FAST:
                for spot in to_draw:
                    spot.draw(win)
                to_draw = set()
                self.draw()
            if current != start:
                current.make_closed()
        return False

    def init_maze(self, start):
        for row in self.grid:
            for spot in row:
                if spot != start:
                    spot.make_barrier()

    @staticmethod
    def add_frontiers(frontiers, frontiers_set, cell, grid):
        directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
        row, col = cell.row, cell.col
        for y, x in directions:
            if 0 < row + y < len(grid) - 1 and 0 < col + x < len(grid) - 2:
                if grid[row + y][col + x].is_barrier() and grid[row + y][col + x] not in frontiers_set:
                    frontiers.append(grid[row + y][col + x])
                    frontiers_set.add(grid[row + y][col + x])

    @staticmethod
    def add_connecting_path(cell, grid):
        directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
        neighbours = []
        row, col = cell.row, cell.col
        for y, x in directions:
            if 0 < row + y < len(grid) - 1 and 0 < col + x < len(grid) - 1:
                if grid[row + y][col + x].is_path() or grid[row + y][col + x].is_start():
                    neighbours.append(grid[row + y][col + x])
        connector = neighbours.pop(random.randrange(len(neighbours)))
        con_row, con_col = connector.row, connector.col
        grid[(row + con_row) // 2][(col + con_col) // 2].reset()

    def generate_maze(self, start):
        frontiers = []
        frontiers_set = set()
        self.add_frontiers(frontiers, frontiers_set, start, self.grid)
        while frontiers:
            self.draw()
            # time.sleep(0.5)
            cell = frontiers.pop(random.randrange(len(frontiers)))
            cell.reset()
            self.add_frontiers(frontiers, frontiers_set, cell, self.grid)
            self.add_connecting_path(cell, self.grid)

    @staticmethod
    def get_clicked_position(pos, rows, width):
        gap = width // rows
        y, x = pos
        row = y // gap
        col = x // gap
        return row, col


def main(win, width):
    global ALGORITHM
    global DRAW
    ROWS = 50
    grid = Grid(ROWS, width, win)
    grid.make_grid()

    start = None
    end = None
    run = True

    while run:
        grid.draw()
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            run = False

        # Left mouse button
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            row, col = Grid.get_clicked_position(pos, ROWS, width)
            spot = grid.get_spot(row, col)
            if not start and spot != end:
                start = spot
                start.make_start()

            elif not end and spot != start:
                end = spot
                end.make_end()

            elif spot != end and spot != start:
                spot.make_barrier()

        # Right mouse button
        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            row, col = Grid.get_clicked_position(pos, ROWS, width)
            spot = grid.get_spot(row, col)
            spot.reset()
            if spot == start:
                start = None
            elif spot == end:
                end = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start and end:
                grid.update_neighbours()
                if ALGORITHM == ASTAR:
                    grid.astar(start, end)
                else:
                    grid.dijkstra(start, end)

            elif event.key == pygame.K_m and start:
                end = None
                grid.init_maze(start)
                grid.generate_maze(start)

            elif event.key == pygame.K_c:
                start = None
                end = None
                grid.make_grid()

            elif event.key == pygame.K_r:
                grid.remove_path()

            elif event.key == pygame.K_t:
                ALGORITHM = (ALGORITHM + 1) % 2

            elif event.key == pygame.K_1:
                DRAW = 1

            elif event.key == pygame.K_2:
                DRAW = 2

            elif event.key == pygame.K_3:
                DRAW = 3

    pygame.quit()


main(win, WIDTH)
