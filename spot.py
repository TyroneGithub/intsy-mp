import pygame

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


class Spot:
  def __init__(self, row, col, total_rows, game_obj):
    self.row = row
    self.col = col
    # self.x = row * width
    # self.y = col * width
    self.color = WHITE
    self.neighbors = []
    # self.width = width
    self.total_rows = total_rows
    self.front = None
    self.front_pos = None
    self.game_obj = game_obj

  def get_pos(self):
    return self.row, self.col

  def is_pit(self):
    return self.game_obj.get_type()
    # return self.color == RED

  def is_gold(self):
    return self.color == GREEN

  def is_miner(self):
    return self.color == ORANGE

  def is_beacon(self):
    return self.color == TURQUOISE

  def is_neighbor(self):
    return self.color == BLACK

  def reset(self):
    self.color = WHITE

  def miner(self):
    self.color = ORANGE

  def pit(self):
    self.color = RED

  def gold(self):
    self.color = GREEN

  def beacon(self):
    self.color = TURQUOISE

  def neighbor(self):
    self.color = BLACK

  def get_front(self):
    return self.front
  
  def get_front_pos(self):
    return self.front_pos 

  def get_obj(self):
    return self.game_obj
  
  def get_color(self):
    return self.color

  def set_obj(self, game_obj):
    self.game_obj = game_obj

  # def draw(self, win):
  #   pygame.draw.rect(win, self.color,(self.x, self.y, self.width, self.width))

  def update_neighbors(self, grid):
    self.neighbors = []
    if (self.row < self.total_rows - 1
        and not grid[self.row + 1][self.col].is_miner()):  # DOWN

      self.neighbors.append(grid[self.row + 1][self.col])
      grid[self.row + 1][self.col].neighbor()

    if self.row > 0 and not grid[self.row - 1][self.col].is_miner():  # UP

      self.neighbors.append(grid[self.row - 1][self.col])
      grid[self.row - 1][self.col].neighbor()

    if (self.col < self.total_rows - 1
            and not grid[self.row][self.col + 1].is_miner()):  # RIGHT

      self.neighbors.append(grid[self.row][self.col + 1])
      grid[self.row][self.col + 1].neighbor()

    if self.col > 0 and not grid[self.row][self.col -1].is_miner():  # LEFT

      self.neighbors.append(grid[self.row][self.col - 1])
      grid[self.row][self.col - 1].neighbor()

  def reset_neighbors(self):
    for neighbor in self.neighbors:
        neighbor.reset()

  def init_front(self, grid):
    self.front = grid[self.row][self.col + 1]
    self.front_pos = 'right'
    print(self.front_pos)
    self.front.neighbor()

  def rotate_front(self, grid):
    front_row, front_col = self.front.get_pos()
    self.neighbors = []
    try:
      if self.col < self.total_rows - 1 and self.front_pos=='right':

        self.front.reset()
        self.front = self.bottom_front(grid)
        self.front_pos = 'bottom'
        self.front.neighbor()
        self.neighbors.append(self.bottom_front(grid))

      elif self.col > 0 and self.front_pos=='left':

        self.front.reset()
        self.front = self.top_front(grid)
        self.front_pos = 'top'
        self.front.neighbor()
        self.neighbors.append(self.top_front(grid))

      elif self.row < self.total_rows - 1 and self.front_pos=='bottom':

        self.front.reset()
        self.front = self.left_front(grid)
        self.front_pos = 'left'
        self.front.neighbor()
        self.neighbors.append(self.left_front(grid))

      elif self.row > 0 and self.front_pos=='top':
        self.front.reset()
        self.front = self.right_front(grid)
        self.front_pos = 'right'
        self.front.neighbor()
        self.neighbors.append(self.right_front(grid))


    except IndexError:
        print("index error bitch")

  def update_front(self, grid):
    self.front.reset()
    front_x, front_y = self.front.get_pos()
    if (self.col >= self.total_rows - 1 and self.front_pos=='right'):
      self.front = self.bottom_front(grid)
    elif (self.row == 0 and front_y == 0 and self.front_pos == 'top'):
      self.front= self.right_front(grid)
    elif (self.col == 0 and self.front_pos == 'left'):
      self.front = self.bottom_front(grid)
    elif (self.row >= self.total_rows - 1 and self.front_pos == 'bottom'):
      self.front = self.right_front(grid)
    else:
      x, y = self.front.get_pos()
      if self.front_pos == 'right':
        self.front = self.right_front(grid)
      elif self.front_pos == 'left':
        self.front = self.left_front(grid)

      elif self.front_pos == 'bottom' :
        self.front = self.bottom_front(grid)

      elif self.front_pos == 'top' :
        self.front = self.top_front(grid)      

    self.front.neighbor()
  
  def left_front(self,grid):
    return grid[self.row][self.col - 1]

  def right_front(self,grid):
    return grid[self.row][self.col + 1]

  def bottom_front(self, grid):
    return grid[self.row + 1][self.col]

  def top_front(self, grid):
    return grid[self.row - 1][self.col]

  def scan(self, grid, draw):
    # self.rotate_front(grid)
    # self.rotate_front(grid)
    for i in range(4):
      self.rotate_front(grid)
      grid[self.row][self.col].miner()
      draw()
      pygame.time.delay(300)
      # print("h")
      

