import pygame

class Button(pygame.sprite.Sprite):
	def __init__(self, active, pos, label):
		pygame.sprite.Sprite.__init__(self)

		self.active = active
		self.pos = pos
		self.label = label
		self.audioLevel = .2
		self.font = pygame.font.Font('Assets/font/kenvector_future.ttf',20)
		self.image = pygame.image.load("Assets/Images/UI/buttonRed.png").convert_alpha()
		self.rect = self.image.get_rect(topleft = self.pos)
		self.activeImage = pygame.image.load("Assets/Images/UI/buttonBlue.png").convert_alpha()
		self.inactiveImage = pygame.image.load("Assets/Images/UI/buttonRed.png").convert_alpha()
		self.text = self.font.render(self.label, False, (0,0,0))
		self.textRect = self.text.get_rect(topleft = (self.pos[0] + 20, self.pos[1] + 10))
		self.clicked = False
		self.dingOnce = False
		self.buttonDing = pygame.mixer.Sound('Assets/Audio/Sounds/Ding.wav')
		self.buttonDing.set_volume(self.audioLevel)

	def addLabel(self, screen):
		screen.blit(self.text, self.textRect)

	def update(self):
		mousePos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mousePos):
			self.active = 'active'
			if self.dingOnce == False:
				self.buttonDing.play()
				self.dingOnce = True
		else:
			self.active = 'inactive'
			self.dingOnce = False


		if self.active == 'active':
			self.image = self.activeImage
		else:
			self.image = self.inactiveImage

class ArrowButton(pygame.sprite.Sprite):
	def __init__(self, active, pos, value):
		pygame.sprite.Sprite.__init__(self)

		self.active = active
		self.pos = pos
		self.value = value
		self.clicked = False
		self.dingOnce = False
		self.buttonDing = pygame.mixer.Sound('Assets/Audio/Sounds/Ding.wav')

		if self.value == -1:
			self.image = pygame.image.load("Assets/Images/UI/downOne.png").convert_alpha()
		elif self.value == -10:
			self.image = pygame.image.load("Assets/Images/UI/downTen.png").convert_alpha()
		elif self.value == 1:
			self.image = pygame.image.load("Assets/Images/UI/upOne.png").convert_alpha()
		elif self.value == 10:
			self.image = pygame.image.load("Assets/Images/UI/upTen.png").convert_alpha()
		self.rect = self.image.get_rect(topleft = self.pos)

	def update(self):
		mousePos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mousePos):
			self.active = 'active'
			if self.dingOnce == False:
				self.buttonDing.play()
				self.dingOnce = True
		else:
			self.active = 'inactive'
			self.dingOnce = False
			self.clicked = False