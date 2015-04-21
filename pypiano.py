#! /usr/bin/env python2

import sys
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class View(object):
  def __init__(self, size):
    self.size = size

    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 40)

    self.screen = pygame.Surface(self.size)

  def render(self):
    return self.screen

  def render_keyboard_overlay(self, kb):
    return

  def handle_event(self, event):
    return

class ScrollWidget(object):
  def __init__(self, size):
    self.size = size

    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 40)

    self.screen = pygame.Surface(size)

    self.items = []
    self.dirty = False
    self.scroll_inc = 0
    self.scroll_y = 0

  def add(self, title):
    text = self.font.render(title, True, WHITE)
    size = self.font.size(title)
    self.items.append([text, size])
    self.dirty = True
    if self.scroll_y == 0: self.scroll_y = size[1]

  def render(self):
    if self.dirty:
      self.screen.fill(BLACK)

      pygame.draw.rect(self.screen, WHITE, (0, 0, self.size[0], self.size[1]), 1)

      vert = 0

      for x in self.items:
        self.screen.blit(x[0], (0, vert-self.scroll_y*self.scroll_inc)) 
        vert += x[1][1]
      
      self.dirty = False

    return self.screen

  def scroll_up(self):
    self.scroll_inc += 1
    if self.scroll_inc > len(self.items)-3: self.scroll_inc = len(self.items)-3
    self.dirty = True

  def scroll_down(self):
    self.scroll_inc -= 1
    if self.scroll_inc < 0: self.scroll_inc = 0
    self.dirty = True

class PlayView(View):
  def __init__(self, size):
    View.__init__(self, size)

    self.title = self.font.render("Song Select", True, WHITE);
    self.title_size = self.font.size("Song Select");

    self.up = self.font.render("Up", True, BLACK)
    self.up_size = self.font.size("Up")

    self.down = self.font.render("Down", True, BLACK)
    self.down_size = self.font.size("Down")

    self.select = self.font.render("Select", True, BLACK);
    self.select_size = self.font.size("Select")

    self.back = self.font.render("Back", True, BLACK)
    self.back_size = self.font.size("Back")

    self.dirty = True

    self.song_list = ScrollWidget((self.size[0]*0.8, self.size[1]*0.4))

    for x in range(10):
      self.song_list.add("Song " + str(x))

  def render(self):
    if self.dirty:
      self.screen.blit(self.title, ((self.size[0]-self.title_size[0])/2, self.size[1]*0.05))

      self.screen.blit(self.song_list.render(), (self.size[0]*0.1, self.size[1]*0.3))

      pygame.draw.circle(self.screen, WHITE, (int(self.size[0]*0.1) - 12, int(self.size[1]*0.3) + 10), 8)

      self.dirty = False

    return self.screen

  def render_keyboard_overlay(self, keyboard):
    keyboard.add_key_overlay(1, self.down, self.down_size)
    keyboard.add_key_overlay(0, self.up, self.up_size)
    keyboard.add_key_overlay(2, self.select, self.select_size)
    keyboard.add_key_overlay(3, self.back, self.back_size)

    return

  def handle_event(self, event):
    if event.key == pygame.K_w:
      self.song_list.scroll_up()
      self.dirty = True
    elif event.key == pygame.K_q:
      self.song_list.scroll_down()
      self.dirty = True

class LibraryView(View):
  def __init__(self, size):
    View.__init__(self, size)

    self.title_size = self.font.size("Library")
    self.title = self.font.render("Library", True, WHITE)

    self.dirty = True
  
  def render(self):
    if self.dirty:
      self.screen.fill(BLACK)

      self.screen.blit(self.title, ((self.size[0]-self.title_size[0])/2, 0))
    
      self.dirty = False

    return self.screen

class OptionsView(View):
  def __init__(self, size):
    View.__init__(self, size)

    self.title_size = self.font.size("Options")
    self.title = self.font.render("Options", True, WHITE)

    self.dirty = True

  def render(self):
    if self.dirty:
      self.screen.fill(BLACK)

      self.screen.blit(self.title, ((self.size[0]-self.title_size[0])/2, 0))
    
      self.dirty = False

    return self.screen

class MenuView(View):
  def __init__(self, size, event_handler):
    View.__init__(self, size)

    self.event_handler = event_handler
    self.vert = 0
    self.dirty = True
    self.init = False
    self.menus = []

  def add(self, title, view):
    text = self.font.render(title, True, WHITE)
    text_size = self.font.size(title)
    text_pos = (0, self.vert)
    self.vert += text_size[1]
    self.menus.append([text, text_size, text_pos, view])

  def init_layout(self):
    return

  def update_layout(self):
    return
  
  def render(self):
    if not self.init:
      self.init_layout()
      self.init = True

    if self.dirty:
      self.update_layout()
      self.screen.fill(BLACK)
      for x in self.menus:
        self.screen.blit(x[0], x[2])
      self.dirty = False

    return self.screen

