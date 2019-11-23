#!/usr/bin/python3
import random
import pygame
from time import sleep
from bomb_network import BombServer

INITIALISING = 0
ACTIVE = 1
DEFUSED = 2
EXPLODED = 3
bomb_server = BombServer('127.0.0.1')

disarmed = False
registered = False
layers = 4

pygame.init()

display_width = 320
display_height = 480

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

overdraw = ''

gameDisplay = pygame.display.set_mode((display_width, display_height))
#gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)

#pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

info_text = pygame.font.Font('./fonts/c800.ttf', 30)
button_text = pygame.font.Font('./fonts/c800.ttf', 20)

button = pygame.image.load('./images/button.png')
screen = pygame.image.load('./images/screen.png')
wrong = pygame.image.load('./images/wrong.png')
correct = pygame.image.load('./images/correct.png')

background = pygame.image.load('./images/whobg.jpg')
bg_width, bg_height = background.get_rect().size
wrong = pygame.image.load('./images/wrong.png')
correct = pygame.image.load('./images/correct.png')
tilex = display_width // bg_width + 1
tiley = display_height // bg_height + 1

display_words = {'YES':3, 'FIRST':2, 'DISPLAY':6, 'OKAY':2, 'SAYS':6, 'NOTHING':3, '':5, 'BLANK':4, 'NO':6, 'LED':3, 'LEAD':6, 'READ':4, 'RED':4, 'REED':5, 'LEED':5, 'HOLD ON':6, 'YOU':4, 'YOU ARE':6, 'YOUR':4, "YOU'RE":4, 'UR':1, 'THERE':6, "THEY'RE":5, 'THEIR':4, 'THEY ARE':3, 'SEE':6, 'C':2, 'CEE':6}

button_words = {
  'READY':'YES, OKAY, WHAT, MIDDLE, LEFT, PRESS, RIGHT, BLANK, READY, NO, FIRST, UHHH, NOTHING, WAIT,',
  'FIRST':'LEFT, OKAY, YES, MIDDLE, NO, RIGHT, NOTHING, UHHH, WAIT, READY, BLANK, WHAT, PRESS, FIRST,',
  'NO':'BLANK, UHHH, WAIT, FIRST, WHAT, READY, RIGHT, YES, NOTHING, LEFT, PRESS, OKAY, NO, MIDDLE,',
  'BLANK':'WAIT, RIGHT, OKAY, MIDDLE, BLANK, PRESS, READY, NOTHING, NO, WHAT, LEFT, UHHH, YES, FIRST,',
  'NOTHING':'UHHH, RIGHT, OKAY, MIDDLE, YES, BLANK, NO, PRESS, LEFT, WHAT, WAIT, FIRST, NOTHING, READY,',
  'YES':'OKAY, RIGHT, UHHH, MIDDLE, FIRST, WHAT, PRESS, READY, NOTHING, YES, LEFT, BLANK, NO, WAIT,',
  'WHAT':'UHHH, WHAT, LEFT, NOTHING, READY, BLANK, MIDDLE, NO, OKAY, FIRST, WAIT, YES, PRESS, RIGHT,',
  'UHHH':'READY, NOTHING, LEFT, WHAT, OKAY, YES, RIGHT, NO, PRESS, BLANK, UHHH, MIDDLE, WAIT, FIRST,',
  'LEFT':'RIGHT, LEFT, FIRST, NO, MIDDLE, YES, BLANK, WHAT, UHHH, WAIT, PRESS, READY, OKAY, NOTHING,',
  'RIGHT':'YES, NOTHING, READY, PRESS, NO, WAIT, WHAT, RIGHT, MIDDLE, LEFT, UHHH, BLANK, OKAY, FIRST,',
  'MIDDLE':'BLANK, READY, OKAY, WHAT, NOTHING, PRESS, NO, WAIT, LEFT, MIDDLE, RIGHT, FIRST, UHHH, YES,',
  'OKAY':'MIDDLE, NO, FIRST, YES, UHHH, NOTHING, WAIT, OKAY, LEFT, READY, BLANK, PRESS, WHAT, RIGHT,',
   'WAIT':'UHHH, NO, BLANK, OKAY, YES, LEFT, FIRST, PRESS, WHAT, WAIT, NOTHING, READY, RIGHT, MIDDLE,',
  'PRESS':'RIGHT, MIDDLE, YES, READY, PRESS, OKAY, NOTHING, UHHH, BLANK, LEFT, FIRST, WHAT, NO, WAIT,',
  'YOU':"SURE, YOU ARE, YOUR, YOU'RE, NEXT, UH HUH, UR, HOLD, WHAT?, YOU, UH UH, LIKE, DONE, U,",
  'YOU ARE':"YOUR, NEXT, LIKE, UH HUH, WHAT?, DONE, UH UH, HOLD, YOU, U, YOU'RE, SURE, UR, YOU ARE,",
  'YOUR':"UH UH, YOU ARE, UH HUH, YOUR, NEXT, UR, SURE, U, YOU'RE, YOU, WHAT?, HOLD, LIKE, DONE,",
  "YOU'RE":"YOU, YOU'RE, UR, NEXT, UH UH, YOU ARE, U, YOUR, WHAT?, UH HUH, SURE, DONE, LIKE, HOLD,",
  'UR':"DONE, U, UR, UH HUH, WHAT?, SURE, YOUR, HOLD, YOU'RE, LIKE, NEXT, UH UH, YOU ARE, YOU,",
  'U':"UH HUH, SURE, NEXT, WHAT?, YOU'RE, UR, UH UH, DONE, U, YOU, LIKE, HOLD, YOU ARE, YOUR,",
  'UH HUH':"UH HUH, YOUR, YOU ARE, YOU, DONE, HOLD, UH UH, NEXT, SURE, LIKE, YOU'RE, UR, U, WHAT?,",
  'UH UH':"UR, U, YOU ARE, YOU'RE, NEXT, UH UH, DONE, YOU, UH HUH, LIKE, YOUR, SURE, HOLD, WHAT?,",
  'WHAT?':"YOU, HOLD, YOU'RE, YOUR, U, DONE, UH UH, LIKE, YOU ARE, UH HUH, UR, NEXT, WHAT?, SURE,",
  'DONE':"SURE, UH HUH, NEXT, WHAT?, YOUR, UR, YOU'RE, HOLD, LIKE, YOU, U, YOU ARE, UH UH, DONE,",
  'NEXT':"WHAT?, UH HUH, UH UH, YOUR, HOLD, SURE, NEXT, LIKE, DONE, YOU ARE, UR, YOU'RE, U, YOU,",
  'HOLD':"YOU ARE, U, DONE, UH UH, YOU, UR, SURE, WHAT?, YOU'RE, NEXT, HOLD, UH HUH, YOUR, LIKE,",
  'SURE':"YOU ARE, DONE, LIKE, YOU'RE, YOU, HOLD, UH HUH, UR, SURE, U, WHAT?, NEXT, YOUR, UH UH,",
  'LIKE':"YOU'RE, NEXT, U, UR, HOLD, DONE, UH UH, WHAT?, UH HUH, YOU, LIKE, SURE, YOU ARE, YOUR,"
}

