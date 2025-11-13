import pygame
from os import path

class Powerup(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight, x, y, powerupType):
        '''
        powerupType: shield, missle
        '''
        pygame.sprite.Sprite.__init__(self)

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.x = x
        self.y = y
        self.powerupType = powerupType

        self.speedy = 4

        if self.powerupType == "shield":
        	self.image = pygame.image.load('Assets/Images/Powerups/shield.png').convert_alpha()
        elif self.powerupType == "missle":
        	self.image = pygame.image.load('Assets/Images/Powerups/missle.png').convert_alpha()
        else:
            raise pygame.error("Unsupported powerupType")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

    def update(self):
    	self.rect.centery = self.rect.centery + self.speedy
    	if self.rect.centery > self.screenHeight + 50:
    		self.kill()
