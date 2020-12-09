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
  def text_list_setup(texts, font, colors):
    text_list = []
    text_rect_list = []
    x = 90
    for i in range(len(texts)):
      text_obj = font.render(texts[i], False, colors[i])
      text_rect = text_obj.get_rect()
      text_rect.center = (x, 600)
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


