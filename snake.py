import math
import time

import numpy as np
import pygame

from config import *
import objects as obj


# Initialize Pygame
pygame.init()
pygame.font.init()

# Clear debug cmd prompt
os.system("cls")


# Print that the game started
if debug:
	import shutil
	columns = shutil.get_terminal_size((80, 20))[0]
	print('<', '-'*int(0.5*columns-4.5), " BEGIN ", '-'*int(0.5*columns-4), '>', sep='')

print(width, height)

win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Snake!")


def updateWindow():
	'''
	This function checks if the player has quited the game so the pygame
	window exits instead of don't respond. Also this function updates
	the	window and handles the resizing of the window. This function
	needs to be executed every game tick.
	'''
	global width, height
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			sys.exit(0)
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		elif event.type == pygame.VIDEORESIZE:
			width, height = event.size
			if debug:
				print("[*] resizing to", width, height)

	pygame.display.update()
	return width, height




def mainGame(difficulty):
	# Grid
	global width, height
	grid = obj.Grid(0, 0, 0, 0, 21, 21, color=gridColor, boxBorderColor=gridBorderColor)
	grid.width, grid.height = min((width, height))*0.8, min((width, height))*0.8
	grid.x, grid.y = width/2-grid.width/2, height/2-grid.height/2
	grid.updateBoxes()

	# Snake
	snake = obj.Snake(
		[(initSnakeLength-i+1, grid.rows//2) for i in range(initSnakeLength)],				#((4, grid.rows//2), (3, grid.rows//2), (2, grid.rows//2), (1, grid.rows//2)),
		(np.tile((1, 0), (initSnakeLength, 1))),
		grid,
		mapArrayToRainBow(np.linspace(0, 1, initSnakeLength), initSnakeLength)
	)

	newFacing = snake.facing[0]


	start = time.time()
	timePast = 0

	# Main game loop
	while True:
		newTimePast = roundToNearestMultiple(time.time()-start, 1/gamespeed)
		if newTimePast != timePast:		# New game tick
			print("[*] tick", round(timePast, 5))
			snake.facing[0] = newFacing
			if snake.tick():			# Returns if snake has died in that gametick
				return					# If so return TODO: Make it return the score
			timePast = newTimePast
		

		keys = pygame.key.get_pressed()

		if keys[pygame.K_w] or keys[pygame.K_UP] and snake.facing[0].tolist() != [0, 1]:
			newFacing = [0, -1]
		if keys[pygame.K_a] or keys[pygame.K_LEFT] and snake.facing[0].tolist() != [1, 0]:
			newFacing = [-1, 0]
		if keys[pygame.K_s] or keys[pygame.K_DOWN] and snake.facing[0].tolist() != [0, -1]:
			newFacing = [0, 1]
		if keys[pygame.K_d] or keys[pygame.K_RIGHT] and snake.facing[0].tolist() != [-1, 0]:
			newFacing = [1, 0]
		if keys[pygame.K_p]:
			pause(pygame.display.get_surface())


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
	pauseTextLine1 = font.render(f"Paused, click to unpause", True, DARK_BLUE)
	pauseTextLine2 = font.render(f"Hit SPACE to return home", True, DARK_BLUE)
	pauseText = combineSufacesVertical(pauseTextLine1, pauseTextLine2)
	pauseTextAspectRatio = np.divide(*pauseText.get_size()[::-1])

	backgroundImage = PIL_to_surface(changeBrightness(surface_to_PIL(bg), 0.3))

	hover = 0

	frameCount = 1
	while True:
		fpsClock.tick(60)	# Ensures that the game will not play higher than 60 fps
		win.blit(pygame.transform.scale(backgroundImage, (width, height)), (0, 0))

		goldenRatio = (1 + 5 ** 0.5) / 2

		h = max(50*np.sin(frameCount/10) * (1.03**(-frameCount)) + (min((width, height))/2-(1000*1/(2*frameCount))), 0) # y = 50 * sin(x/10) * 1.03^-x + (maxWidth -(1000*1/x))
		w = goldenRatio*h
		maxHover = width/80
		hoverSpeed = maxHover/3	# This ensures a constant magnification time of 0.05 seconds, calculated by (maxHover/hoverSpeed)/fps

		
		pauseButton = obj.Button(pygame.Rect(
			width/2 - w/2 - hover*goldenRatio,		# Make sure the button is centered
			height/2-h/2 - hover,
			w + 2*hover*goldenRatio,
			h + 2*hover
		))

		
		if pauseButton.isHovering(*pygame.mouse.get_pos()):
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


		pauseTextWidth = int(w*0.9 + hover)								# Scle the width to 90% of the pauseButton
		pauseTextHeight = int((w*0.9 + hover)*pauseTextAspectRatio)		# Scale the font but remain the correct aspect ratio

		win.blit(						# Print the pauseText to the screen
			pygame.transform.smoothscale(		# Scaling the surface that contains the font to the correct size
				pauseText,
				(pauseTextWidth, pauseTextHeight)
			),
			(
				(width-pauseTextWidth)/2,
				(height-pauseTextHeight)/2
			)
		)

		frameCount+=1
		updateWindow()

mainGame(-1)