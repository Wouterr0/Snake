import math

import numpy as np
import pygame

from config import *
import objects as obj

# Grid
grid = obj.Grid(0, 0, 0, 0, 11, 11)
grid.width, grid.height = min((width, height))*0.8, min((width, height))*0.8
grid.x, grid.y = width/2-grid.width/2, height/2-grid.height/2
grid.rows, grid.columns = 11, 11
grid.updateBoxes()

# Snake
snake = obj.Snake((
	(3, grid.rows//2),
	(2, grid.rows//2),
	(1, grid.rows//2)),
		grid, np.full((3, 4), RED, dtype=np.uint8))


# Main game loop
while True:
	from config import *

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