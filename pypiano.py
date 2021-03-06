#! /usr/bin/env python2

import sys
import pygame
import pygame.midi

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class View(object):
  def __init__(self, game, size, title = ""):
    self.size = size

    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 40)

    self.title_text = self.create_text(title, WHITE) 

    self.__screen = pygame.Surface(self.size)

    self.__dirty = False
    
    self.game = game;

    self.msg_text = self.create_text("", WHITE)

  def set_dirty(self):
    self.__dirty = True

  def clear_dirty(self):
    self.dirty = False

  def is_dirty(self):
    return self.__dirty

  def set_msg_text(self, msg):
    self.msg_text = self.create_text(msg, WHITE)

    self.set_dirty()

  def clear_msg_text(self):
    self.msg_text = self.create_text("", WHITE)

  def create_text(self, text, color = WHITE):
    text_surface = self.font.render(text, True, color)

    text_size = self.font.size(text)

    return [text_surface, text_size]

  def render(self):
    if self.__dirty:
      self.__screen.fill(BLACK)

      offset = ((self.size[0]-self.title_text[1][0])/2, self.size[1]*0.1)

      self.__screen.blit(self.title_text[0], offset) 

      offset = ((self.size[0]-self.msg_text[1][0])/2, self.size[1]*0.9-self.msg_text[1][1])

      self.__screen.blit(self.msg_text[0], offset)
    
    return self.__screen

  def render_keyboard_overlay(self, kb):
    return

  def handle_event(self, event):
    return

  def handle_midi_event(self, event):
    return

class ScrollWidget(object):
  def __init__(self, size):
    self.size = size

    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 30)

    self.screen = pygame.Surface(size)

    self.items = []
    self.__dirty = True
    self.scroll_inc = 0
    self.scroll_y = 0

  def add(self, title):
    text = self.font.render(title, True, WHITE)
    size = self.font.size(title)
    self.items.append([text, size])
    self.__dirty = True
    if self.scroll_y == 0: self.scroll_y = size[1]

  def render(self):
    if self.__dirty:
      self.screen.fill(BLACK)

      pygame.draw.rect(self.screen, WHITE, (0, 0, self.size[0], self.size[1]), 1)

      vert = 0

      for x in self.items:
        self.screen.blit(x[0], (0, vert-self.scroll_y*self.scroll_inc)) 
        vert += x[1][1]
      
      self.__dirty = False

    return self.screen

  def scroll_up(self):
    self.scroll_inc += 1
    if self.scroll_inc > len(self.items)-1: self.scroll_inc = len(self.items)-1
    self.__dirty = True

  def scroll_down(self):
    self.scroll_inc -= 1
    if self.scroll_inc < 0: self.scroll_inc = 0
    self.__dirty = True

class PlayView(View):
  def __init__(self, game, size):
    View.__init__(self, game, size, "Song Select")

    self.up_text = self.create_text("Up", BLACK)
    self.down_text = self.create_text("Down", BLACK)
    self.select_text = self.create_text("Select", BLACK)
    self.back_text = self.create_text("Back", BLACK)

    self.next_view = GameStyleView(game, size)

    self.song_list = ScrollWidget((self.size[0]*0.8, self.size[1]*0.4))

    for x in range(10):
      self.song_list.add("Song " + str(x))

  def render(self):
    screen = super(PlayView, self).render()

    if self.is_dirty():
      screen.blit(self.song_list.render(), (self.size[0]*0.1, self.size[1]*0.3))

      pygame.draw.circle(screen, WHITE, (int(self.size[0]*0.1) - 12, int(self.size[1]*0.3) + 10), 8)

    return screen

  def render_keyboard_overlay(self, kb):
    kb.add_key_overlay(0, self.up_text[0], self.up_text[1])
    kb.add_key_overlay(1, self.down_text[0], self.down_text[1])
    kb.add_key_overlay(2, self.select_text[0], self.select_text[1])
    kb.add_key_overlay(3, self.back_text[0], self.back_text[1])

  def handle_event(self, event):
    if event.key == pygame.K_w:
      self.song_list.scroll_up()
      self.set_dirty()
    elif event.key == pygame.K_q:
      self.song_list.scroll_down()
      self.set_dirty()
    elif event.key == pygame.K_e:
      self.game.change_view(self.next_view)
    elif event.key == pygame.K_r:
      self.game.previous_view()

  def handle_midi_event(self, event):
    if event[1] % 36 == 0:
      self.song_list.scroll_up()
      self.set_dirty()
    elif event[1] % 38 == 0:
      self.song_list.scroll_down()
      self.set_dirty()
    elif event[1] % 40 == 0:
      self.game.change_view(self.next_view)
    elif event[1] % 42 == 0:
      self.game.previous_view()

