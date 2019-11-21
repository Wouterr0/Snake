import math
import time

import numpy as np
import pygame

from config import *
import objects as obj

# Grid
grid = obj.Grid(0, 0, 0, 0, 21, 21)
grid.width, grid.height = min((width, height))*0.8, min((width, height))*0.8
grid.x, grid.y = width/2-grid.width/2, height/2-grid.height/2
grid.updateBoxes()

# Snake
snake = obj.Snake(
	((4, grid.rows//2), (3, grid.rows//2), (2, grid.rows//2), (1, grid.rows//2)),
	((1, 0), (1, 0), (1, 0), (1, 0)),
	grid,
	np.full((4, 4), RED, dtype=np.uint8)
)


start = time.time()
timePast = 0

# Main game loop
while True:
	from config import *

	newTimePast = roundToNearestMultiple(time.time()-start, 1/gamespeed)
	if newTimePast != timePast:			# New game tick
		print("[*] tick", round(timePast, 5))
		if snake.tick():
			break
		timePast = newTimePast
	
		if pygame.key.get_pressed()[pygame.K_SPACE]:
			snake.eat(np.vstack((snake.colors, RED)))
	

	keys = pygame.key.get_pressed()

	if keys[pygame.K_w] or keys[pygame.K_UP]:
		snake.facing[0] = [0, -1]
	if keys[pygame.K_a] or keys[pygame.K_LEFT]:
		snake.facing[0] = [-1, 0]
	if keys[pygame.K_s] or keys[pygame.K_DOWN]:
		snake.facing[0] = [0, 1]
	if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
		snake.facing[0] = [1, 0]
	


	# Making sure that the game plays at a stable fps
	fpsClock.tick(60)

	# Fill the background
	win.fill(BLACK)

	# Making sure the grid is propperly resized
	grid.width, grid.height = min((width, height))*0.8, min((width, height))*0.8
	grid.x, grid.y = width/2-grid.width/2, height/2-grid.height/2
	
	# Draw everything
	grid.draw(win)
	snake.draw()


	updateWindow()

# pygame.quit()
while True:
	updateWindow()
