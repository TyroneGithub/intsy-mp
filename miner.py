import pygame
import math
from queue import PriorityQueue
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
      # print(color)
      rect = pygame.draw.rect(win, color, [(margin + width) * column + margin,
                    (margin + width) * row + margin,width,width])
      if grid[row][column].is_miner():
        image = pygame.image.load('arrow.png').convert()
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
  # grid[row][col].set_obj(miner)
  grid[row][col].miner()
  grid[row][col].init_front(grid)

  # grid[row][col].update_neighbors(grid)

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
    # print(x, y, 'prev')
    # print(row, col, 'new')  
    # if 
    # front = grid[x][y].get_front()
    grid[x][y].reset()
    miner.update_pos(row, col)
    grid[row][col].scan(grid, ROWS)
    # print(grid[row][col].get_neighbors())
    # grid[row][col].front = front
    # grid[row][col].front_pos = grid[x][y].get_front_pos()
    # grid[row][col].scan(grid, lambda: draw_grid(width,ROWS, 1, grid, win))
    # draw_grid(width, rows, 1, grid, win)
    # grid[row][col].update_front(grid)
    grid[row][col].miner()
  else:
    # print('fail')
    miner.update_pos(x, y)
    grid[x][y].miner()
    return



def search_gold(grid, rows):
  for row in range(rows):
    for col in range(rows):
      if grid[row][col].is_gold() is not None:
        return True
  return False


def random_move(miner, grid, win, rows, width):
  x, y = miner.get_pos()
  run = False
  ctr= 0
  random.seed(datetime.now())
  if search_gold(grid, rows):
    run = True
    while run:
      num = random.randint(1, 4)
      if num == 1:
        x = x + 1 if x < rows else x - 1
      elif num == 2:
        x = x - 1 if x >= 0 else x + 1
      elif num == 3:
        y =y + 1 if y < rows else y - 1
      elif num == 4:
        y = y - 1 if y >= 0 else y + 1
      move(miner,grid, x, y, win, rows, width)    
      draw_grid(width, rows, 1, grid, win)
      pygame.display.flip()
      ctr+=1
      print(ctr)
      if check(grid, x, y, rows) == 'gold' or check(grid, x, y, rows) == 'pit':
        break
      pygame.time.delay(100)

    
    # print('h')



def main(win, num_rows):
  ROWS = int(num_rows)
  grid = init_grid(ROWS)
  width = 1000 // (ROWS * 2)
  # print(len(grid), len(grid[0]))
  margin = 1
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
  area = pygame.Rect(0, 0, 1030//2, 515)

  texts = ['[F] to toggle Pit ', '[B] to toggle Beacon', '[G] to toggle Gold']
  font = pygame.font.SysFont('Arial', 18)
  button_text, button_rect = GUI.text_setup('Random',font, 635, 250, WHITE) 
  move_ctr, move_ctr_rect = GUI.text_setup('Moves: ', font, 575, 220, BLACK)

  while run:
    pit_color = RED if toggle_pit else BLACK
    gold_color = GREEN if toggle_gold else BLACK
    beacon_color = TURQUOISE if toggle_beacon else BLACK
    
    colors = [pit_color, beacon_color, gold_color]

    text, rect = GUI.text_list_setup(texts, font, colors)


    for event in pygame.event.get():
      win.fill(WHITE)
      pygame.draw.rect(win, BLACK, area)
      draw_grid(width, ROWS, margin, grid, win)

      butt_container = button_rect
      butt_container.width = 120
      butt_container.height = 40
      butt_container.center = (600, 150)
      pygame.draw.rect(win, BLUE, butt_container)

      GUI.render_text(text, rect, win)
      GUI.render_text([move_ctr], [move_ctr_rect], win)
      win.blit(button_text, (565,140))

      pygame.display.flip()

      if event.type == pygame.QUIT:
        run = False

      # if toggle_pit:
      #   toggle_pit = False
      #   random_move(miner, grid, win, ROWS, width, lambda: draw_grid(width, ROWS, margin, grid, win))

      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if event.button == 1 and butt_container.collidepoint(pos):
          random_move(miner, grid, win, ROWS, width)
        if event.button == 1 and area.collidepoint(pos):
          row, col = get_clicked_pos(pos, width, margin)
          # print(row, col)
          if not (toggle_pit or toggle_beacon or toggle_gold):
            x, y = miner.get_pos()
            grid[x][y].rotate_front(grid)

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
            gold = GameObj(row, col, "gold")
            grid[row][col].set_obj(gold)
            grid[row][col].gold()       
        
        if event.button == 1:
          pass
            
      
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
     





  pygame.quit()


main(WIN, 8)
