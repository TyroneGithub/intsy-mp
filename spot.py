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
BACKGROUND = (28, 24, 20)


class Spot:
  def __init__(self, row, col, total_rows, game_obj):
    self.row = row
    self.col = col
    # self.x = row * width
    # self.y = col * width
    self.neighbors = []
    # self.width = width
    self.total_rows = total_rows
    self.front = None
    self.front_pos = 'right'
    self.game_obj = game_obj
    self.color = self.init_color()
    self.visited_times = 0
    self.visits = []

  def init_color(self):
    if self.game_obj is not None:
      if self.is_pit():
        return RED

      elif self.is_beacon():
        return TURQUOISE

      elif self.is_gold():
        return GREEN

      elif self.is_front():
        return BLACK
      
      elif self.is_visited():
        return GREY
      
    return BACKGROUND
      
      
      # elif self.game_obj

  def get_pos(self):
    return self.row, self.col

  def is_pit(self):
    return self.game_obj.get_type() == "pit" if self.game_obj is not None else None

  def is_gold(self):
    return self.game_obj.get_type() == "gold" if self.game_obj is not None else None

  def is_miner(self):
    return self.color == ORANGE

  def is_beacon(self):
    return self.game_obj.get_type() == "beacon" if self.game_obj is not None else None

  def is_front(self):
    return self.game_obj.get_type() == "front" if self.game_obj is not None else None

  def is_visited(self):
    return self.game_obj.get_type() == "visited" if self.game_obj is not None else None

  def reset(self):
    self.color = WHITE if self.game_obj is None else self.init_color()

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


  def init_front(self, grid):
    self.front_pos = 'left'
  
  def get_visit_num(self):
    return self.visited_times

  def scan_direction(self, grid, num_rows):
    #top
    # top = []
    self.neighbors = []
    self.visits = []
    n_row = 0
    n_col = 0
    for row in range(num_rows):
      for col in range(num_rows):
    
        if self.front_pos == 'top' and self.row > row and self.col == col:
          self.neighbors.append(None if grid[row][col].get_obj() is 
                            None else grid[row][col].get_obj().get_type())
          if grid[row][col].is_visited():
            self.visits.append(grid[row][col].get_visit_num())
        elif self.front_pos == 'bottom' and self.row < row and self.col == col:
          self.neighbors.append(None if grid[row][col].get_obj() is 
                            None else grid[row][col].get_obj().get_type())
          if grid[row][col].is_visited():
            self.visits.append(grid[row][col].get_visit_num())
        if self.front_pos == 'right' and self.col < col and self.row == row:
          self.neighbors.append(None if grid[row][col].get_obj() is 
                            None else grid[row][col].get_obj().get_type())
          if grid[row][col].is_visited():
            self.visits.append(grid[row][col].get_visit_num())
        elif self.front_pos == 'left' and self.col > col and self.row == row:
          self.neighbors.append(None if grid[row][col].get_obj() is 
                            None else grid[row][col].get_obj().get_type())
          if grid[row][col].is_visited():
            self.visits.append(grid[row][col].get_visit_num())

    # self.neighbors = top
    if self.front_pos == 'top' or self.front_pos == 'left':
      self.neighbors.reverse()
      # print(self.neighbors, self.front_pos)

    
  def get_neighbors(self):
    return self.neighbors


  def rotate_front(self, grid):
    # front_row, front_col = self.front.get_pos()
    # self.neighbors = []
    try:
      if self.front_pos=='right':
        self.front_pos = 'bottom'
        # self.front.reset()
        # self.front = self.bottom_front(grid)
        # self.front_pos = 'bottom'
        # self.front.neighbor()
        # self.neighbors.append(self.bottom_front(grid))

      elif self.front_pos=='left':
        self.front_pos = 'top'

        # self.front.reset()
        # self.front = self.top_front(grid)
        # self.front_pos = 'top'
        # self.front.neighbor()
        # self.neighbors.append(self.top_front(grid))

      elif self.front_pos=='bottom':
        self.front_pos = 'left'

        # self.front.reset()
        # self.front = self.left_front(grid)
        # self.front_pos = 'left'
        # self.front.neighbor()
        # self.neighbors.append(self.left_front(grid))

      elif self.front_pos=='top':
        self.front_pos = 'right'
        
        # self.front.reset()
        # self.front = self.right_front(grid)
        # self.front_pos = 'right'
        # self.front.neighbor()
        # self.neighbors.append(self.right_front(grid))


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

  def increase_visit(self):
    self.visited_times -= 100

  def evaluate(self, points):
    directions = ['top', 'bottom', 'left', 'right']
    index = directions.index(self.front_pos)
    # iterate none none none
    ctr = 0 
    for neighbor in self.neighbors:
      if neighbor is None:
        points[index] += 10000
      if neighbor == 'gold':
        points[index] += 1000000000
        break
      if neighbor == 'pit' :
        points[index] -= 1000
        break
      if neighbor == 'beacon':
        points[index] += 10000000
        break
      if neighbor == 'visited':
        points[index] += sum(self.visits) 
        if None in self.neighbors:
          points[index] += 100        
        break

    # if 'visited' not in self.neighbors:
    #   points[index] += 100
    
    if not self.neighbors:
      points[index] = -1e9

    return points

  def scan(self, grid, num_rows, points):
    directions = ['top', 'bottom', 'left', 'right']

    for i in range(4):
      self.scan_direction(grid, num_rows)
      points = self.evaluate(points)
      self.rotate_front(grid)
      pygame.time.delay(50)
    return points
  
  def scan2(self, grid, num_rows):
    directions = ['top', 'bottom', 'left', 'right']
    items = [None, None, None, None]
    for i in range(4):
      item = None
      self.scan_direction(grid, num_rows)
      index = directions.index(self.front_pos)
      if 'pit' in self.neighbors:
        item = 'pit'
      elif 'beacon' in self.neighbors:
        item = 'beacon'
      elif 'gold' in self.neighbors:
        item = 'gold'
      elif 'visited' in self.neighbors:
        item = 'visited'
      if not self.neighbors:
        item = 'edge'

      items[index] = item

      self.rotate_front(grid)
      pygame.time.delay(50)

    return items