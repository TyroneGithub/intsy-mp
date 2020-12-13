import pygame
import math
from spot import Spot
from gui_components import GUI
import random
from datetime import datetime

pygame.init()
WIN = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Gold Miner")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 128, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
BACKGROUND = (23, 16, 12)

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
      image = None
      rect = pygame.draw.rect(win, color, [(margin + width) * column + margin,
                    (margin + width) * row + margin,width,width])
      if grid[row][column].get_obj is None:
        image = pygame.image.load('None.png').convert()

      if grid[row][column].is_miner():
        image = pygame.image.load('Miner.png').convert()

      elif grid[row][column].is_gold():
        image = pygame.image.load('Goal.png').convert()
        
      elif grid[row][column].is_pit():
        image = pygame.image.load('Pit.png').convert()

      elif grid[row][column].is_visited():
        image = pygame.image.load('Visited.png').convert()

      elif grid[row][column].is_beacon():
        image = pygame.image.load('Beacon.png').convert()
      if image is not None:
        image = pygame.transform.scale(image, ((margin*2 + width),
                      (margin*2 + width)))
        win.blit(image, rect)
      

def get_clicked_pos(pos, width, margin):
  row = pos[1] // (width + margin)
  col= pos[0] // (width+margin)

  return row, col


def initialize_entities(grid):
  miner = GameObj(0, 0, "miner")
  row, col = miner.get_pos()
  grid[row][col].miner()
  grid[row][col].init_front(grid)

  return miner

def check(grid, row, col, ROWS):
  if  row >= 0 <= col and row < ROWS > col:
    if grid[row][col].get_obj() is not None:
      if grid[row][col].is_pit():
        return 'pit'
      if grid[row][col].is_beacon():
        print('beacon')
      if grid[row][col].is_gold():
        return 'gold'
    else:
      return None
  return None

def move(miner, grid, row, col, win, ROWS, width):
  x, y = miner.get_pos()

  if  row >= 0 <= col and row < ROWS > col:

    visited = GameObj(x, y, 'visited')
    if grid[x][y].is_visited():
      grid[x][y].increase_visit()
    else:
      grid[x][y].set_obj(visited)

    grid[x][y].reset()
    miner.update_pos(row, col)
    grid[row][col].miner()

  else:
    miner.update_pos(x, y)
    grid[x][y].miner()

def compare_len(arr1, arr2):
  return len(arr1) >= len(arr2)    


def update_pos(row, col, direction):
  if direction == 'top':
    row -= 1
  elif direction == 'bottom':
    row += 1
  elif direction == 'left':
    col -= 1
  elif direction == 'right':
    col += 1

  return row, col


def smart_move2(miner, grid, win, ROWS, width):
  if search_gold(grid, ROWS):
    run = True
    row, col =  miner.get_pos()
    while run:
      directions = ['top', 'bottom', 'left', 'right']
      items = grid[row][col].scan2(grid, ROWS)
      # print(items)
      visited = GameObj(row, col, 'visited')
      if grid[row][col].is_visited():
        grid[row][col].increase_visit()
      else:
        grid[row][col].set_obj(visited)

      grid[row][col].reset()
      try:
        direction = directions[items.index('gold')]
        row, col = update_pos(row, col, direction)
      except ValueError:
        if None in items:
          direction = directions[items.index(None)]
        elif 'visited' in items:
          direction = directions[items.index('visited')]
        elif 'pit' in items :
          direction = directions[items.index('pit')]
          row, col = update_pos(row, col, direction)
          row2 = row
          col2 = col
          if check(grid, row2, col2, ROWS) == 'pit': 
            direction = directions[items.index('pit')]
            row, col = update_pos(row, col, direction)
        row, col = update_pos(row, col, direction)
      finally:
        miner.update_pos(row, col)
        grid[row][col].miner()
        if check(grid, row, col, ROWS) == 'gold' or check(grid, row, col, ROWS) == 'pit':
          return 'Dead' if check(grid, row, col, ROWS) == 'pit' else 'Gold Found'

        draw_grid(width, ROWS, 2, grid, win)
        pygame.display.flip()
        pygame.time.delay(100)




