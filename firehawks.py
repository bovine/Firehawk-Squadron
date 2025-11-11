import pygame
import sys
from pygame.locals import *
from os import path
from game import Game
from button import *

pygame.init()
pygame.display.set_caption('Firehawk Squadron')
displayInfo = pygame.display.Info() # Gets the current resolution information of the monitor
screenWidth = displayInfo.current_w # Gets screen width from the displayInfo 
screenHeight = displayInfo.current_h # Gets screen height from the displayInfo 
screen = pygame.display.set_mode((screenWidth,screenHeight))
clock = pygame.time.Clock()
font = pygame.font.Font('Assets/Font/kenvector_future.ttf',50)

highScores = []

# initialize joysticks then print the joystick names
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
	print(joystick.get_name())

# Buttons --------------------------------------------------------------------------------------
buttons = pygame.sprite.Group()
highScoreButton = Button('inactive', (50, screenHeight - 300), 'High Scores')
buttons.add(highScoreButton)
controlsButton = Button('inactive', (50, screenHeight - 250), 'Controls')
buttons.add(controlsButton)
optionsButton = Button('inactive', (50, screenHeight - 200), 'Options')
buttons.add(optionsButton)
creditsButton = Button('inactive', (50, screenHeight - 150), 'Credits')
buttons.add(creditsButton)
quitButton = Button('inactive', (50, screenHeight - 100), 'Quit')
buttons.add(quitButton)

backButtons = pygame.sprite.Group()
backButton = Button('inactive', (screenWidth - 300, screenHeight - 100), 'Back')
backButtons.add(backButton)
# END Buttons --------------------------------------------------------------------------------------

# Options screen elements --------------------------------------------------------------------------------------
audioSurface = font.render(('Audio Level'), False, (255,255,255))
audioRect = audioSurface.get_rect(topleft = (200,screenHeight / 4))

audioLevelSurface = font.render(str(50), False, (255,255,255))
audioLevelRect = audioLevelSurface.get_rect(topleft = (900, screenHeight / 4))

arrowButtons = pygame.sprite.Group()
downTenButton = ArrowButton('inactive', (650,screenHeight / 4), -10)
arrowButtons.add(downTenButton)
downOneButton = ArrowButton('inactive', (750,screenHeight / 4), -1)
arrowButtons.add(downOneButton)
upTenButton  = ArrowButton('inactive', (1050,screenHeight / 4), 10)
arrowButtons.add(upTenButton)
upOneButton  = ArrowButton('inactive', (1150,screenHeight / 4), 1)
arrowButtons.add(upOneButton)

optionsSaveButtonGroup = pygame.sprite.Group()
optionsSaveButton = Button('inactive', (screenWidth / 2, screenHeight / 2), 'Save')
optionsSaveButtonGroup.add(optionsSaveButton)

# Load ship images for ship select screen ----------------------------------------------------------
playerRedSurface = pygame.image.load('Assets/Images/Player/PlayerRed.png').convert_alpha() 
playerRedSurface = pygame.transform.scale(playerRedSurface, (400, 400))
playerRedRect = playerRedSurface.get_rect(topleft = (0,0))

playerBlueSurface = pygame.image.load('Assets/Images/Player/PlayerBlue.png').convert_alpha() 
playerBlueSurface = pygame.transform.scale(playerBlueSurface, (400, 400)) 
playerBlueRect = playerBlueSurface.get_rect(topleft = (0,0))

playerGreenSurface = pygame.image.load('Assets/Images/Player/PlayerGreen.png').convert_alpha() 
playerGreenSurface = pygame.transform.scale(playerGreenSurface, (400, 400)) 
playerGreenRect = playerGreenSurface.get_rect(topleft = (0,0))

playerYellowSurface = pygame.image.load('Assets/Images/Player/PlayerYellow.png').convert_alpha() 
playerYellowSurface = pygame.transform.scale(playerYellowSurface, (400, 400)) 
playerYellowRect = playerYellowSurface.get_rect(topleft = (0,0))

pressStartSurface = pygame.image.load('Assets/Images/Player/PressStart.png').convert_alpha() # Press Start message for player 2 on ship select page
pressStartSurface = pygame.transform.scale(pressStartSurface, (400, 400)) 
pressStartRect = pressStartSurface.get_rect(topleft = (0,0))

# Ship select screen UI elements
outlineSurface = pygame.image.load('Assets/Images/UI/outline.png').convert_alpha() # Surrounds the ships on ship select page
checkSurface = pygame.image.load('Assets/Images/UI/check.png').convert_alpha() # Check mark for selected ship

# END Ship images --------------------------------------------------------------------------------------

