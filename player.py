import pygame
from os import path
from projectile import *

class Player(pygame.sprite.Sprite):
	def __init__(self, shipSpriteName, player, screenWidth, screenHeight, startX, startY, audioLevel):
		super().__init__()
		self.shipSpriteName = shipSpriteName
		self.player = player # Used to determine laser color. Assigned 1 or 2.
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight

		self.image = pygame.image.load("Assets/Images/Player/" + self.shipSpriteName + "1.png").convert_alpha() # Loads the player graphic based on the name passed in by shipSpriteName
		self.rect = self.image.get_rect()

		self.direction = pygame.math.Vector2()
		self.speed = 8

		self.alive = True
		self.gameOver = False

		self.startX = startX
		self.startY = startY

		self.rect.centerx = self.startX # Starting location
		self.rect.centery = self.startY

		self.audioLevel = audioLevel

		self.standardDelay = 300 # Do not change this. Several timers use it.

		# Shield setup
		self.foreShields = 2
		self.aftShields = 2
		self.foreToRightShields = 0
		self.aftToLeftShields = 0
		self.isRotating = False
		self.firstRotation = False
		self.rotationTimer = pygame.time.get_ticks()
		self.shieldRechargeDelay = 30000 # 60,000 milliseconds in 1 minute
		self.startShieldRecharge = pygame.time.get_ticks()
		self.shieldSurface = pygame.image.load("Assets/Images/Effects/shield.png").convert_alpha() # Loads the shield image
		self.shieldRect = self.shieldSurface.get_rect()
		self.aftShieldSurface = pygame.transform.flip(self.shieldSurface, False, True) # Flips the shield image to get the aft shield
		self.rotatedLeftShieldSurface = pygame.transform.rotate(self.shieldSurface, 90)
		self.rotatedRightShieldSurface = pygame.transform.rotate(self.shieldSurface, 270)
		self.shieldRegenSound = pygame.mixer.Sound('Assets/Audio/Sounds/forceField_000.ogg')
		self.shieldRegenSound.set_volume(self.audioLevel)
		self.shieldHitSound = pygame.mixer.Sound('Assets/Audio/Sounds/explosionCrunch_001.ogg')
		self.shieldHitSound.set_volume(self.audioLevel)
		self.shieldHiteSurface = pygame.image.load("Assets/Images/Effects/shieldHit.png").convert_alpha()
		self.shieldHitRect = self.shieldHiteSurface.get_rect()
		self.shieldHitTime = pygame.time.get_ticks() - 500

		# Missle setup
		self.leftMissles = 2
		self.rightMissles = 2
		self.lastMissleFired = pygame.time.get_ticks()
		self.readyToFireMissle = True
		self.missles = pygame.sprite.Group()
		self.missleSound = pygame.mixer.Sound('Assets/Audio/Sounds/Missle.wav')
		self.missleSound.set_volume(self.audioLevel)

		# Laser setup
		self.lasers = pygame.sprite.Group()
		self.laserSound = pygame.mixer.Sound('Assets/Audio/Sounds/Laser.wav')
		self.laserSound.set_volume(self.audioLevel)
		self.shootDelay = 300 # delay in ticks for firing lasers
		self.lastShot = pygame.time.get_ticks() # the last time a laser was fired
		self.ready = True # Tracks if another laser can be fired based on shoot_delay   

	def movePlayer(self,direction):
		self.rect.centerx += direction[0] * self.speed
		self.rect.centery += direction[1] * self.speed
		# Constrain the player to the screen
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > self.screenWidth:
			self.rect.right = self.screenWidth
		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > self.screenHeight:
			self.rect.bottom = self.screenHeight

	def shoot(self):
		if self.ready:
			self.laserSound.play()
			leftLaser = Laser(self.screenWidth, self.screenHeight, True, self.player, self.rect.centerx - 15, self.rect.top + 20)
			self.lasers.add(leftLaser)
			rightLaser = Laser(self.screenWidth, self.screenHeight, True, self.player, self.rect.centerx + 15, self.rect.top + 20)
			self.lasers.add(rightLaser)
			self.ready = False

	def rechargeLaser(self): # Checks to see if enough time has passed to fire again.
		if not self.ready:
			currentTime = pygame.time.get_ticks()
			if currentTime - self.lastShot >= self.shootDelay:
				self.ready = True

	def fireMissle(self, side):
		if self.readyToFireMissle == True:
			if side == "left" and self.leftMissles > 0 or side == "right" and self.rightMissles > 0:
				if side == "left":
					self.leftMissles = self.leftMissles - 1
					missleX = self.rect.centerx - 15
					missleY = self.rect.top + 20
				elif side == "right":
					self.rightMissles = self.rightMissles - 1
					missleX = self.rect.centerx + 15
					missleY = self.rect.top + 20
				self.readyToFireMissle = False
				self.lastMissleFired = pygame.time.get_ticks()
				self.missleSound.play()
				missle = Missle(self.screenWidth, self.screenHeight, missleX, missleY)
				self.missles.add(missle)

	def rechargeMissle(self):
		currentTime = pygame.time.get_ticks()
		if currentTime - self.lastMissleFired >= self.standardDelay * 10:
			self.readyToFireMissle = True

	def displayShields(self, screen):
		if self.foreShields > 0:
			screen.blit(self.shieldSurface,(self.rect.left + 2, self.rect.top - 5))
			if self.foreShields > 1:
				screen.blit(self.shieldSurface,(self.rect.left + 2, self.rect.top - 15))
		if self.aftShields > 0:
			screen.blit(self.aftShieldSurface,(self.rect.left + 2, self.rect.bottom))
			if self.aftShields > 1:
				screen.blit(self.aftShieldSurface,(self.rect.left + 2, self.rect.bottom + 10))
		if self.aftToLeftShields > 0:
			screen.blit(self.rotatedLeftShieldSurface,(self.rect.left - 10, self.rect.top))
			if self.aftToLeftShields > 1:
				screen.blit(self.rotatedLeftShieldSurface,(self.rect.left - 20, self.rect.top))
		if self.foreToRightShields > 0:
			screen.blit(self.rotatedRightShieldSurface,(self.rect.right, self.rect.top))
			if self.foreToRightShields > 1:
				screen.blit(self.rotatedRightShieldSurface,(self.rect.right + 10, self.rect.top))
		currentTime = pygame.time.get_ticks()
		if currentTime < self.shieldHitTime + self.standardDelay:
			screen.blit(self.shieldHiteSurface,(self.rect.left, self.rect.top - 15))


	def rotateShields(self): # Triggers the shield rotation
		self.isRotating = True
		self.firstRotation = True
		self.rotationTimer = pygame.time.get_ticks()
		self.startShieldRecharge = pygame.time.get_ticks()

	def rotateShieldsAnimation(self): # Animates the shield rotation
		currentTime = pygame.time.get_ticks()
		if currentTime > self.rotationTimer + self.standardDelay and self.firstRotation == True:
			self.foreToRightShields = self.foreShields
			self.foreShields = 0
			self.aftToLeftShields = self.aftShields
			self.aftShields = 0
			self.firstRotation = False
		if currentTime > self.rotationTimer + self.standardDelay * 2:
			self.aftShields = self.foreToRightShields
			self.foreToRightShields = 0
			self.foreShields = self.aftToLeftShields
			self.aftToLeftShields = 0
			self.isRotating = False

	def rechargeShields(self):
		if self.aftShields < 2:
			currentTime = pygame.time.get_ticks()
			if currentTime - self.startShieldRecharge >= self.shieldRechargeDelay:
				self.aftShields = self.aftShields + 1
				self.shieldRegenSound.play()
				self.startShieldRecharge = pygame.time.get_ticks()

	def hit(self):
		if self.foreShields > 0:
			self.shieldHitSound.play()
			self.foreShields = self.foreShields - 1
			self.shieldHitTime = pygame.time.get_ticks()
		elif self.foreShields <= 0:
			self.alive = False

	def update(self, direction):
		self.movePlayer(direction)
		self.lasers.update()
		self.missles.update()
		self.rechargeLaser()
		self.rechargeShields()
		if self.isRotating == True:
			self.rotateShieldsAnimation()
		if self.readyToFireMissle == False:
			self.rechargeMissle()



