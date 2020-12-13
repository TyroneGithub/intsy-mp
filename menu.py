import pygame
from miner import main
WIDTH = 400
pygame.display.set_caption("Gold Miner")

WHITE = (255, 255, 255)

# win.fill(WHITE)
def menu():
  window = pygame.display.set_mode((WIDTH, WIDTH))
  # window.fill(WHITE)
  # pygame.display.update()

  run = True
  text=''
  input_box = pygame.Rect(120, 150, 140, 32)
  font = pygame.font.Font(None, 32)
  color_inactive = pygame.Color('lightskyblue3')
  color_active = pygame.Color('dodgerblue2')
  color = color_inactive
  active = False
  while run:
    
    for event in pygame.event.get():
      
      if event.type == pygame.QUIT:
        run = False
      
      if event.type == pygame.MOUSEBUTTONDOWN:
          # If the user clicked on the input_box rect.
          if input_box.collidepoint(event.pos):
              # Toggle the active variable.
              active = not active
          else:
              active = False
          color = color_active if active else color_inactive

      if event.type == pygame.KEYDOWN:
        # print('x')
        if event.key == pygame.K_RETURN:
          print(text)
          main(window, WIDTH)
          # miner.main()
        elif event.key == pygame.K_BACKSPACE:
          text = text[:-1]
        else:
          text+=event.unicode

    window.fill(WHITE)
    txt_surface = font.render(text, True, color)
    window.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(window, color, input_box, 2)
    pygame.display.flip()


  pygame.quit()

if __name__ == '__main__':
  pygame.init()
  menu()