import math
import time
import csv
import sys

import numpy as np
import pygame
import pygame_gui

from config import *
import objects as obj


# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Clear debug cmd prompt
os.system("cls")

# Get username
if len(sys.argv) <= 1:
	username = None
else:
	username = sys.argv[1]


# Print that the game started
import shutil
columns = shutil.get_terminal_size((80, 20))[0]
print('<', '-'*int(0.5*columns-4.5), " BEGIN ", '-'*int(0.5*columns-4), '>', sep='')


win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
manager = pygame_gui.UIManager((width, height))
pygame.display.set_caption("Snake!")


def updateWindow():
	'''
	This function checks if the player has quited the game so the pygame
	window exits instead of don't respond. Also this function updates
	the	window and handles the resizing of the window. This function
	needs to be executed every game tick.
	'''
	global width, height
	global manager

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			sys.exit(0)
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		elif event.type == pygame.VIDEORESIZE:
			width, height = event.size
			print("[*] resizing to", width, height)
		
		manager.process_events(event)

	pygame.display.flip()
	return width, height

def saveScore(username, score, difficulty, berryMode):
	with open('highscore.csv', 'a', newline='') as f:
		writer = csv.writer(f)
		writer.writerow([username, difficulty, berryMode, score])


def home():
	playText = pygame.font.Font(gameFont, 200).render("PLAY", True, WHITE)
	berryMode = False

	slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
		pygame.Rect(
			(width-(width/2*GOLDENRATIO))/2,
			0,
			width/2*GOLDENRATIO,
			height/20
		),
		1,			# default
		(1, 10),	# range
		manager
	)
	
	fpsClock = pygame.time.Clock()
	
	while True:
		fpsClock.tick(maxFPS)	# Ensures that the game will not play higher than maxFPS fps

		background = repeatTileImage(
			startBgImage.resize(
				(np.array(startBgImage.size) * 2).astype(int)
			),
			(width, height)
		)

		# Check if the B key is pressed to activate berry mode
		if pygame.key.get_pressed()[pygame.K_b]:
			berryMode = not berryMode
			time.sleep(0.2)

		# Draw background
		win.blit(pygame.transform.scale2x(PIL_to_surface(background)), (0, 0))

		# Update and draw playButton with playText and difficultyText on it
		difficulty = int(round(slider.get_current_value()))
		difficultyText = pygame.font.Font(gameFont, 200).render("level " + str(difficulty) + (('B' if berryMode else ('' if difficulty==10 else ' '))), True, WHITE)
		fullPlayText = combineSufacesVertical(playText, difficultyText)
		
		_width, _height = min((width, height))/2*GOLDENRATIO, min((width, height))/2
		
		playTextWidth = int(_width*0.9)
		playTextHeight = int(_height*0.9)

		playButton = obj.Button(
			pygame.Rect(
				(width-_width)/2,
				(height-_height)/2,
				_width,
				_height
			),
			pygame.transform.smoothscale(fullPlayText, (playTextWidth, playTextHeight)) # Resize playText to fit nice in the startButton
		)

		# Update pygame_gui
		slider.update(1/maxFPS)
		manager.update(1/maxFPS)



		if playButton.hover(pygame.mouse.get_pos()):
			playButton.color = (145, 34, 0)
			if pygame.mouse.get_pressed()[0]:
				slider.kill()
				return difficulty, berryMode
		else:
			playButton.color = (123, 17, 19)

		# Draw stuff
		playButton.draw(win)
		manager.draw_ui(win)

		updateWindow()


