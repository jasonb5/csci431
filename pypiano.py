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

	def handle_event(self, event):
		return

class PlayView(View):
	def __init__(self, size):
		View.__init__(self, size)

class LibraryView(View):
	def __init__(self, size):
		View.__init__(self, size)

		self.title = self.font.render("Library", True, WHITE)

	def render(self):
		self.screen.blit(self.title, (0, 0))

		return self.screen	

class OptionsView(View):
	def __init__(self, size):
		View.__init__(self, size)

		self.title = self.font.render("Options", True, WHITE)

		def render(self):
			self.screen.blit(self.title, (0, 0))

			return self.screen

class MainMenuView(View):
	def __init__(self, size, event_handler):
		View.__init__(self, size)

		self.event_handler = event_handler

		self.menus = []
		self.voffset = 20
		self.vert = 0
		self.dirty = True
		self.init = False
		self.max_width = 0
		self.sel = 0

	def adjust_xpos(self):
		for x in self.menus:
			pos = ((self.size[0]-self.max_width)/2, x[1][1])
			x[1] = pos	

	def add(self, title, view):
		size = self.font.size(title)
		if size[0] > self.max_width: self.max_width = size[0]
		text = self.font.render(title, True, WHITE)
		pos = (0, self.voffset+self.vert)
		self.vert += size[1]
		self.menus.append([text, pos, size, view])

	def render(self):
		if self.dirty:
			if not self.init:
				self.adjust_xpos()	

				self.init = True

			self.screen.fill(BLACK)

			for x in self.menus:
				self.screen.blit(x[0], x[1])

			pos = self.menus[self.sel][1]

			pygame.draw.circle(self.screen, WHITE, (pos[0]-16, pos[1]+12), 10)

			self.dirty = False
	
		return self.screen

	def handle_event(self, event):
		if event.key == pygame.K_w:
			self.sel += 1	
			if self.sel > len(self.menus)-1: self.sel = len(self.menus)-1
			self.dirty = True
		elif event.key == pygame.K_e:
			self.sel -= 1
			if self.sel < 0: self.sel = 0
			self.dirty = True
		elif event.key == pygame.K_q:
			self.event_handler(self.menus[self.sel][3])

class Keyboard:
	def __init__(self):
		self.w_width = 40
		self.w_height = 200
		self.w_keys = []
	
		self.b_width = 30
		self.b_height = 150
		self.b_keys = []

		self.spacing = 2
		self.dirty = False

		self.size = (7*self.w_width+6*self.spacing, self.w_height)

		self.screen = pygame.Surface(self.size)

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

	def render(self):
		if self.dirty:
			self.screen.fill(BLACK)

			for x in self.w_keys:
				pygame.draw.rect(self.screen, WHITE, x[0])

			for x in self.b_keys:
				pygame.draw.rect(self.screen, BLACK, x[0])	

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

		self.view = MainMenuView(kb.size, self.event_handler)

		self.view.add("Play", play_view)
		self.view.add("Library", lib_view)
		self.view.add("Options", option_view)

		size = (kb.size[0], kb.size[1]*2)

		screen = pygame.display.set_mode(size)		

		clock = pygame.time.Clock()

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						sys.exit(1)
					else:
						self.view.handle_event(event)

			screen.fill(BLACK)

			view_screen = self.view.render()

			screen.blit(view_screen, (0, 0))	

			kb_screen = kb.render()

			screen.blit(kb_screen, (0, kb_screen.get_height()))

			pygame.display.flip()	

			clock.tick(30)

	def event_handler(self, screen):
		self.view = screen

piano = pyPiano()
piano.run()