class GameStyleView(View):
  def __init__(self, game, size):
    View.__init__(self, game, size, "Game Style")

    self.up_text = self.create_text("Up", BLACK)
    self.down_text = self.create_text("Down", BLACK)
    self.select_text = self.create_text("Play", BLACK)
    self.back_text = self.create_text("Back", BLACK)

    self.style_list = ScrollWidget((self.size[0]*0.8, self.size[1]*0.4))

    self.style_list.add("Practice Melody")
    self.style_list.add("Practice Melody (Left Only)")
    self.style_list.add("Practice Melody (Right Only)")
    self.style_list.add("Practice Rhythm")
    self.style_list.add("Practice Rhythm (Left Only)")
    self.style_list.add("Practice Rhythm (Right Only)")
    self.style_list.add("Song Recital")
    self.style_list.add("Song Recital (Left Only)")
    self.style_list.add("Song Recital (Right Only)")

  def render(self):
    screen = super(GameStyleView, self).render()

    if self.is_dirty():
      screen.blit(self.style_list.render(), (self.size[0]*0.1, self.size[1]*0.3))

      pygame.draw.circle(screen, WHITE, (int(self.size[0]*0.1) - 12, int(self.size[1]*0.3) + 10), 8)

    return screen

  def render_keyboard_overlay(self, kb):
    kb.add_key_overlay(0, self.up_text[0], self.up_text[1])
    kb.add_key_overlay(1, self.down_text[0], self.down_text[1])
    kb.add_key_overlay(2, self.select_text[0], self.select_text[1])
    kb.add_key_overlay(3, self.back_text[0], self.back_text[1])

  def handle_event(self, event):
    if event.key == pygame.K_w:
      self.style_list.scroll_up()
      self.set_dirty()
    elif event.key == pygame.K_q:
      self.style_list.scroll_down()
      self.set_dirty() 
    elif event.key == pygame.K_e:
      self.set_msg_text("Play")
    elif event.key == pygame.K_r:
      self.game.previous_view()

  def handle_midi_event(self, event):
    if event[1] % 36 == 0:
      self.style_list.scroll_up()
      self.set_dirty()
    elif event[1] % 38 == 0:
      self.style_list.scroll_down()
      self.set_dirty() 
    elif event[1] % 40 == 0:
      self.set_msg_text("Play")
    elif event[1] % 42 == 0:
      self.game.previous_view()

class AudioView(View):
  def __init__(self, game, size):
    View.__init__(self, game, size, "Audio")

  def render(self):
    screen = super(AudioView, self).render()

    return screen

