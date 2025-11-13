import pygame
from os import path
from projectile import Laser
from random import randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight, startX, startY, shipType, attackPattern, audioLevel): 
        '''
        shipType: one, two, rockDropper, miniBoss
        attackPattern: dive, position of the rockDropper, strafe
        '''
        pygame.sprite.Sprite.__init__(self)
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.onScreen = False
        self.startx = startX
        self.starty = startY
        self.miniBossLeftOrRight = randint(1,2) # 1 is left, 2 is right
        self.miniBossYMovement = True # 

        self.shipType = shipType
        self.attackPattern = attackPattern
        self.resetAttackPattern = False
        self.shootY = randint(50, self.screenHeight / 2)

        self.audioLevel = audioLevel

        self.hitpoints = 1
        self.score = 10
        self.speedX = 0
        self.speedY = 6

        self.lasers = pygame.sprite.Group()
        self.laserSound = pygame.mixer.Sound('Assets/Audio/Sounds/Laser.wav')
        self.laserSound.set_volume(self.audioLevel)
        self.shootDelay = 3000 # delay in ticks for firing lasers
        self.lastShot = pygame.time.get_ticks() # the last time a laser was fired
        self.ready = True # Tracks if another laser can be fired based on shoot_delay
        self.strafeShoot = 0

        if self.shipType == 'one':
            self.image = pygame.image.load('Assets/Images/Enemies/Enemy1.png').convert_alpha()
        elif self.shipType == 'two':
            self.image = pygame.image.load('Assets/Images/Enemies/Enemy2.png').convert_alpha()
        elif self.shipType == 'rockDropper':
            self.image = pygame.image.load('Assets/Images/Enemies/RockDropper.png').convert_alpha()
            self.hitpoints = 4
            self.score = 40
        elif self.shipType == 'miniBoss':
            self.image = pygame.image.load('Assets/Images/Enemies/MiniBoss.png').convert_alpha()
            self.hitpoints = 20
            self.score = 100
        else:
            raise pygame.error("Unsupported shipType")
        self.rect = self.image.get_rect()
        self.rect.centerx = self.startx
        self.rect.centery = self.starty

        if self.attackPattern == "strafe":
            self.speedY = 0
            temp = randint(1,2)
            if temp == 1:
                self.rect.centerx = -100
                self.speedX = 6
            elif temp == 2:
                self.rect.centerx = self.screenWidth + 50
                self.speedX = -6
        elif self.attackPattern == "miniBoss":
            self.rect.centerx = randint(200, self.screenWidth - 200)
            self.rect.centery = -100

    def shoot(self):
        '''
        Only works for Dive attack pattern because of shootY
        '''
        if self.ready and self.rect.centery >= self.shootY:
            self.laserSound.play()
            laser = Laser(self.screenWidth, self.screenHeight, False, 3, self.rect.centerx, self.rect.bottom + 20)
            self.lasers.add(laser)
            self.lastShot = pygame.time.get_ticks()
            self.ready = False

    def rechargeLaser(self):
        '''
        Checks to see if enough time has passed to fire again.
        '''
        if not self.ready:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.lastShot >= self.shootDelay:
                self.ready = True

    def move(self):
        self.rect.centerx = self.rect.centerx + self.speedX
        self.rect.centery = self.rect.centery + self.speedY

    def checkOnscreen(self):
        if self.rect.centerx < 0 or self.rect.centerx > self.screenWidth or self.rect.centery < 0 or self.rect.centery > self.screenHeight:
            self.onScreen = False
        else:
            self.onScreen = True
            self.resetAttackPattern = True

    def hit(self):
        self.hitpoints = self.hitpoints - 1
        if self.hitpoints <= 0:
            self.rect.centerx = -1000 # Moves sprite off screen until all lasers are gone.
            self.speedY = 0
            self.speedX = 0

    def dive(self): # If attackPattern is dive 
        if self.onScreen == False and self.resetAttackPattern == True:
            self.resetDive()

    def resetDive(self):
        self.shootY = randint(50, self.screenHeight / 2)
        self.rect.centerx = randint(50, self.screenWidth - 50)
        self.rect.centery = -50
        self.resetAttackPattern = False

    def strafe(self):
        if self.onScreen == False and self.resetAttackPattern == True:
            self.resetStrafe()
        if self.ready: # Handles shooting for strafe attack pattern
            self.laserSound.play()
            laser = Laser(self.screenWidth, self.screenHeight, False, 3, self.rect.centerx, self.rect.bottom + 20)
            self.lasers.add(laser)
            self.lastShot = pygame.time.get_ticks()
            self.ready = False
            self.strafeShoot = self.strafeShoot + 1
        if self.strafeShoot > 2:
            self.speedY = 6

    def resetStrafe(self):
        self.speedX = self.speedX * -1

    def miniBossControl(self):
        if self.miniBossYMovement == True:
            if self.rect.centery >= self.screenHeight / 3:
                self.miniBossYMovement = False
                self.speedY = 0
                if self.miniBossLeftOrRight == 1:
                    self.speedX = -6
                elif self.miniBossLeftOrRight == 2:
                    self.speedX = 6
                else:
                    self.speedX = -6
        elif self.miniBossYMovement == False:
            self.miniBossShoot()
            if self.rect.left < 0 or self.rect.right > self.screenWidth:
                self.speedX = self.speedX * -1

    def miniBossShoot(self):
        if self.ready:
            self.laserSound.play()
            laser1 = Laser(self.screenWidth, self.screenHeight, False, 3, self.rect.centerx, self.rect.centery)
            self.lasers.add(laser1)
            laser2 = Laser(self.screenWidth, self.screenHeight, False, 3, self.rect.centerx - 20, self.rect.centery)
            self.lasers.add(laser2)
            laser3 = Laser(self.screenWidth, self.screenHeight, False, 3, self.rect.centerx + 20, self.rect.centery)
            self.lasers.add(laser3)
            self.lastShot = pygame.time.get_ticks()
            self.ready = False

    def update(self):
        self.rechargeLaser()
        self.move()
        self.checkOnscreen()

        if self.attackPattern == "dive":
            self.dive()
            self.shoot()
        elif self.attackPattern == "strafe":
            self.strafe()
            if self.rect.centery > self.screenHeight + 100:
                self.attackPattern = "dive"
                self.speedX = 0
        elif self.attackPattern == "miniBoss":
            self.miniBossControl()

        if self.hitpoints <= 0 and not self.lasers: # If all lasers are gone and HP is <= 0 kill sprite
            self.kill()
