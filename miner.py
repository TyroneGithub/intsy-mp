import pygame
import math
from queue import PriorityQueue
from spot import Spot

WIDTH = 400
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class GameObj:
  def __init__(self, row, col, obj_type):
    self.row = row
    self.col = col
    self.type = obj_type

  def get_pos(self):
    return self.row, self.col

  def update_pos(self, row, col):
    self.row = row
    self.col = col


def h(p1, p2):
  x1, y1 = p1
  x2, y2 = p2
  return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
  while current in came_from:
    current = came_from[current]
    current.make_path()
    draw()


def algorithm(draw, grid, start, end):
  count = 0
  open_set = PriorityQueue()
  open_set.put((0, count, start))
  came_from = {}
  g_score = {spot: float("inf") for row in grid for spot in row}
  g_score[start] = 0
  f_score = {spot: float("inf") for row in grid for spot in row}
  f_score[start] = h(start.get_pos(), end.get_pos())

  open_set_hash = {start}

  while not open_set.empty():
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()

    current = open_set.get()[2]
    open_set_hash.remove(current)

    if current == end:
      reconstruct_path(came_from, end, draw)
      end.make_end()
      return True

    for neighbor in current.neighbors:
      temp_g_score = g_score[current] + 1

      if temp_g_score < g_score[neighbor]:
        came_from[neighbor] = current
        g_score[neighbor] = temp_g_score
        f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
        if neighbor not in open_set_hash:
          count += 1
          open_set.put((f_score[neighbor], count, neighbor))
          open_set_hash.add(neighbor)
          neighbor.make_open()

      draw()

      if current != start:
        current.make_closed()

  return False


def make_grid(rows, width):
  grid = []
  gap = width // rows
  for i in range(rows):
    grid.append([])
    for j in range(rows):
      spot = Spot(i, j, gap, rows)
      grid[i].append(spot)

  return grid


def draw_grid(win, rows, width):
  gap = width // rows
  for i in range(rows):
    pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
      pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
  win.fill(WHITE)

  for row in grid:
    for spot in row:
      spot.draw(win)

  draw_grid(win, rows, width)
  pygame.display.update()


def get_clicked_pos(pos, rows, width):
  gap = width // rows
  y, x = pos

  row = y // gap
  col = x // gap

  return row, col


def initialize_entities(grid):
  miner = GameObj(0, 0, "miner")
  row, col = miner.get_pos()
  grid[row][col].miner()
  grid[row][col].init_front(grid)

  # grid[row][col].update_neighbors(grid)

  pit = GameObj(1, 2, "pit")
  row, col = pit.get_pos()
  grid[row][col].pit()

  beacon = GameObj(4, 5, "beacon")
  row, col = beacon.get_pos()
  grid[row][col].beacon()

  gold = GameObj(3, 5, "gold")
  row, col = gold.get_pos()
  grid[row][col].gold()

  return miner, pit, beacon, gold


def move(miner, grid, row, col):
  x, y = miner.get_pos()
  front = grid[x][y].get_front()
  grid[x][y].reset()
  miner.update_pos(row, col)
  grid[row][col].front = front
  grid[row][col].front_pos = grid[x][y].get_front_pos()
  grid[row][col].update_front(grid)
  grid[row][col].miner()


def main(win, width, num_rows):
  ROWS = int(num_rows)
  grid = make_grid(ROWS, width)

  start = None
  end = None

  run = True

  miner, pit, beacon, gold = initialize_entities(grid)

  while run:
    draw(win, grid, ROWS, width)
    row, col = pit.get_pos()
    grid[row][col].pit()

    for event in pygame.event.get():

      if event.type == pygame.QUIT:
        run = False

      if pygame.mouse.get_pressed()[0]:  # LEFT
        x, y = miner.get_pos()
        grid[x][y].rotate_front(grid)

        # pos = pygame.mouse.get_pos()
        # row, col = get_clicked_pos(pos, ROWS, width)
        # if not grid[row][col].is_pit():
        #     move(miner, grid, row, col)
      
      if event.type == pygame.KEYDOWN:
        x, y = miner.get_pos()
        if event.key == pygame.K_w:
          move(miner, grid, x, y-1)
        if event.key == pygame.K_s:
          move(miner, grid, x, y+1)
        if event.key == pygame.K_a:
          move(miner, grid, x-1, y)
        if event.key == pygame.K_d:
          move(miner, grid, x+1, y)

          # else:
          # 	print('fuck')

          # if not start and spot != end:
          # 	start = spot
          # 	start.make_start()

          # elif not end and spot != start:
          # 	end = spot
          # 	end.make_end()

          # elif spot != end and spot != start:
          # 	spot.make_barrier()

      # if event.type == pygame.KEYDOWN:
      # 	if event.key == pygame.K_SPACE and start and end:
      # 		for row in grid:
      # 			for spot in row:
      # 				spot.update_neighbors(grid)

      # 		algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

      # 	if event.key == pygame.K_c:
      # 		start = None
      # 		end = None
      # 		grid = make_grid(ROWS, width)

  pygame.quit()


main(WIN, WIDTH, 8)