def smart_move(miner, grid, win, ROWS, width, points):
  if search_gold(grid, ROWS):
    run = True
    row, col = miner.get_pos()

    while run:
      points = [0, 0, 0, 0]
      directions = ['top', 'bottom', 'left', 'right']

      points = grid[row][col].scan(grid, ROWS, points)
      max_index = points.index(max(points))
      direction = directions[max_index]
      print(points, direction)
      print()
      visited = GameObj(row, col, 'visited')
      if grid[row][col].is_visited():
        grid[row][col].increase_visit()
      else:
        grid[row][col].set_obj(visited)

      grid[row][col].reset()
      row, col = update_pos(row, col, direction)
      miner.update_pos(row, col)
      grid[row][col].miner()
      if check(grid, row, col, ROWS) == 'gold' or check(grid, row, col, ROWS) == 'pit':
        return 'Dead' if check(grid, row, col, ROWS) == 'pit' else 'Gold Found'

      draw_grid(width, ROWS, 2, grid, win)
      pygame.display.flip()
      pygame.time.delay(100)


def search_gold(grid, rows):
  for row in range(rows):
    for col in range(rows):
      if grid[row][col].is_gold() is not None:
        return True
  return False


def randomize_move(x, y, num, rows):
  if num == 1:
    x = x + 1 if x < rows else x - 1
  elif num == 2:
    x = x - 1 if x >= 0 else x + 1
  elif num == 3:
    y =y + 1 if y < rows else y - 1
  elif num == 4:
    y = y - 1 if y >= 0 else y + 1
  return x, y


def random_move(miner, grid, win, rows, width):
  x, y = miner.get_pos()
  run = False
  random.seed(datetime.now())
  if search_gold(grid, rows):
    run = True
    while run:
      num = random.randint(1, 4)
      x, y = randomize_move(x, y, num, rows)
      move(miner,grid, x, y, win, rows, width)    
      draw_grid(width, rows, 2, grid, win)
      pygame.display.flip()
      pygame.time.delay(100)
      if check(grid, x, y, rows) == 'gold' or check(grid, x, y, rows) == 'pit':
        return 'Dead' if check(grid, x, y, rows) == 'pit' else 'Gold Found'