buttons = []
screen_text = ''
correct_button = ''

def do_thing(button_pressed):
  global buttons
  global screen_text
  global correct_button
  global timer
  global overdraw
  global layers
  if button_pressed:
    print(f'You pressed: {button_pressed}')
    print(f'Correct choice: {correct_button}')
    if button_pressed == correct_button:
      print('CORRECT!')
      overdraw = 'O'
      layers -= 1
    else:
      print('WRONG!')
      overdraw = 'X'
      bomb_server.strike()
    timer = 2
  buttons = random.sample(list(button_words), 6)
  screen_text = random.choice(list(display_words))
  look = buttons[display_words[screen_text]-1]
  press = button_words[look]
  best_index = 99
  for needle in buttons:
    location = press.find(needle + ',')
    #print(f'{needle} is located {location}')
    if location != -1 and location < best_index:
      correct_button = needle
      best_index = location

  print(f'look at: {look}')
  print(f'list is: {press}')
  print(f'push   : {correct_button}')

do_thing(None)
button_press = 0

def quitgame():
  pygame.quit()
  exit()

def text_objects(text, font, colour, background=None):
  textSurface = font.render(text, True, colour, background)
  return textSurface, textSurface.get_rect()

def info_lcd(text):
  TextSurf, TextRect = text_objects(text, info_text, white)
  TextRect.left = 10
  TextRect.top = 10
  gameDisplay.blit(TextSurf, TextRect)

lm = 20
tm = 20
mm = 20

gap = 35

bh = 80
bw = 125

def place_button(msg, x, y):
  w = 125
  h = 80
  global button_press
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()
  if x + w > mouse[0] > x and y + h > mouse[1] > y:
    if click[0] == 1 and msg != None:
      button_press = msg

  pygame.draw.rect(gameDisplay, white, (x,y,w,h), 0)
  textSurf, textRect = text_objects(msg, button_text, black)
  textRect.center = ((x + (w / 2)), (y + (h / 2)))
  gameDisplay.blit(button, (x, y))
  gameDisplay.blit(textSurf, textRect)

def place_screen(msg):
  x = lm
  y = tm
  w = 280
  h = 100
  textSurf, textRect = text_objects(msg, info_text, white)
  textRect.center = ((x + (w / 2)), (y + (h / 2)))
  gameDisplay.blit(screen, (x, y))
  gameDisplay.blit(textSurf, textRect)

def draw_background():
  gameDisplay.fill(black)
  for i in range(0, tiley):
    for j in range(0,tilex):
      gameDisplay.blit(background, (j*bg_width,i*bg_height))

pygame.time.set_timer(pygame.USEREVENT, 1000)
timer = 0

#TODO: This absolutely hammers the server with requests - put a 1-3 second delay in?
while True:
  registered = bomb_server.register()
  status = bomb_server.get_status()
  if registered and status == INITIALISING and disarmed:
    disarmed = False
  if registered and status == ACTIVE and not disarmed:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          quitgame()
      if event.type == pygame.QUIT:
        quitgame()
      if event.type == pygame.MOUSEBUTTONUP:
        if button_press != 0:
          do_thing(button_press)
          button_press = 0
      if event.type == pygame.USEREVENT:
        if timer <= 0:
          overdraw = ''
        else:
          timer -= 1

    draw_background()

    place_screen(screen_text)
    last_y = 130
    b = 0
    for i in range(1,4):
      place_button(buttons[b], lm, last_y+tm)
      place_button(buttons[b+1], lm+125+30, last_y+tm)
      b += 2
      last_y += 110

    if overdraw:
      draw_background()
      if overdraw == 'X':
        gameDisplay.blit(wrong, (0,0))
      elif overdraw == 'O':
        gameDisplay.blit(correct, (0,0))
    if layers <= 0:
      disarmed = True
      layers = 4
      bomb_server.disarm()

  else:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          quitgame()
      if event.type == pygame.QUIT:
        quitgame()
    draw_background()
  pygame.display.update()