class LibraryView(View):
  def __init__(self, game, size):
    View.__init__(self, game, size, "Library")

    self.up_text = self.create_text("Up", BLACK)
    self.down_text = self.create_text("Down", BLACK)
    self.add_text = self.create_text("Add", BLACK)
    self.remove_text = self.create_text("Remove", BLACK)
    self.back_text = self.create_text("Back", BLACK)

    self.library_list = ScrollWidget((size[0]*0.8, size[1]*0.50))

    for x in range(10):
      self.library_list.add("Item " + str(x))

  def render_keyboard_overlay(self, kb):
    kb.add_key_overlay(0, self.up_text[0], self.up_text[1])
    kb.add_key_overlay(1, self.down_text[0], self.down_text[1])
    kb.add_key_overlay(2, self.add_text[0], self.add_text[1])
    kb.add_key_overlay(3, self.remove_text[0], self.remove_text[1])
    kb.add_key_overlay(4, self.back_text[0], self.back_text[1])
  
  def render(self):
    screen = super(LibraryView, self).render()

    if self.is_dirty():
      screen.blit(self.library_list.render(), (self.size[0]*0.1, self.size[1]*0.3)) 

      pygame.draw.circle(screen, WHITE, (int(self.size[0]*0.1)-12, int(self.size[1]*0.3)+8), 8)

    return screen

  def handle_event(self, event):
    if event.key == pygame.K_w:
      self.library_list.scroll_up()
      self.set_dirty()
    elif event.key == pygame.K_q:
      self.library_list.scroll_down()
      self.set_dirty()
    elif event.key == pygame.K_e:
      self.set_msg_text("Add song")
    elif event.key == pygame.K_r:
      self.set_msg_text("Remove song")
    elif event.key == pygame.K_t:
      self.game.previous_view()

  def handle_midi_event(self, event):
    if event[1] % 36 == 0:
      self.style_list.scroll_up()
      self.set_dirty()
    elif event[1] % 38 == 0:
      self.style_list.scroll_down()
      self.set_dirty() 
    elif event[1] % 40 == 0:
      self.set_msg_text("Add song")
    elif event[1] % 42 == 0:
      self.set_msg_text("Remove song")
    elif event[1] % 44 == 0:
      self.game.previous_view()

class UserProfilesView(View):
  def __init__(self, game, size):
    View.__init__(self, game, size, "User Profiles")

    self.up_text = self.create_text("Up", BLACK)
    self.down_text = self.create_text("Down", BLACK)
    self.add_text = self.create_text("Add", BLACK)
    self.remove_text = self.create_text("Remove", BLACK)
    self.back_text = self.create_text("Back", BLACK)

    self.profile_list = ScrollWidget((size[0]*0.8, size[1]*0.5))

    self.profile_list.add("Anonymous")

  def render_keyboard_overlay(self, kb):
    kb.add_key_overlay(0, self.up_text[0], self.up_text[1])
    kb.add_key_overlay(1, self.down_text[0], self.down_text[1])
    kb.add_key_overlay(2, self.add_text[0], self.add_text[1])
    kb.add_key_overlay(3, self.remove_text[0], self.remove_text[1])
    kb.add_key_overlay(4, self.back_text[0], self.back_text[1])

  def render(self):
    screen = super(UserProfilesView, self).render()

    if self.is_dirty():
      screen.blit(self.profile_list.render(), (self.size[0]*0.1, self.size[1]*0.3)) 

      pygame.draw.circle(screen, WHITE, (int(self.size[0]*0.1)-12, int(self.size[1]*0.3)+8), 8)

    return screen

  def handle_event(self, event):
    if event.key == pygame.K_q:
      self.profile_list.scroll_down()
      self.set_dirty()
    elif event.key == pygame.K_w:
      self.profile_list.scroll_up()
      self.set_dirty()
    elif event.key == pygame.K_e:
      self.set_msg_text("Add user profile")
    elif event.key == pygame.K_r:
      self.set_msg_text("Remove user profile")
    elif event.key == pygame.K_t:
      self.game.previous_view()

  def handle_midi_event(self, event):
    if event[1] % 36 == 0:
      self.style_list.scroll_up()
      self.set_dirty()
    elif event[1] % 38 == 0:
      self.style_list.scroll_down()
      self.set_dirty() 
    elif event[1] % 40 == 0:
      self.set_msg_text("Add user profile")
    elif event[1] % 42 == 0:
      self.set_msg_text("Remove user profile")
    elif event[1] % 44 == 0:
      self.game.previous_view()

class MenuView(View):
  def __init__(self, game, size):
    View.__init__(self, game, size, "")

    self.vert = 0
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

    screen = super(MenuView, self).render() 

    if self.is_dirty():
      self.update_layout()

      for x in self.menus:
        screen.blit(x[0], x[2])

    return screen

