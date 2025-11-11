import pygame
import sys
from os import path
from random import randint
from pygame.locals import *
from player import Player
from enemy import Enemy
from explosion import *
from objects import *
from powerup import *

class Game:
	def __init__(self, screen, screenWidth, screenHeight, audioLevel):
		self.screen = screen
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight
		self.audioLevel = audioLevel
		self.firstPressed = 99 # Used to determine player 1's controller. First person to press start is player 1.
		self.playerOneJoy = 99 # Player joys set to 99 for dynamic controller assignment. Either joy can be player 1. Whoever presses start first is player 1.
		self.playerTwoJoy = 99

		self.playerOneShipChoice = 1 # Used to determine which ship each player has selected on ship select screen
		self.playerTwoShipChoice = 5 # 1=red, 2=blue, 3=green, 4=yellow, 5=press start
		self.playerOneSelected = False # Controls displaying the check mark on the selected ships
		self.playerTwoSelected = False # 

		self.numberOfPlayers = 0
		self.score = 0
		self.lastScore = 0
		self.gameRunning = False

		self.font = pygame.font.Font('Assets/Font/kenvector_future.ttf',50)

		self.gameOverSurface = self.font.render(str("Game Over"), False, (255,255,255))
		self.gameOverRect = self.gameOverSurface.get_rect(center = (self.screenWidth / 2, self.screenHeight / 2))
		self.gameOver = False
		self.gameOverTimer = 4800
		self.gameOverTime = pygame.time.get_ticks()

		self.sector = 0
		self.displaySector = False
		self.sectorSurface = self.font.render(str("Sector ") + str(self.sector), False, (255,255,255))
		self.sectorRect = self.sectorSurface.get_rect(center = (self.screenWidth / 2, self.screenHeight / 2))
		self.sectorStartTime = pygame.time.get_ticks()
		self.sectorDisplayTimer = 4800

		self.enemySpawnDelay = 300
		self.lastEnemySpawn = pygame.time.get_ticks()
		self.maxEnemiesLive = 20 # Max enemies in play. default 20
		self.liveEnemies = 0 # Current active enemies
		self.baseSectorEnemies = 10 # The base number of enemies that will spawn in the current sector * sector
		self.totalSectorEnemies = 0 # The number of enemies that will spawn in the current sector


# Screens --------------------------------------------------------------------------------------
		self.controlsSurface = pygame.image.load('Assets/Images/Screens/Controls.png').convert_alpha() # Controls screen
		self.controlsSurface = pygame.transform.scale(self.controlsSurface, (self.screenWidth, self.screenHeight)) # Scales the screen image to match the display
		self.controlsRect = self.controlsSurface.get_rect(topleft = (0,0))

		self.creditsSurface = pygame.image.load('Assets/Images/Screens/Credits.png').convert_alpha() # Credits screen
		self.creditsSurface = pygame.transform.scale(self.creditsSurface, (self.screenWidth, self.screenHeight)) # Scales the screen image to match the display
		self.creditsRect = self.creditsSurface.get_rect(topleft = (0,0))

		self.highScoresSurface = pygame.image.load('Assets/Images/Screens/HighScores.png').convert_alpha() # High Scores screen
		self.highScoresSurface = pygame.transform.scale(self.highScoresSurface, (self.screenWidth, self.screenHeight)) # Scales the screen image to match the display
		self.highScoresRect = self.highScoresSurface.get_rect(topleft = (0,0))

		self.optionsSurface = pygame.image.load('Assets/Images/Screens/Options.png').convert_alpha() # High Scores screen
		self.optionsSurface = pygame.transform.scale(self.optionsSurface, (self.screenWidth, self.screenHeight)) # Scales the screen image to match the display
		self.optionsRect = self.optionsSurface.get_rect(topleft = (0,0))

		self.splashSurface = pygame.image.load('Assets/Images/Screens/Splash.png').convert_alpha() # Splash screen
		self.splashSurface = pygame.transform.scale(self.splashSurface, (self.screenWidth, self.screenHeight)) # Scales the screen image to match the display
		self.splashRect = self.splashSurface.get_rect(topleft = (0,0))

		self.shipSelectSurface = pygame.image.load('Assets/Images/Screens/ShipSelect.png').convert_alpha() # Splash screen
		self.shipSelectSurface = pygame.transform.scale(self.shipSelectSurface, (self.screenWidth, self.screenHeight)) # Scales the screen image to match the display
		self.shipSelectRect = self.shipSelectSurface.get_rect(topleft = (0,0))

		self.currentScreen = 'Splash' # Set default screen
