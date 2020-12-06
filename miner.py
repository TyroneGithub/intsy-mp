import pygame
import math
from queue import PriorityQueue
from spot import Spot

pygame.init()
WIN = pygame.display.set_mode((1000, 700))
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

  def get_type(self):
    return self.type
    
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




# def make_grid(rows, width):
#   grid = []
#   gap = width // rows
#   for i in range(rows):
#     grid.append([])
#     for j in range(rows):
#       spot = Spot(i, j, gap, rows, None)
#       grid[i].append(spot)

#   return grid


# def draw_grid(win, rows, width):
#   gap = width // rows
#   for i in range(rows):
#     pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
#     for j in range(rows):
#       pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


# def draw(win, grid, rows, width):
#   win.fill(WHITE)

#   for row in grid:
#     for spot in row:
#       spot.draw(win)

#   draw_grid(win, rows, width)
#   pygame.display.update()


# def get_clicked_pos(pos, rows, width):
#   gap = width // rows
#   y, x = pos

#   row = y // gap
#   col = x // gap

#   return row, col


def init_grid(rows):
  grid = []
  for row in range(rows):
    grid.append([])
    for column in range(rows):
      spot = Spot(row, column, rows, None)
      grid[row].append(spot)

  return grid

def draw_grid(width, dim, margin, grid, win):
  for row in range(dim):
    for column in range(dim):
      color = grid[row][column].get_color()
      pygame.draw.rect(win, color, [(margin + width) * column + margin,
                    (margin + width) * row + margin,width,width])

def get_clicked_pos(pos, width, margin):
  row = pos[1] // (width + margin)
  col= pos[0] // (width+margin)

  return row, col


def initialize_entities(grid):
  miner = GameObj(0, 0, "miner")
  row, col = miner.get_pos()
  grid[row][col].set_obj(miner)
  grid[row][col].miner()
  grid[row][col].init_front(grid)

  # grid[row][col].update_neighbors(grid)

  return miner


def move(miner, grid, row, col, win, ROWS, width):
  x, y = miner.get_pos()
  front = grid[x][y].get_front()
  grid[x][y].reset()
  miner.update_pos(row, col)
  grid[row][col].front = front
  grid[row][col].front_pos = grid[x][y].get_front_pos()
  # grid[row][col].scan(grid, lambda: draw_grid(win, grid, ROWS, width))
  grid[row][col].update_front(grid)
  grid[row][col].miner()


def text_init(texts, font, colors):
  # text = font.render('Pit', False, BLACK)
  # textRect = text.get_rect()
  # textRect.center = (550, 50)
  text_list = []
  text_rect_list = []
  y = 50
  for i in range(len(texts)):
    text_obj = font.render(texts[i], False, colors[i])
    text_rect = text_obj.get_rect()
    text_rect.center = (635, y)
    y += 50
    text_list.append(text_obj)
    text_rect_list.append(text_rect)
  
  return text_list, text_rect_list

def render_text(texts, text_rects, win):

  for i in range(len(texts)):
    win.blit(texts[i], text_rects[i])


def main(win, num_rows):
  ROWS = int(num_rows)
  grid = init_grid(ROWS)
  width = 1000 // (ROWS * 2)
  print(len(grid), len(grid[0]))
  margin = 1
  start = None
  end = None

  run = True

  miner = initialize_entities(grid)

  toggle_pit = False
  toggle_gold = False
  toggle_beacon = False

  # pit_color = RED
  # gold_color = GREEN
  # beacon_color = TURQUOISE

  area = pygame.Rect(0, 0, 1030//2, 515)


  # font = pygame.font.SysFont('Arial', 24)
  # text = font.render('Pit', False, BLACK)
  # textRect = text.get_rect()
  # textRect.center = (550, 50)

  texts = ['Pit [F] to toggle', 'Beacon [B] to toggle', 'Gold [G] to toggle']
  font = pygame.font.SysFont('Arial', 24)


  while run:
    pit_color = RED if toggle_pit else BLACK
    gold_color = GREEN if toggle_gold else BLACK
    beacon_color = TURQUOISE if toggle_beacon else BLACK
    
    colors = [pit_color, beacon_color, gold_color]

    text, rect = text_init(texts, font, colors)

    for event in pygame.event.get():

      if event.type == pygame.QUIT:
        run = False


      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if event.button == 1 and area.collidepoint(pos):
          row, col = get_clicked_pos(pos, width, margin)
          print(row, col)
          if not (toggle_pit or toggle_beacon or toggle_gold):
            x, y = miner.get_pos()
            grid[x][y].rotate_front(grid)

          if toggle_pit:
            pit = GameObj(row, col, "pit")
            grid[row][col].set_obj(pit)
            grid[row][col].pit()

          
          if toggle_beacon:
            beacon = GameObj(row, col, "beacon")
            grid[row][col].set_obj(beacon)
            grid[row][col].beacon()
          
          if toggle_gold:
            gold = GameObj(row, col, "gold")
            grid[row][col].set_obj(gold)
            grid[row][col].gold()       
            
      
      if event.type == pygame.KEYDOWN:
        x, y = miner.get_pos()
        if event.key == pygame.K_a:
          move(miner, grid, x, y-1, win, ROWS, width)
        if event.key == pygame.K_d:
          move(miner, grid, x, y+1, win, ROWS, width)
        if event.key == pygame.K_w:
          move(miner, grid, x-1, y, win, ROWS, width)
        if event.key == pygame.K_s:
          move(miner, grid, x+1, y, win, ROWS, width)
          
        if event.key == pygame.K_f: # toggle pit
          toggle_pit = not toggle_pit
          toggle_gold = False
          toggle_beacon = False
          # text[0] = font.render('Pit [F] to toggle', False, pit_color)

        if event.key == pygame.K_g: # toggle gold
          toggle_pit = False
          toggle_gold = not toggle_gold
          toggle_beacon = False
          # text[1] = font.render('Gold [G] to toggle', False, gold_color)

        if event.key == pygame.K_b: # toggle beacon
          toggle_pit = False
          toggle_gold = False
          toggle_beacon = not toggle_beacon
          # text[2] = font.render('Beacon [B] to toggle', False, beacon_color)



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
      win.fill(WHITE)
      pygame.draw.rect(win, BLACK, area)
      draw_grid(width, ROWS, margin, grid, win)
      # win.blit(text[0], rect[0])
      render_text(text, rect, win)
      pygame.display.flip()





  pygame.quit()


main(WIN, 8)