# player motion setup
player1Motion = [0, 0]
player2Motion = [0, 0]

# EVENT HANDLING --------------------------------------------------------------------------------------
def eventHandlingNotRunning(game): # Handles window events and game input when a game is not running
	for event in pygame.event.get():
		#print(event)
		if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and game.currentScreen == 'Splash': # The window's X is clicked or escape button is pressed
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and game.currentScreen == 'ShipSelect': # Escape from ship select screen
			game.firstPressed = 99
			game.playerOneJoy = 99
			game.playerTwoJoy = 99
			game.playerOneShipChoice = 1
			game.playerTwoShipChoice = 5
			game.playerOneSelected = False
			game.playerTwoSelected = False
			game.currentScreen = 'Splash'
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and game.currentScreen != 'Splash': # Escape from all screens except splash
			game.currentScreen = 'Splash'
		elif game.firstPressed == 99 and event.type == JOYBUTTONDOWN and event.button == 7: # Assignment for player 1
			game.firstPressed = 0
			game.playerOneJoy = event.joy
			game.currentScreen = 'ShipSelect'
		elif game.firstPressed != 99 and event.type == JOYBUTTONDOWN and event.button == 7 and event.joy != game.playerOneJoy: # Assignment for player 2
			game.playerTwoJoy = event.joy
			playerTwoShipChoice = 1
			if game.playerTwoShipChoice == game.playerOneShipChoice:
				game.playerTwoShipChoice = game.playerTwoShipChoice + 1
			if game.playerTwoShipChoice > 4:
				game.playerTwoShipChoice = 1
			if game.playerTwoShipChoice == game.playerOneShipChoice:
				game.playerTwoShipChoice = game.playerTwoShipChoice + 1
		elif game.currentScreen == 'ShipSelect': # Handles the selection of ships for both players on the ship select screen
			if event.type == JOYBUTTONDOWN and event.joy == game.playerOneJoy and game.playerOneSelected == False:
				if event.button != 0: # Any button but green
					game.playerOneShipChoice = game.playerOneShipChoice + 1
					if game.playerOneShipChoice == game.playerTwoShipChoice: # Prevents player 1 from selecting the same ship as player 2
						game.playerOneShipChoice = game.playerOneShipChoice + 1
					if game.playerOneShipChoice > 4:
						game.playerOneShipChoice = 1
				elif event.button == 0:
					game.playerOneSelected = True
					game.numberOfPlayers = game.numberOfPlayers + 1
			elif event.type == JOYBUTTONDOWN and event.joy == game.playerTwoJoy and game.playerTwoSelected == False:
				if event.button != 0: # Any button but green
					game.playerTwoShipChoice = game.playerTwoShipChoice + 1
					if game.playerTwoShipChoice == game.playerOneShipChoice: # Prevents player 2 from selecting the same ship as player 1
						game.playerTwoShipChoice = game.playerTwoShipChoice + 1
					if game.playerTwoShipChoice > 4:
						game.playerTwoShipChoice = 1
				if event.button == 0:
					game.playerTwoSelected = True
					game.numberOfPlayers = game.numberOfPlayers + 1
			if game.playerTwoShipChoice == game.playerOneShipChoice: # Prevents a rare bug when both players press the buttons at the same time.
				game.playerTwoShipChoice = game.playerTwoShipChoice + 1
		elif event.type == MOUSEBUTTONDOWN and game.currentScreen == 'Splash':
			for b in buttons:
				if b.active == 'active':
					game.currentScreen = b.label
					if b.label == 'Quit':
						pygame.quit()
						sys.exit()
		elif event.type == MOUSEBUTTONDOWN and game.currentScreen != 'Splash' and game.currentScreen != 'Options':
			for b in backButtons:
				if b.active == 'active':
					game.currentScreen = 'Splash'
		elif event.type == MOUSEBUTTONDOWN and game.currentScreen == 'Options': # Handles arrow button clicks in options screen
			for b in arrowButtons:
				if b.active == 'active':
					b.clicked = True
			for b in optionsSaveButtonGroup:
				if b.active == 'active':
					b.clicked = True
			for b in backButtons:
				if b.active == 'active':
					game.currentScreen = 'Splash'