def main(win, num_rows):
  ROWS = int(num_rows)
  grid = init_grid(ROWS)
  area_w = 800
  width = area_w // (ROWS * 2) 
  margin = 2
  start = None
  end = None

  run = True

  miner = initialize_entities(grid)

  toggle_pit = False
  toggle_gold = False
  toggle_beacon = False

  pits = []
  beacons = []
  gold = None
  area = pygame.Rect(0, 0, (margin + width) * ROWS + margin + 5, (margin + width) * ROWS + margin + 5)
  points = [0, 0, 0, 0]
  input_text = ''

  texts = ['[F] to toggle Pit ', '[B] to toggle Beacon', '[G] to toggle Gold']
  button_texts = ['Random', 'Smart', 'Kinda Smart']

  font = pygame.font.SysFont('Arial', 18)
  # move_ctr, move_ctr_rect = GUI.text_setup('Moves: ', font, 575, 220, BLACK)
  status_text, status_rect = GUI.text_setup('Status: ', font, 575, 300, BLACK)
  
  # input_box, input_dim, box = GUI.input_box(font, win, input_text)

  active_input = False

  curr_status_text = 'Alive'

  while run:
    pit_color = RED if toggle_pit else BLACK
    gold_color = GREEN if toggle_gold else BLACK
    beacon_color = TURQUOISE if toggle_beacon else BLACK
    input_color = TURQUOISE if not active_input else BLUE
    
    colors = [pit_color, beacon_color, gold_color]

    text, rect = GUI.text_list_setup(texts, font, colors, 90, 600)
    button_text, button_rect = GUI.text_list_setup(button_texts, font, [WHITE, WHITE, WHITE],635, 250)
    curr_status, curr_rect = GUI.text_setup(curr_status_text, font, 650, 300, BLACK)

    grid_butt, grid_rect = GUI.text_setup('Generate', font, 750, 10, WHITE)

    for event in pygame.event.get():
      win.fill(WHITE)
      pygame.draw.rect(win, BACKGROUND, area)
      draw_grid(width, ROWS, margin, grid, win)

      
      button_rect[0].width = 120
      button_rect[0].height = 40
      button_rect[0].center = (615, 150)
      pygame.draw.rect(win, BLUE, button_rect[0])

      button_rect[1].width = 120
      button_rect[1].height = 40
      button_rect[1].center = (760, 150)
      pygame.draw.rect(win, BLUE, button_rect[1])

      button_rect[2].width = 120
      button_rect[2].height = 40
      button_rect[2].center = (900, 150)
      pygame.draw.rect(win, BLUE, button_rect[2])

      grid_rect.width = 120
      grid_rect.height = 32
      grid_rect.center = (770, 25)
      pygame.draw.rect(win, BLUE, grid_rect)

      GUI.render_text(text, rect, win)
      # GUI.render_text([move_ctr], [move_ctr_rect], win)
      GUI.render_text([status_text, curr_status], [status_rect, curr_rect], win)


      win.blit(button_text[0], (580,140))
      win.blit(button_text[1], (735,140))
      win.blit(button_text[2], (850,140))

      win.blit(grid_butt, (733,14))


      input_box, input_dim, box = GUI.input_box(font, win, input_text)
      win.blit(input_box, input_dim)
      pygame.draw.rect(win, input_color, box, 2)

      # input_text = GUI.input_box(font, event, win, input_text)
      pygame.display.flip()

      if event.type == pygame.QUIT:
        run = False

      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()

        
          
        # if event.type == pygame.KEYDOWN and active_input: 

        if event.button == 1 :
          if box.collidepoint(event.pos):
            active_input = not active_input

          if button_rect[0].collidepoint(pos):
            curr_status_text = random_move(miner, grid, win, ROWS, width)

          if button_rect[1].collidepoint(pos):
            curr_status_text = smart_move(miner, grid, win, ROWS, width, points)

          if button_rect[2].collidepoint(pos):
            curr_status_text = smart_move2(miner, grid, win, ROWS, width)

          
          
          if grid_rect.collidepoint(pos):
            num_rows = int(input_text)
            if num_rows >= 8 and num_rows <= 64:
              main(win, num_rows)
              break
          if area.collidepoint(pos):
            row, col = get_clicked_pos(pos, width, margin)

            if toggle_pit:
              pit = GameObj(row, col, "pit")
              grid[row][col].set_obj(pit)
              grid[row][col].pit()
              pits.append(pit)
            
            if toggle_beacon:
              gold_row, gold_col = gold.get_pos() if gold is not None else (0, 0)
              if gold is not None and (gold_row == row or gold_col == col):
                beacon = GameObj(row, col, "beacon")
                grid[row][col].set_obj(beacon)
                grid[row][col].beacon()
                beacons.append(beacon)
            
            if toggle_gold and gold is None:
              toggle_gold = False
              gold = GameObj(row, col, "gold")
              grid[row][col].set_obj(gold)
              grid[row][col].gold()       
        
      if event.type == pygame.KEYDOWN:
        x, y = miner.get_pos()
        if active_input:
          if event.key == pygame.K_BACKSPACE:
            input_text = input_text[:-1]
          else:
            if event.unicode >= '0' and event.unicode <= '9':
              input_text+=event.unicode
              print(input_text)

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

        if event.key == pygame.K_g: # toggle gold
          toggle_pit = False
          toggle_gold = not toggle_gold
          toggle_beacon = False

        if event.key == pygame.K_b: # toggle beacon
          toggle_pit = False
          toggle_gold = False
          toggle_beacon = not toggle_beacon

  pygame.quit()



main(WIN, 8)