class OptionsView(MenuView):
  def __init__(self, game, size):
    MenuView.__init__(self, game, size)

    self.sel = 0

    self.up_text = self.create_text("Up", BLACK)
    self.down_text = self.create_text("Down", BLACK)
    self.select_text = self.create_text("Select", BLACK) 

    self.add("User Profiles", UserProfilesView(game, size))
    self.add("Audio", AudioView(game, size))

  def init_layout(self):
    max_width = 0

    for x in self.menus:
      if x[1][0] > max_width: max_width = x[1][0]

    for x in self.menus:
      pos = ((self.size[0]-max_width)/2, 20+x[2][1])
      x[2] = pos

  def render(self):
    screen = super(OptionsView, self).render()

    if self.is_dirty():
      if len(self.menus) > 0:
        menu = self.menus[self.sel]

        pygame.draw.circle(screen, WHITE, (menu[2][0]-12, menu[2][1]+12), 10)
      
    return screen

  def render_keyboard_overlay(self, kb):
    kb.add_key_overlay(0, self.up_text[0], self.up_text[1])
    kb.add_key_overlay(1, self.down_text[0], self.down_text[1])
    kb.add_key_overlay(2, self.select_text[0], self.select_text[1])

  def handle_event(self, event):
    if event.key == pygame.K_w:
      self.sel += 1
      if self.sel > len(self.menus)-1: self.sel = len(self.menus)-1
      self.set_dirty()
    elif event.key == pygame.K_q:
      self.sel -= 1
      if self.sel < 0: self.sel = 0
      self.set_dirty()
    elif event.key == pygame.K_e:
      self.game.change_view(self.menus[self.sel][3])

  def handle_midi_event(self, event):
    if event[1] % 36 == 0:
      self.sel += 1
      if self.sel > len(self.menus)-1: self.sel = len(self.menus)-1
      self.set_dirty()
    elif event[1] % 38 == 0:
      self.sel -= 1
      if self.sel < 0: self.sel = 0
      self.set_dirty()
    elif event[1] % 40 == 0:
      self.game.change_view(self.menus[self.sel][3])

class VertMenuView(MenuView):
  def __init__(self, game, size):
    MenuView.__init__(self, game, size)

    self.sel = 0
    
    self.up_text = self.create_text("Up", BLACK)
    self.down_text = self.create_text("Down", BLACK)
    self.select_text = self.create_text("Select", BLACK) 

    self.add("Play", PlayView(game, size)) 
    self.add("Library", LibraryView(game, size))
    self.add("Options", OptionsView(game, size))
    self.add("Quit", None)

  def init_layout(self):
    max_width = 0

    for x in self.menus:
      if x[1][0] > max_width: max_width = x[1][0]

    for x in self.menus:
      pos = ((self.size[0]-max_width)/2, 20+x[2][1])
      x[2] = pos

  def render(self):
    screen = super(VertMenuView, self).render()

    if self.is_dirty():
      if len(self.menus) > 0:
        menu = self.menus[self.sel]

        pygame.draw.circle(screen, WHITE, (menu[2][0]-12, menu[2][1]+12), 10)
      
    return screen

  def render_keyboard_overlay(self, kb):
    kb.add_key_overlay(0, self.up_text[0], self.up_text[1])
    kb.add_key_overlay(1, self.down_text[0], self.down_text[1])
    kb.add_key_overlay(2, self.select_text[0], self.select_text[1])

  def handle_event(self, event):
    if event.key == pygame.K_w:
      self.sel += 1
      if self.sel > len(self.menus)-1: self.sel = len(self.menus)-1
      self.set_dirty()
    elif event.key == pygame.K_q:
      self.sel -= 1
      if self.sel < 0: self.sel = 0
      self.set_dirty()
    elif event.key == pygame.K_e:
      if self.sel == 3:
        sys.exit(0)

      self.game.change_view(self.menus[self.sel][3])

  def handle_midi_event(self, event):
    if event[1] % 36 == 0:
      self.sel += 1
      if self.sel > len(self.menus)-1: self.sel = len(self.menus)-1
      self.set_dirty()
    elif event[1] % 38 == 0:
      self.sel -= 1
      if self.sel < 0: self.sel = 0
      self.set_dirty()
    elif event[1] % 40 == 0:
      if self.sel == 3:
        sys.exit(0)

      self.game.change_view(self.menus[self.sel][3])

