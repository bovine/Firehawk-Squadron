import pygame
from os import path

class Laser(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight, playerOrEnemy, player, x, y):
        '''
        bounds: screen size
        playerOrEnemy: booleen. True for player, false for enemy
        player: Determines player 1 or player 2. Valid numbers are 1 and 2
        '''
        pygame.sprite.Sprite.__init__(self)
        self.playerOrEnemy = playerOrEnemy
        self.player = player
        if self.playerOrEnemy:
            if self.player == 1:
                self.image = pygame.image.load("Assets/Images/Effects/laserBlue.png").convert_alpha() #loads the sprite file
            elif self.player == 2:
                self.image = pygame.image.load("Assets/Images/Effects/laserGreen.png").convert_alpha() #loads the sprite file
        else:
            self.image = pygame.image.load("Assets/Images/Effects/laserRed.png").convert_alpha() #loads the sprite file
        self.image = pygame.transform.scale(self.image,(5,28))
        self.rect = self.image.get_rect() # Gets the rectangle around the sprite

        if self.playerOrEnemy: # Controls the direction of the laser.
            self.speedy = -12
        else:
            self.speedy = 12

        self.bounds = (screenWidth, screenHeight)
        self.rect.centerx = x
        self.rect.bottom = y
        
    def update(self):
        self.rect.y += self.speedy
        
        if self.rect.bottom < -50 or self.rect.top > self.bounds[1] + 50:
            self.kill()

class Missle(pygame.sprite.Sprite):
    def __init__(self,screenWidth, screenHeight, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/Images/Effects/missle.png").convert_alpha()
        self.rect = self.image.get_rect() # Gets the rectangle around the sprite
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedY = -40

    def update(self):
        self.rect.y += self.speedY
        if self.rect.bottom < -50:
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, bounds, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/star3.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.bounds = bounds
        self.speed = 15

    def update(self):
        self.rect.centery += self.speed

        if self.rect.top > self.bounds[1] - 50:
            self.kill()