# END Screens --------------------------------------------------------------------------------------

# Space Backgrounds --------------------------------------------------------------------------------------
		self.backgroundSurface = pygame.image.load('Assets/Images/Backgrounds/space.png').convert_alpha()
		self.backgroundSurface = pygame.transform.scale(self.backgroundSurface, (self.screenWidth, self.screenHeight))
		self.backgroundRect = self.backgroundSurface.get_rect(topleft = (0,0))

# UI --------------------------------------------------------------------------------------
		self.P1UISurface = pygame.image.load('Assets/Images/UI/P1UI.png').convert_alpha()
		self.P1UIRect =  self.P1UISurface.get_rect(bottomleft = (0,self.screenHeight))
		self.P2UISurface = pygame.image.load('Assets/Images/UI/P2UI.png').convert_alpha()
		self.P2UIRect =  self.P2UISurface.get_rect(bottomright = (self.screenWidth,self.screenHeight))
		self.missleUISurface = pygame.image.load('Assets/Images/UI/MissleUI.png').convert_alpha()
		self.missleUIRect = self.missleUISurface.get_rect(topleft = (0,0))

# Music and sounds --------------------------------------------------------------------------------------
		self.splashMusic = pygame.mixer.Sound('Assets/Audio/Music/Crypto.mp3')
		self.splashMusic.set_volume(self.audioLevel)
		self.splashMusic.play(loops = -1)
		self.gameMusic = pygame.mixer.Sound('Assets/Audio/Music/Space Fighter Loop.mp3')
		self.gameMusic.set_volume(self.audioLevel)
		self.gameMusicPlaying = False # To turn on game music when the game starts
# to stop the music    self.splashMusic.stop() --------------------------------------------------------------------------------------

# Spritegroup setups --------------------------------------------------------------------------------------
		self.player1 = pygame.sprite.Group()
		self.player2 = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		self.explosions = pygame.sprite.Group()
		self.stars = pygame.sprite.Group()
		self.powerupGroup = pygame.sprite.Group()