class HorizMenuView(MenuView):
  def __init__(self, game, size, key_width):
    MenuView.__init__(self, game, size)

    self.key_width = key_width

    self.add("Play", PlayView(game, size)) 
    self.add("Library", LibraryView(game, size))
    self.add("Options", OptionsView(game, size))
    self.add("Quit", None)

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
      self.game.change_view(self.menus[0][3])
    elif event.key == pygame.K_w:
      self.game.change_view(self.menus[1][3])
    elif event.key == pygame.K_e:
      self.game.change_view(self.menus[2][3])
    elif event.key == pygame.K_r:
      sys.exit(1)

  def handle_midi_event(self, event):
    if event[1] % 36 == 0:
      self.game.change_view(self.menus[0][3])
    elif event[1] % 38 == 0:
      self.game.change_view(self.menus[1][3])
    elif event[1] % 40 == 0:
      self.game.change_view(self.menus[2][3])
    elif event[1] % 42 == 0:
      sys.exit(1)

class Keyboard:
  def __init__(self):
    self.w_width = 60
    self.w_height = 300
    self.w_keys = []
  
    self.b_width = 50
    self.b_height = 200
    self.b_keys = []

    self.spacing = 2
    self.__dirty = False

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

    self.__dirty = True

  def clear_key_overlays(self):
    del self.overlays[:]

    self.__dirty = True

  def render(self):
    if self.__dirty:
      self.screen.fill(BLACK)

      for x in self.w_keys:
        pygame.draw.rect(self.screen, WHITE, x[0])

      for x in self.b_keys:
        pygame.draw.rect(self.screen, BLACK, x[0])  

      for overlay in self.overlays:
        self.screen.blit(overlay[0], overlay[1])

      self.__dirty = False

    return self.screen

class pyPiano:
  def choose_midi_input(self):
    valid_devs = []

    for x in range(pygame.midi.get_count()):
      dev = pygame.midi.get_device_info(x)

      if dev[2] == 1:
        valid_devs.append([x, dev])        

    print('Select an input midi device.')

    for index, dev in enumerate(valid_devs):
      print(str(index+1) + ' - ' + dev[1][1]) 

    list_length = len(valid_devs)+1

    print(str(list_length) + ' - None')

    selection = int(raw_input('Enter selection: '))

    if selection >= list_length:
      return None
    else:
      return valid_devs[selection-1][0] 

  def run(self):
    pygame.init()
    pygame.midi.init()
    pygame.display.init()

    dev = self.choose_midi_input()

    kb_dev = None

    if dev != None:
      kb_dev = pygame.midi.Input(dev, 0)

    kb = Keyboard()

    horiz_menu = HorizMenuView(self, kb.size, kb.w_width)
    vert_menu = VertMenuView(self, kb.size)

    self.view = vert_menu

    self.view_stack = []
  
    self.view.set_dirty()

    size = (kb.size[0], kb.size[1]*2)

    self.__dirty = True

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

            self.view.set_dirty()
      
            self.__dirty = True
          else:
            self.view.handle_event(event)

      if kb_dev != None and kb_dev.poll():
        events = kb_dev.read(1)

        print(events)

        if len(events) > 1:
          self.view.handle_midi_event(events[0])

      screen.fill(BLACK)

      view_screen = self.view.render()

      self.view.clear_dirty()

      screen.blit(view_screen, (0, 0))  

      if self.__dirty:
        kb.clear_key_overlays()

        self.view.render_keyboard_overlay(kb);

        self.__dirty = False

      kb_screen = kb.render()

      screen.blit(kb_screen, (0, kb_screen.get_height()))

      pygame.display.flip() 

      clock.tick(30)

  def change_view(self, view):
    self.view.clear_msg_text()

    self.view_stack.insert(0, self.view)

    self.view = view

    self.view.set_dirty()

    self.__dirty = True

  def previous_view(self):
    self.view.clear_msg_text()

    self.view = self.view_stack.pop(0)

    self.view.set_dirty()

    self.__dirty = True

piano = pyPiano()
piano.run()