def eventHandlingRunning(game): # Handles window events and game input when a game is running
	for event in pygame.event.get():
		if event.type == JOYAXISMOTION:
			if event.joy == game.playerOneJoy and game.player1Sprite.alive == True: # Joystick axis controls player 1
				if event.axis < 2:
					player1Motion[event.axis] = event.value
				elif event.axis == 4:
					game.player1Sprite.fireMissle("left")
				elif event.axis == 5:
					game.player1Sprite.fireMissle("right")
			elif event.joy == game.playerTwoJoy and game.player2Sprite.alive == True: # Joystick axis controls player 2
				if event.axis < 2:
					player2Motion[event.axis] = event.value
				elif event.axis == 4:
					game.player2Sprite.fireMissle("left")
				elif event.axis == 5:
					game.player2Sprite.fireMissle("right")
		elif event.type == JOYBUTTONDOWN and event.joy == game.playerOneJoy and game.player1Sprite.alive == True:
			if event.button == 0: # Player 1 shooting
				game.player1Sprite.shoot()
			elif event.button == 4 or event.button == 5 and game.player1Sprite.isRotating == False: # Player 1 shield rotation
				game.player1Sprite.rotateShields()
		elif event.type == JOYBUTTONDOWN and event.joy == game.playerTwoJoy and game.player2Sprite.alive == True:
			if event.button == 0: # Player 2 shooting
				game.player2Sprite.shoot()
			elif event.button == 4 or event.button == 5 and game.player2Sprite.isRotating == False: # Player 2 shield rotation
				game.player2Sprite.rotateShields()
		elif game.firstPressed != 99 and event.type == JOYBUTTONDOWN and event.button == 7 and event.joy != game.playerOneJoy: # If the game is started and player 2 wants to join. Setup player 2 and auto assign ship.
			game.playerTwoJoy = event.joy
			game.numberOfPlayers = game.numberOfPlayers + 1
			if game.playerOneShipChoice > 1:
				game.playerTwoShipChoice = 1
			else:
				game.playerTwoShipChoice = 2
			game.createPlayer2()
		elif event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # ESC closes the program -- needs to change later
			pygame.quit()
			sys.exit()

# END EVENT HANDLING --------------------------------------------------------------------------------------

def screenDisplay(game): # Handles which window screen to display if the game is not running (Splash, Controls, Credits, High Scores)
	if game.currentScreen == 'Splash':
		screen.blit(game.splashSurface,game.splashRect)
		if game.lastScore > 0:
			lastScoreSurface = font.render('Last Score: ' + str(game.lastScore), False, (255,255,255))
			lastScoreRect = lastScoreSurface.get_rect(center = (screenWidth / 2, 50))
			screen.blit(lastScoreSurface, lastScoreRect)
		buttons.update()
		buttons.draw(screen)
		for b in buttons:
			b.addLabel(screen)
	elif game.currentScreen == 'High Scores':
		screen.blit(game.highScoresSurface,game.highScoresRect)
		displayHighScores()
	elif game.currentScreen == 'Controls':
		screen.blit(game.controlsSurface,game.controlsRect)
	elif game.currentScreen == 'Options':
		screen.blit(game.optionsSurface,game.optionsRect)
		optionsScreen()
	elif game.currentScreen == 'Credits':
		screen.blit(game.creditsSurface,game.creditsRect)
	elif game.currentScreen == 'ShipSelect':
		screen.blit(game.shipSelectSurface,game.shipSelectRect)
		shipSelect(game)
	if game.currentScreen != 'Splash' and game.currentScreen != 'ShipSelect': # Display back button for all non-splash and non-shipSelct pages
		backButtons.update()
		backButtons.draw(screen)
		for b in backButtons:
			b.addLabel(screen)

def shipSelect(game): # handles displaying the currently selected ship for each player on the ship select screen
	playerOneShipLoc = (screenWidth / 8,screenHeight / 3)
	playerTwoShipLoc = (screenWidth / 8 * 5,screenHeight / 3)

	playerOneOutlineLoc = (screenWidth / 8 - 10,screenHeight / 3 - 10)
	playerTwoOutlineLoc = (screenWidth / 8 * 5 - 10,screenHeight / 3 - 10)

	screen.blit(outlineSurface,playerOneOutlineLoc)
	screen.blit(outlineSurface,playerTwoOutlineLoc)

	if game.playerOneShipChoice == 1:
		screen.blit(playerRedSurface,playerOneShipLoc)
	elif game.playerOneShipChoice == 2:
		screen.blit(playerBlueSurface,playerOneShipLoc)
	elif game.playerOneShipChoice == 3:
		screen.blit(playerGreenSurface,playerOneShipLoc)
	elif game.playerOneShipChoice == 4:
		screen.blit(playerYellowSurface,playerOneShipLoc)

	if game.playerTwoShipChoice == 1:
		screen.blit(playerRedSurface,playerTwoShipLoc)
	elif game.playerTwoShipChoice == 2:
		screen.blit(playerBlueSurface,playerTwoShipLoc)
	elif game.playerTwoShipChoice == 3:
		screen.blit(playerGreenSurface,playerTwoShipLoc)
	elif game.playerTwoShipChoice == 4:
		screen.blit(playerYellowSurface,playerTwoShipLoc)
	elif game.playerTwoShipChoice == 5:
		screen.blit(pressStartSurface,playerTwoShipLoc)

	if game.playerOneSelected == True:
		screen.blit(checkSurface,playerOneShipLoc)
	if game.playerTwoSelected == True:
		screen.blit(checkSurface,playerTwoShipLoc)