# Stars --------------------------------------------------------------------------------------
		self.numberOfStars = 30
		self.starCounter = 0
		while self.starCounter <= self.numberOfStars:
			self.star = Star(self.screenWidth, self.screenHeight)
			self.stars.add(self.star)
			self.starCounter = self.starCounter + 1

	def setAudioLevel(self):
		self.splashMusic.set_volume(self.audioLevel)
		self.gameMusic.set_volume(self.audioLevel)

	def createPlayer1(self): # 1=red, 2=blue, 3=green, 4=yellow
		if self.playerOneShipChoice == 1:
			self.player1Sprite = Player("PlayerRed", 1, self.screenWidth, self.screenHeight, self.screenWidth / 3, self.screenHeight - 200, self.audioLevel) # Graphic, screenWidth, screenHeight, startX, startY
		elif self.playerOneShipChoice == 2:
			self.player1Sprite = Player("PlayerBlue", 1, self.screenWidth, self.screenHeight, self.screenWidth / 3, self.screenHeight - 200, self.audioLevel)
		elif self.playerOneShipChoice == 3:
			self.player1Sprite = Player("PlayerGreen", 1, self.screenWidth, self.screenHeight, self.screenWidth / 3, self.screenHeight - 200, self.audioLevel)
		elif self.playerOneShipChoice == 4:
			self.player1Sprite = Player("PlayerYellow", 1, self.screenWidth, self.screenHeight, self.screenWidth / 3, self.screenHeight - 200, self.audioLevel)
		self.player1.add(self.player1Sprite) # Adds player1Sprite to the sprite group for player 1
		self.maxEnemiesLive = self.maxEnemiesLive + 5
		
	def createPlayer2(self):
		if self.playerTwoShipChoice != 5: # If player 2 exists and has made a choice.
			if self.playerTwoShipChoice == 1:
				self.player2Sprite = Player("PlayerRed", 2, self.screenWidth, self.screenHeight, self.screenWidth / 3 * 2, self.screenHeight - 200, self.audioLevel)
			elif self.playerTwoShipChoice == 2:
				self.player2Sprite = Player("PlayerBlue", 2, self.screenWidth, self.screenHeight, self.screenWidth / 3 * 2, self.screenHeight - 200, self.audioLevel)
			elif self.playerTwoShipChoice == 3:
				self.player2Sprite = Player("PlayerGreen", 2, self.screenWidth, self.screenHeight, self.screenWidth / 3 * 2, self.screenHeight - 200, self.audioLevel)
			elif self.playerTwoShipChoice == 4:
				self.player2Sprite = Player("PlayerYellow", 2, self.screenWidth, self.screenHeight, self.screenWidth / 3 * 2, self.screenHeight - 200, self.audioLevel)
			self.player2.add(self.player2Sprite) # Adds player2Sprite to the sprite group for player 2
			self.maxEnemiesLive = self.maxEnemiesLive + 5

	def drawPlayerOneStuff(self): # UI elements and explosions when player1 dies
		self.player1Sprite.lasers.draw(self.screen)
		self.player1Sprite.missles.draw(self.screen)

		# UI element for Player 1
		if self.player1Sprite.gameOver == False:
			self.screen.blit(self.P1UISurface, self.P1UIRect)
			if self.player1Sprite.leftMissles > 0:
				self.screen.blit(self.missleUISurface,(self.missleUIRect.right + 50, self.screenHeight - 35))
				if self.player1Sprite.leftMissles > 1:
					self.screen.blit(self.missleUISurface,(self.missleUIRect.right + 70, self.screenHeight - 35))
			if self.player1Sprite.rightMissles > 0:
				self.screen.blit(self.missleUISurface,(self.missleUIRect.right + 95, self.screenHeight - 35))
				if self.player1Sprite.rightMissles > 1:
					self.screen.blit(self.missleUISurface,(self.missleUIRect.right + 115, self.screenHeight - 35))
		# End UI Elements for player 1

			self.player1.draw(self.screen)
			self.player1Sprite.displayShields(self.screen)
			
			if self.player1Sprite.alive == False and self.player1Sprite.gameOver == False:
				explosionSprite = Explosion(self.player1Sprite.rect.centerx, self.player1Sprite.rect.centery, self.screen, self.audioLevel)
				self.explosions.add(explosionSprite)
				self.player1Sprite.gameOver = True
				self.player1Sprite.kill()

		else:
			gameOverRect = self.gameOverSurface.get_rect(bottomleft = (0, self.screenHeight))
			self.screen.blit(self.gameOverSurface, gameOverRect)

	def drawPlayerTwoStuff(self): # UI elements and explosions when player2 dies
		self.player2Sprite.lasers.draw(self.screen)
		self.player2Sprite.missles.draw(self.screen)

		# UI element for Player 2
		if self.player2Sprite.gameOver == False:
			self.screen.blit(self.P2UISurface, self.P2UIRect)
			if self.player2Sprite.leftMissles > 0:
				self.screen.blit(self.missleUISurface,(self.screenWidth - 150, self.screenHeight - 35))
				if self.player2Sprite.leftMissles > 1:
					self.screen.blit(self.missleUISurface,(self.screenWidth - 130, self.screenHeight - 35))
			if self.player2Sprite.rightMissles > 0:
				self.screen.blit(self.missleUISurface,(self.screenWidth - 105, self.screenHeight - 35))
				if self.player2Sprite.rightMissles > 1:
					self.screen.blit(self.missleUISurface,(self.screenWidth - 85, self.screenHeight - 35))
		# End UI Elements for player 2

			self.player2.draw(self.screen)
			self.player2Sprite.displayShields(self.screen)

			if self.player2Sprite.alive == False and self.player2Sprite.gameOver == False:
				explosionSprite = Explosion(self.player2Sprite.rect.centerx, self.player2Sprite.rect.centery, self.screen, self.audioLevel)
				self.explosions.add(explosionSprite)
				self.player2Sprite.gameOver = True
				self.player2Sprite.kill()
		else:
			gameOverRect = self.gameOverSurface.get_rect(bottomright = (self.screenWidth, self.screenHeight))
			self.screen.blit(self.gameOverSurface, gameOverRect)

	def drawEnemyStuff(self):
		self.enemies.update()
		self.enemies.draw(self.screen)

		allEnemies = self.enemies.sprites() # Iterate through all enemies and update and draw their lasers
		for enemy in allEnemies:
			enemy.lasers.update()
			enemy.lasers.draw(self.screen)

	def drawStars(self):
		self.stars.update()
		self.stars.draw(self.screen)

	def checkCollisions(self):
		if self.player1: # If player1 exists
			if self.player1Sprite.lasers: # If player1 lasers exist
				for laser in self.player1Sprite.lasers:
					enemiesHit = pygame.sprite.spritecollide(laser, self.enemies, False) # sprite, sprite group, doKill (bool, kills the enemy)
					if enemiesHit: # If any enemies are hit
						for enemy in enemiesHit:
							enemyPosition = (enemy.rect.centerx, enemy.rect.centery)
							enemy.hit()
							if enemy.hitpoints <= 0: # If the enemy is destroyed
								if enemy.shipType == "miniBoss": # Check if miniboss died and drop powerup
									temp = randint(1, 10)
									if temp >= 5 and temp <= 7:
										powerup = Powerup(self.screenWidth, self.screenHeight, enemyPosition[0], enemyPosition[1], "shield")
										self.powerupGroup.add(powerup)
									elif temp > 7:
										powerup = Powerup(self.screenWidth, self.screenHeight, enemyPosition[0], enemyPosition[1], "missle")
										self.powerupGroup.add(powerup)									
								explosionSprite = Explosion(enemyPosition[0], enemyPosition[1], self.screen, self.audioLevel)
								self.explosions.add(explosionSprite)
								self.liveEnemies = self.liveEnemies - 1
								self.score += enemy.score
							elif enemy.hitpoints > 0: # If the enemy is damaged
								explosionSprite = MiniExplosion(laser.rect.centerx, laser.rect.top - 30, self.screen, self.audioLevel)
								self.explosions.add(explosionSprite)
						laser.kill() # Removes the laser that killed the enemy
			if self.player1Sprite.missles: # If player1 missles exist
				for missle in self.player1Sprite.missles:
					if missle.rect.centery <= 200:
						x = missle.rect.centerx
						missle.kill()
						explosionSprite = BigExplosion(x, 200, self.screen, self.audioLevel)
						self.explosions.add(explosionSprite)
						for enemy in self.enemies:
							if enemy.onScreen == True:
								explosionSprite = Explosion(enemy.rect.centerx, enemy.rect.centery, self.screen, self.audioLevel)
								self.explosions.add(explosionSprite)
								enemy.hit()
								if enemy.hitpoints <= 0:
									self.liveEnemies = self.liveEnemies - 1
									self.score += enemy.score


		if self.player2: # If player2 exists
			if self.player2Sprite.lasers: # If player2 lasers exist
				for laser in self.player2Sprite.lasers:
					enemiesHit = pygame.sprite.spritecollide(laser, self.enemies, False) # sprite, sprite group, doKill (bool, kills the enemy)
					if enemiesHit: # If any enemies are hit
						for enemy in enemiesHit:
							enemyPosition = (enemy.rect.centerx, enemy.rect.centery)
							enemy.hit()
							if enemy.hitpoints <= 0: # If the enemy is destroyed
								if enemy.shipType == "miniBoss": # Check if miniboss died and drop powerup
									temp = randint(1, 10)
									if temp >= 5 and temp <= 7:
										powerup = Powerup(self.screenWidth, self.screenHeight, enemyPosition[0], enemyPosition[1], "shield")
										self.powerupGroup.add(powerup)
									elif temp > 7:
										powerup = Powerup(self.screenWidth, self.screenHeight, enemyPosition[0], enemyPosition[1], "missle")
										self.powerupGroup.add(powerup)
								explosionSprite = Explosion(enemyPosition[0], enemyPosition[1], self.screen, self.audioLevel)
								self.explosions.add(explosionSprite)
								self.liveEnemies = self.liveEnemies - 1
								self.score += enemy.score
							elif enemy.hitpoints > 0: # If the enemy is damaged
								explosionSprite = MiniExplosion(laser.rect.centerx, laser.rect.top - 30, self.screen, self.audioLevel)
								self.explosions.add(explosionSprite)
						laser.kill() # Removes the laser that killed the enemy
			if self.player2Sprite.missles: # If player1 missles exist
				for missle in self.player2Sprite.missles:
					if missle.rect.centery <= 200:
						x = missle.rect.centerx
						missle.kill()
						explosionSprite = BigExplosion(x, 200, self.screen, self.audioLevel)
						self.explosions.add(explosionSprite)
						for enemy in self.enemies:
							if enemy.onScreen == True:
								explosionSprite = Explosion(enemy.rect.centerx, enemy.rect.centery, self.screen, self.audioLevel)
								self.explosions.add(explosionSprite)
								enemy.hit()
								if enemy.hitpoints <= 0:
									self.liveEnemies = self.liveEnemies - 1
									self.score += enemy.score

		for enemy in self.enemies: # Enemy lasers hit players
			for laser in enemy.lasers:
				player1Hit = pygame.sprite.spritecollide(laser, self.player1, False)
				if player1Hit:
					self.player1Sprite.hit()
					laser.kill()
				player2Hit = pygame.sprite.spritecollide(laser, self.player2, False)
				if player2Hit:
					self.player2Sprite.hit()
					laser.kill()

		for enemy in self.enemies: # enemy hits player
			player1Hit = pygame.sprite.spritecollide(enemy, self.player1, False)
			if player1Hit:
				self.player1Sprite.hit()
				enemy.hit()
				if enemy.hitpoints <= 0: # If the enemy is destroyed
					explosionSprite = Explosion(enemy.rect.centerx, enemy.rect.centery, self.screen, self.audioLevel)
					self.explosions.add(explosionSprite)
					self.score += enemy.score

		for powerup in self.powerupGroup:
			player1Hit = pygame.sprite.spritecollide(powerup, self.player1, False)
			if player1Hit:
				powerupType = powerup.powerupType
				powerup.kill()
				if powerupType == "shield":
					self.player1Sprite.foreShields = 2
					self.player1Sprite.aftShields = 2
				elif powerupType == "missle":
					if self.player1Sprite.leftMissles < 2:
						self.player1Sprite.leftMissles += 1
					elif self.player1Sprite.rightMissles < 2:
						self.player1Sprite.rightMissles += 1
			player2Hit = pygame.sprite.spritecollide(powerup, self.player2, False)
			if player2Hit:
				powerupType = powerup.powerupType
				powerup.kill()
				if powerupType == "shield":
					self.player2Sprite.foreShields = 2
					self.player2Sprite.aftShields = 2
				elif powerupType == "missle":
					if self.player2Sprite.leftMissles < 2:
						self.player2Sprite.leftMissles += 1
					elif self.player2Sprite.rightMissles < 2:
						self.player2Sprite.rightMissles += 1


	def checkGameOver(self):
		if not self.player1 and not self.player2:
			self.gameOver = True
			self.gameOverTime = pygame.time.get_ticks()
			self.lastScore = self.score
			self.updateHighScores()

	def gameOverDisplay(self):
		currentTime = pygame.time.get_ticks()
		if currentTime < self.gameOverTime + self.gameOverTimer:
			self.screen.blit(self.gameOverSurface, self.gameOverRect)
		else:
			self.resetGame()

	def checkSectorOver(self):
		if self.totalSectorEnemies <= 0 and not self.enemies:
			self.displaySector = True
			self.sectorStartTime = pygame.time.get_ticks()
			self.liveEnemies = 0
			for star in self.stars:
				star.speed = 30

	def sectorDisplay(self):
		currentTime = pygame.time.get_ticks()
		if currentTime < self.sectorStartTime + self.sectorDisplayTimer:
			self.screen.blit(self.sectorSurface, self.sectorRect)
		else:
			self.sector = self.sector + 1
			self.sectorSurface = self.font.render(str("Sector ") + str(self.sector), False, (255,255,255))
			self.totalSectorEnemies = self.baseSectorEnemies + (self.sector * 10)
			self.displaySector = False
			for star in self.stars:
				star.speed = 1

	def resetGame(self):
		for enemy in self.enemies:
			enemy.kill()
		self.currentScreen = 'Splash'
		self.firstPressed = 99 # Used to determine player 1's controller. First person to press start is player 1.
		self.playerOneJoy = 99 # Player joys set to 99 for dynamic controller assignment. Either joy can be player 1. Whoever presses start first is player 1.
		self.playerTwoJoy = 99

		self.playerOneShipChoice = 1 # Used to determine which ship each player has selected on ship select screen
		self.playerTwoShipChoice = 5 # 1=red, 2=blue, 3=green, 4=yellow, 5=press start
		self.playerOneSelected = False # Controls displaying the check mark on the selected ships
		self.playerTwoSelected = False # 

		self.numberOfPlayers = 0
		self.score = 0
		self.gameRunning = False
		self.gameOver = False

		self.sector = 0
		self.sectorSurface = self.font.render(str("Sector ") + str(self.sector), False, (255,255,255))
		self.liveEnemies = 0
		self.totalSectorEnemies = 0

		self.gameMusicPlaying = False
		self.gameMusic.stop()
		self.splashMusic.play(loops = -1)



	def updateHighScores(self):
		try:
			file = open('Saves/HighScores.txt', 'r') # Checks for the file in read mode
		except FileNotFoundError:
			file = open('Saves/HighScores.txt', 'w') # If the file is not found: create file
			file.close()
			file = open('Saves/HighScores.txt', 'r') # Then read file
		text = file.readlines()
		highScores = []
		i = 0
		while i <= len(text) -1:
			score = int(text[i])
			highScores.append(score)
			if len(highScores) > 10:
				highScores.pop(-1)
			i += 1
		file.close()

		highScores.append(self.lastScore)
		highScores.sort(reverse=True)
		if len(highScores) > 10:
			highScores.pop(-1)
		file = open('Saves/HighScores.txt', 'w')
		for score in highScores:
			file.write(str(score) + '\n')
		file.close() # closes file

	def determineEnemyToSpawn(self):
		randomNumber = randint(1,105)
		if randomNumber >= 1 and randomNumber <= 25:
			enemySprite = Enemy(self.screenWidth, self.screenHeight, randint(50, self.screenHeight / 2), -50, 'one', "dive", self.audioLevel)
		elif randomNumber > 25 and randomNumber <= 50:
			enemySprite = Enemy(self.screenWidth, self.screenHeight, randint(50, self.screenHeight / 2), -50, 'two', "dive", self.audioLevel)
		elif randomNumber > 50 and randomNumber <= 75:
			enemySprite = Enemy(self.screenWidth, self.screenHeight, -50, randint(50, self.screenHeight / 2), 'one', "strafe", self.audioLevel)
		elif randomNumber > 75 and randomNumber <= 100:
			enemySprite = Enemy(self.screenWidth, self.screenHeight, -50, randint(50, self.screenHeight / 2), 'two', "strafe", self.audioLevel)
		elif randomNumber > 100 and randomNumber <= 105:
			enemySprite = Enemy(self.screenWidth, self.screenHeight, randint(50, self.screenHeight / 2), -50, 'miniBoss', "miniBoss", self.audioLevel)
		elif randomNumber > 105:
			enemySprite = Enemy(self.screenWidth, self.screenHeight, randint(50, self.screenHeight / 2), -50, 'rockDropper', "rockDropper", self.audioLevel)

		return(enemySprite)


	def spawnEnemies(self):
		if self.displaySector == False:
			currentTime = pygame.time.get_ticks()
			if currentTime > self.lastEnemySpawn + self.enemySpawnDelay:
				if self.liveEnemies < self.maxEnemiesLive and self.totalSectorEnemies > 0:
					self.lastEnemySpawn = pygame.time.get_ticks()
					enemySprite = self.determineEnemyToSpawn()
					self.enemies.add(enemySprite)
					self.liveEnemies = self.liveEnemies + 1
					self.totalSectorEnemies = self.totalSectorEnemies - 1

			
	def update(self):
		if self.gameRunning == True: # If the game is running
			self.screen.blit(self.backgroundSurface,self.backgroundRect)
			self.drawStars()

			if self.gameMusicPlaying == False:
				self.splashMusic.fadeout(300)
				self.gameMusic.play(loops = -1)
				self.gameMusicPlaying = True

			scoreSurface = self.font.render(str(self.score), False, (255,255,255))
			scoreRect = scoreSurface.get_rect(center = (self.screenWidth / 2, 50))
			self.screen.blit(scoreSurface, scoreRect)

			if self.numberOfPlayers > 0: # Draw Player 1 stuff
				self.drawPlayerOneStuff()

			if self.numberOfPlayers > 1: # Draw Player 2 stuff
				self.drawPlayerTwoStuff()

			self.spawnEnemies()
			self.drawEnemyStuff()
			self.checkCollisions()
			self.explosions.update()

			self.powerupGroup.update()
			self.powerupGroup.draw(self.screen)
			
			if self.displaySector == False:
				self.checkSectorOver()
			elif self.displaySector == True:
				self.sectorDisplay()

			if self.gameOver == False:
				self.checkGameOver()
			elif self.gameOver == True:
				self.gameOverDisplay()

		elif self.gameRunning == False: # If the game is not running
			if self.playerOneJoy != 99 and self.playerTwoJoy != 99 and self.playerOneSelected == True and self.playerTwoSelected == True: # Handles starting the game when 2 players are ready
				self.gameRunning = True
				self.createPlayer1()
				self.createPlayer2()
			if self.playerOneJoy != 99 and self.playerTwoJoy == 99 and self.playerOneSelected == True and self.playerTwoSelected == False: # Handles starting the game for one player
				self.gameRunning = True
				self.createPlayer1()