class VertMenuView(MenuView):
  def __init__(self, size, event_handler):
    MenuView.__init__(self, size, event_handler)

    self.sel = 0

  def init_layout(self):
    max_width = 0

    for x in self.menus:
      if x[1][0] > max_width: max_width = x[1][0]

    for x in self.menus:
      pos = ((self.size[0]-max_width)/2, 20+x[2][1])
      x[2] = pos

  def render(self):
    self.dirty = True

    MenuView.render(self)

    menu = self.menus[self.sel]

    pygame.draw.circle(self.screen, WHITE, (menu[2][0]-12, menu[2][1]+12), 10)
  
    return self.screen

  def handle_event(self, event):
    if event.key == pygame.K_w:
      self.sel += 1
      if self.sel > len(self.menus)-1: self.sel = len(self.menus)-1
      self.dirty = True
    elif event.key == pygame.K_q:
      self.sel -= 1
      if self.sel < 0: self.sel = 0
      self.dirty = True
    elif event.key == pygame.K_e:
      self.event_handler(self.menus[self.sel][3])

class HorizMenuView(MenuView):
  def __init__(self, size, event_handler, key_width):
    MenuView.__init__(self, size, event_handler)

    self.key_width = key_width

  def init_layout(self):
    max_height = 0
    
    for x in self.menus:
      if x[1][0] > max_height: max_height = x[1][0]

    for x in range(len(self.menus)):
      menu = self.menus[x]
      menu[0] = pygame.transform.rotate(menu[0], 90)
      menu[2] = (x*self.key_width+self.key_width-menu[1][1], self.size[1]-menu[1][0]-20)

  def handle_event(self, event):
    if event.key == pygame.K_q:
      self.event_handler(self.menus[0][3])
    elif event.key == pygame.K_w:
      self.event_handler(self.menus[1][3])
    elif event.key == pygame.K_e:
      self.event_handler(self.menus[2][3])

class Keyboard:
  def __init__(self):
    self.w_width = 40
    self.w_height = 200
    self.w_keys = []
  
    self.b_width = 30
    self.b_height = 100
    self.b_keys = []

    self.spacing = 2
    self.dirty = False

    self.size = (7*self.w_width+6*self.spacing, self.w_height)

    self.screen = pygame.Surface(self.size)

    self.overlays = []

    offset = self.w_width+self.spacing

    for x in range(7):
      pos = (x*offset, 0, self.w_width, self.w_height)
      pygame.draw.rect(self.screen, WHITE, pos)
      self.w_keys.append([pos])

    for x in range(6):
      if x == 2: continue
      pos = (offset+x*offset-self.b_width/2, 0, self.b_width, self.b_height)
      pygame.draw.rect(self.screen, BLACK, pos) 
      self.b_keys.append([pos])

  def add_key_overlay(self, index, text, size):
    text = pygame.transform.rotate(text, 90)

    loffset = (self.w_width - size[1]) / 2

    offset = (index * self.w_width + (index - 1) * self.spacing + loffset, self.size[1]-size[0])

    self.overlays.append([text, offset])

    self.dirty = True

  def clear_key_overlays(self):
    for x in self.overlays:
      del x

  def render(self):
    if self.dirty:
      self.screen.fill(BLACK)

      for x in self.w_keys:
        pygame.draw.rect(self.screen, WHITE, x[0])

      for x in self.b_keys:
        pygame.draw.rect(self.screen, BLACK, x[0])  

      for overlay in self.overlays:
        self.screen.blit(overlay[0], overlay[1])

      self.dirty = False

    return self.screen

class pyPiano:
  def run(self):
    pygame.init()
    pygame.display.init()

    kb = Keyboard()

    play_view = PlayView(kb.size)
    lib_view = LibraryView(kb.size)
    option_view = OptionsView(kb.size)

    horiz_menu = HorizMenuView(kb.size, self.event_handler, kb.w_width)

    horiz_menu.add("Play", play_view)
    horiz_menu.add("Library", lib_view)
    horiz_menu.add("Options", option_view)

    vert_menu = VertMenuView(kb.size, self.event_handler)

    vert_menu.add("Play", play_view)
    vert_menu.add("Library", lib_view)
    vert_menu.add("Options", option_view)

    self.view = horiz_menu
    self.last_view = None

    size = (kb.size[0], kb.size[1]*2)

    screen = pygame.display.set_mode(size)    

    clock = pygame.time.Clock()

    while 1:
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            sys.exit(1)
          elif event.key == pygame.K_z:
            if self.view == horiz_menu:
              self.view = vert_menu
            else:
              self.view = horiz_menu
          else:
            self.view.handle_event(event)

      screen.fill(BLACK)

      view_screen = self.view.render()

      screen.blit(view_screen, (0, 0))  

      if self.view != self.last_view:
        kb.clear_key_overlays()

        self.view.render_keyboard_overlay(kb);

        self.last_view = self.view

      kb_screen = kb.render()

      screen.blit(kb_screen, (0, kb_screen.get_height()))

      pygame.display.flip() 

      clock.tick(30)

  def event_handler(self, screen):
    self.view = screen

piano = pyPiano()
piano.run()