def resetPlayerMotion(): # Reset motion to 0 when axis value gets too low. prevents joystick drifting.
	if game.numberOfPlayers > 0:
		if abs(player1Motion[0]) < 0.1:
			player1Motion[0] = 0
		if abs(player1Motion[1]) < 0.1:
			player1Motion[1] = 0	

	if game.numberOfPlayers > 1:
		if abs(player2Motion[0]) < 0.1:
			player2Motion[0] = 0
		if abs(player2Motion[1]) < 0.1:
			player2Motion[1] = 0

def readHighScores():
	highScores = []
	try:
		file = open('Saves/HighScores.txt', 'r') # Checks for the file in read mode
	except FileNotFoundError:
		file = open('Saves/HighScores.txt', 'w') # If the file is not found: create file
		file.close()
		file = open('Saves/HighScores.txt', 'r') # Then read file
	text = file.readlines()
	i = 0
	while i <= len(text) -1:
		score = int(text[i])
		highScores.append(score)
		if len(highScores) > 10:
			highScores.pop(-1)
		i += 1
	file.close()
	return highScores

def displayHighScores():
   	YPosition = 250
   	i = 0
   	highScores = readHighScores()
   	while i <= len(highScores) - 1:
   		if highScores[i] == game.lastScore:
   			scoreText = font.render(str(highScores[i]), False,(0,255,0))
   		else:
   			scoreText = font.render(str(highScores[i]), False,(255,255,255))
   		scoreTextRect = scoreText.get_rect(center = (screenWidth / 2,YPosition))
   		screen.blit(scoreText,scoreTextRect)
   		YPosition += 90
   		i += 1

def optionsScreen():
	game.audioLevel = game.audioLevel * 100
	screen.blit(audioSurface,audioRect)
	arrowButtons.update()
	arrowButtons.draw(screen)
	audioLevelSurface = font.render(str(int(game.audioLevel)), False, (255,255,255))
	screen.blit(audioLevelSurface,audioLevelRect)
	for b in arrowButtons:
		if b.clicked == True:
			b.clicked = False
			game.audioLevel = game.audioLevel + b.value
			if game.audioLevel < 0:
				game.audioLevel = 0
			if game.audioLevel > 100:
				game.audioLevel = 100
	game.audioLevel = game.audioLevel / 100
	optionsSaveButtonGroup.update()
	optionsSaveButtonGroup.draw(screen)
	for b in optionsSaveButtonGroup:
		b.addLabel(screen)
		if b.clicked == True:
			b.clicked = False
			setAudioLevel(game.audioLevel)

def getAudioLevel():
	try:
		optionsFile = open('Options/Options.txt', 'r') # Checks for the file in read mode
	except FileNotFoundError:
		optionsFile = open('Options/Options.txt', 'w')
		optionsFile.write(str(.5))
		optionsFile.close()
		optionsFile = open('Options/Options.txt', 'r')
	text = optionsFile.readlines()
	audioLevel = text[0]
	audioLevel = float(audioLevel)
	return(audioLevel)

def setAudioLevel(audioLevel):
	optionsFile = open('Options/Options.txt', 'w')
	optionsFile.write(str(game.audioLevel))
	optionsFile.close()
	game.setAudioLevel()

audioLevel = getAudioLevel()
game = Game(screen, screenWidth, screenHeight, audioLevel)

while True:
	if game.gameRunning == True:
		resetPlayerMotion()
		eventHandlingRunning(game)
		if game.numberOfPlayers > 0:
			game.player1Sprite.update(player1Motion) # Update player 1
		if game.numberOfPlayers > 1:
			game.player2Sprite.update(player2Motion) # Update player 2
	elif game.gameRunning == False:
		eventHandlingNotRunning(game) # Handles window events and game input
		screenDisplay(game) # Displays any non-game screen (Splash, Controls, Credits, Options, High Scores)

		player1Motion = [0, 0] # Needed to reset motion between games.
		player2Motion = [0, 0]

	game.update()
	pygame.display.flip()
	clock.tick(60)