def snake(difficulty, berryMode):
	# Grid
	global width, height
	gridColor = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
	gridBorderColor = (np.array(gridColor)*0.7).tolist()
	
	gridSize = -2*difficulty+29 # Calculate grid size with the formula: gridSize = -2 * difficulty + 29
	print("[*] gridSize =", gridSize)
	print("[*] difficulty = ", difficulty)

	grid = obj.Grid(0, 0, 0, 0, gridSize//2*3 if berryMode else gridSize, gridSize, color=gridColor, boxBorderColor=gridColor if berryMode else gridBorderColor)
	grid.width, grid.height = min((width, height))*0.8, min((width, height))*0.8
	grid.x, grid.y = width/2-grid.width/2, height/2-grid.height/2
	grid.updateBoxes()

	# Snake
	snake = obj.Snake(
		[(initSnakeLength-i+1, grid.rows//2) for i in range(initSnakeLength)],
		(np.tile((1, 0), (initSnakeLength, 1))),
		grid,
		mapArrayToRainBow(np.linspace(0, 1, initSnakeLength), initSnakeLength),
		berryHeadImage if berryMode else snakeHeadImage,	# Snake head image
		berryFruitImage if berryMode else appleImage,		# Apple image
		berryPickupSound if berryMode else applePickupSound # pickup sound
	)

	newFacing = snake.facing[0] # newFacing is the current firs facing and is updated to snake.facing[0] every gametick


	start = time.time()
	timePast = 0

	# Main game loop
	while True:
		newTimePast = roundToNearestMultiple(time.time()-start, 1/gamespeed)
		if newTimePast != timePast:		# New game tick
			print("[*] tick", round(timePast, 5))
			snake.facing[0] = newFacing

			if snake.tick():			# Checks if snake has died in that gametick
				return snake.score, difficulty, berryMode
			timePast = newTimePast
		

		keys = pygame.key.get_pressed()

		if (keys[pygame.K_w] or keys[pygame.K_UP]) and snake.facing[0].tolist() != [0, 1]:
			newFacing = [0, -1]
		if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and snake.facing[0].tolist() != [1, 0]:
			newFacing = [-1, 0]
		if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and snake.facing[0].tolist() != [0, -1]:
			newFacing = [0, 1]
		if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and snake.facing[0].tolist() != [-1, 0]:
			newFacing = [1, 0]
		if keys[pygame.K_p]:
			if pause(pygame.display.get_surface()):
				return snake.score, difficulty, berryMode


		# Fill the background
		win.fill(BLACK)

		# Making sure the grid is propperly resized
		grid.width, grid.height = min((width, height))*0.8, min((width, height))*0.8
		grid.x, grid.y = width/2-grid.width/2, height/2-grid.height/2
		
		# Draw everything
		grid.draw(win)
		snake.draw(win)

		# Display the score
		scoreFont = pygame.font.Font(gameFont, min((width, height))//10)
		scoreText = scoreFont.render(str(snake.score), True, WHITE)
		win.blit(scoreText, ((width - scoreText.get_width())/2, 0))
		
		width, height = updateWindow()


def pause(bg):
	'''
	The function responsable for the pause menu.
	
	The pause manu rect has a golden ratio and the height is:
	`50*np.sin(i/10) * (1.02**(-i)) + (400-(1000*1/i))`
	but it's never smaler than 0.
	'''
	fpsClock = pygame.time.Clock()
	font = pygame.font.Font(gameFont, 200)

	# Rendering it firs so I can scale the surface instead of the font beacause then it would be really not smooth
	pauseTextLine1 = font.render(f"Paused, click to continue", True, DARK_BLUE)
	pauseTextLine2 = font.render(f"Hit SPACE to return home", True, DARK_BLUE)
	pauseText = combineSufacesVertical(pauseTextLine1, pauseTextLine2)
	pauseTextAspectRatio = np.divide(*pauseText.get_size()[::-1])

	backgroundImage = PIL_to_surface(changeBrightness(surface_to_PIL(bg), 0.3))

	hover = 0

	frameCount = 1
	while True:
		fpsClock.tick(maxFPS)	# Ensures that the game will not play higher than maxFPS fps
		win.blit(pygame.transform.scale(backgroundImage, (width, height)), (0, 0))

		h = max(50*np.sin(frameCount/10) * (1.03**(-frameCount)) + (min((width, height))/2-(1000*1/(2*frameCount))), 0) # y = 50 * sin(x/10) * 1.03^-x + (maxWidth -(1000*1/x))
		w = GOLDENRATIO*h
		maxHover = width/80
		hoverSpeed = maxHover/3	# This ensures a constant magnification time of 0.05 seconds, calculated by (maxHover/hoverSpeed)/fps

		pauseTextWidth = int(w*0.9 + hover)								# Scle the width to 90% of the pauseButton
		pauseTextHeight = int((w*0.9 + hover)*pauseTextAspectRatio)		# Scale the font but remain the correct aspect ratio

		pauseButton = obj.Button(
			pygame.Rect(
				width/2 - w/2 - hover*GOLDENRATIO,		# Make sure the button is centered
				height/2-h/2 - hover,
				w + 2*hover*GOLDENRATIO,
				h + 2*hover
			),
			pygame.transform.smoothscale(pauseText, (pauseTextWidth, pauseTextHeight))
		)

		if pygame.key.get_pressed()[pygame.K_SPACE]:
			return -1
		
		if pauseButton.hover(pygame.mouse.get_pos()):
			if pygame.mouse.get_pressed()[0]:
				return
			pauseButton.color = (110, 166, 255)
			hover += hoverSpeed
			hover = min(hover, maxHover)
		else:
			pauseButton.color = (66, 135, 245)
			hover -= hoverSpeed
			hover = max(hover, 0)

		pauseButton.draw(win)

		frameCount+=1
		updateWindow()

while True:
	score, difficulty, berryMode = snake(*home())
	print("[*] Score was {} on difficulty {} with berry mode {}".format(score, difficulty, "on" if berryMode else "off"))
	if username:
		saveScore(username, score, difficulty, berryMode)