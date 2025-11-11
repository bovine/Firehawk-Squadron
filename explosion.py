import pygame
from os import path

class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, screen, audioLevel):
		pygame.sprite.Sprite.__init__(self)

		self.audioLevel = audioLevel
		self.explosionSound = pygame.mixer.Sound('Assets/Audio/Sounds/explosionCrunch_000.ogg')
		self.explosionSound.set_volume(self.audioLevel)
		self.explosionSound.play()

		self.imageYellow = pygame.image.load('Assets/Images/Effects/explosionYellow.png').convert_alpha()
		self.rectYellow = self.imageYellow.get_rect()
		self.rectYellow.centerx = x
		self.rectYellow.centery = y

		self.imageOrange = pygame.image.load('Assets/Images/Effects/explosionOrange.png').convert_alpha()
		self.rectOrange = self.imageOrange.get_rect()
		self.rectOrange.centerx = x
		self.rectOrange.centery = y

		self.imageGrey = pygame.image.load('Assets/Images/Effects/explosionGrey.png').convert_alpha()
		self.rectGrey = self.imageGrey.get_rect()
		self.rectGrey.centerx = x
		self.rectGrey.centery = y

		self.screen = screen
		self.timer = 10

	def update(self):
		if self.timer <= 5:
			self.screen.blit(self.imageGrey,self.rectGrey)
		if self.timer >= 3 and self.timer <= 7:
			self.screen.blit(self.imageOrange,self.rectOrange)
		if self.timer >= 5:
			self.screen.blit(self.imageYellow,self.rectYellow)

		self.timer -= 1
		if self.timer <= 0:
			self.kill()

class MiniExplosion(pygame.sprite.Sprite):
	def __init__(self, x, y, screen, audioLevel):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('Assets/Images/Effects/smoke.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.audioLevel = audioLevel

		self.explosionSound = pygame.mixer.Sound('Assets/Audio/Sounds/explosionCrunch_000.ogg')
		self.explosionSound.set_volume(self.audioLevel)
		self.explosionSound.play()

		self.screen = screen
		self.timer = 10

	def update(self):
		self.screen.blit(self.image, self.rect)

		self.timer -= 1
		if self.timer <= 0:
			self.kill()

class BigExplosion(pygame.sprite.Sprite):
	def __init__(self, x, y, screen, audioLevel):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('Assets/Images/Effects/missleExplosion.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.audioLevel = audioLevel

		self.explosionSound = pygame.mixer.Sound('Assets/Audio/Sounds/explosionCrunch_000.ogg')
		self.explosionSound.set_volume(self.audioLevel)
		self.explosionSound.play()

		self.screen = screen
		self.timer = 30

	def update(self):
		self.screen.blit(self.image, self.rect)

		self.timer -= 1
		if self.timer <= 0:
			self.kill()