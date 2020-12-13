import pygame
import math
from spot import Spot
import random

pygame.init()
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


class GUI:

  @staticmethod
  def text_list_setup(texts, font, colors, x, y):
    text_list = []
    text_rect_list = []
    # x = 90
    for i in range(len(texts)):
      text_obj = font.render(texts[i], False, colors[i])
      text_rect = text_obj.get_rect()
      text_rect.center = (x, y)
      x += 175
      text_list.append(text_obj)
      text_rect_list.append(text_rect)
    
    return text_list, text_rect_list

  @staticmethod
  def text_setup(word, font, x, y, color):
    text = font.render(word, False, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    # text_rect.width = 500
    
    return text, text_rect


  @staticmethod
  def render_text(texts, text_rects, win):

    for i in range(len(texts)):
      win.blit(texts[i], text_rects[i])

  @staticmethod
  def input_box(font, win, text):
    box = pygame.Rect(550, 10, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    # text=''
    # if event.type == pygame.MOUSEBUTTONDOWN:
    #   # If the user clicked on the input_box rect.
    #   if box.collidepoint(event.pos):
    #       # Toggle the active variable.
    #       active = not active
    #   else:
    #       active = False
    #   color = color_active if active else color_inactive
    # if event.type == pygame.KEYDOWN:
    #   if event.key == pygame.K_BACKSPACE:
    #       text = text[:-1]
    #   else:
    #     if event.unicode >= '0' and event.unicode <= '9':
    #       text+=event.unicode
    # text = "".join(text)
    txt_surface = font.render(text, True, BLACK)
    box_pos = (box.x+5, box.y+5)
    return txt_surface, box_pos, box
    # win.blit(txt_surface, (box.x+700, box.y+5))
    # pygame.draw.rect(win, color, box, 2)
    




