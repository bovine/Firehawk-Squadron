import pygame
from os import path
from random import randint

class Star(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight):
        pygame.sprite.Sprite.__init__(self)
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.speed = 1

        self.color = randint(1,5)

        if self.color == 1:
        	self.image = pygame.image.load('Assets/Images/Stars/blue.png').convert_alpha()
        if self.color == 2:
        	self.image = pygame.image.load('Assets/Images/Stars/green.png').convert_alpha()
        if self.color == 3:
        	self.image = pygame.image.load('Assets/Images/Stars/orange.png').convert_alpha()
        if self.color == 4:
        	self.image = pygame.image.load('Assets/Images/Stars/red.png').convert_alpha()
        if self.color == 5:
        	self.image = pygame.image.load('Assets/Images/Stars/yellow.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = randint(50, self.screenWidth - 50)
        self.rect.centery = randint(50, self.screenHeight)

    def update(self):
    	self.rect.centery = self.rect.centery + self.speed
    	if self.rect.centery > self.screenHeight + 50:
    		self.rect.centery = -50
    		self.rect.centerx = randint(50, self.screenWidth - 50)
