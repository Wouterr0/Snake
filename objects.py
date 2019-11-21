import random

import numpy as np
import pygame

import config as cfg


class Box(pygame.Rect):
	'''
	The Box object represents on box on a grid

	'''
	def __init__(self, x, y, w, h, lineWidth, color=cfg.GREEN):
		self.color = color
		self.edgeColor = cfg.DARK_GREEN
		
		self.x = int(x)
		self.y = int(y)
		self.width = w
		self.height = h

		self.lineWidth = int(lineWidth)
		super().__init__(self.x, self.y, self.width, self.height)
	
	def draw(self, surface: pygame.Surface):
		pygame.draw.rect(surface, self.color, self)							# Draw box
		pygame.draw.rect(surface, self.edgeColor, self, self.lineWidth)		# Draw border




class Grid:
	'''
	The Grid object represents a grid full of boxes

	'''
	def __init__(self, x, y, w, h, rows, cols):
		self.x = x
		self.y = y

		self.width = int(w)
		self.height = int(h)

		self.rows = int(rows)
		self.columns = int(cols)

		self.updateBoxes()
		
	def __str__(self):
	 return f"Grid(x={self.x}, y={self.y}, width={self.width}, height={self.height}, rows={self.rows}, cols={self.columns})"

	def __getitem__(self, boxIndex):
		return self.boxes[boxIndex]

	def __setitem__(self, boxIndex, newBox):
		self.boxes[boxIndex] = newBox


	def updateBoxes(self):
		self.boxes = np.ndarray((self.rows, self.columns), dtype=Box)
		self.boxWidth = self.width//self.columns
		self.boxHeight = self.height//self.rows

		for row in range(self.rows):
			for column in range(self.columns):
				self.boxes[row, column] = Box(self.x+self.boxWidth*column, self.y+self.boxHeight*row, self.boxWidth, self.boxHeight, self.width//150+1)


	def draw(self, surface: pygame.Surface):
		'''
		Draws all the boxes in the grid
		
		'''
		self.updateBoxes()
		for row in range(self.rows):
			for column in range(self.columns):
				self.boxes[row, column].draw(surface)




class Snake:
	def __init__(self, shape, facing, grid: Grid, colors):
		self.grid = grid
		self.length = len(shape)
		self.shape = np.array(shape)
		self.facing = np.array(facing)
		self.apple = None
		self.colors = colors

		self.updateBody()
		self.generateApple()


	def updateBody(self):
		self.body = np.empty((len(self.shape)), dtype=Box)
		i = 0
		for x, y in self.shape:
			self.body[i] = self.grid[y][x]
			i+=1

	def draw(self):
		self.updateBody()
		for i, rect in enumerate(self.body):
			pygame.draw.rect(cfg.win, self.colors[i], rect)
		if self.apple:
			self.apple.draw()

	def tick(self):
		for i in range(len(self.shape)):
			self.shape[i] = np.add(self.shape[i], self.facing[i])
		self.facing[1:] = self.facing[:-1]

		if any(pos[0] < 0 or pos[0] >= self.grid.rows or pos[1] < 0 or pos[1] >= self.grid.columns for pos in self.shape) or not cfg.unique(self.shape.tolist()):
			return 1

		if self.grid.boxes[self.shape[0][1], self.shape[0][0]] == self.grid.boxes[self.apple.column, self.apple.row]:
			print("EAT")

		self.updateBody()

	def generateApple(self, amount=1):
		possibleSpawnLocations = np.dstack(np.mgrid[0:self.grid.columns, 0:self.grid.rows])
		mask = np.zeros((self.grid.rows, self.grid.columns), dtype=bool)
		mask[self.shape.T[0], self.shape.T[1]] = True
		possibleSpawnLocations = possibleSpawnLocations[~mask]
		self.apple = Apple(*random.choice(possibleSpawnLocations), self.grid)
	
	
	def eat(self, newColors, amount=1):
		print(f"[*] growing by {amount}")
		for _ in range(amount):
			self.shape = np.vstack((self.shape, np.add(np.multiply(self.facing[-1], -1), self.shape[-1])))
			self.facing = np.vstack((self.facing, self.facing[-1]))
			self.colors = newColors

		self.updateBody()




class Apple:
	def __init__(self, column, row, grid, img=cfg.apple_image):
		self.column = column
		self.row = row
		self.grid = grid

		self.image = img

	def draw(self):
		img = self.image.resize((int(self.grid.boxWidth), int(self.grid.boxHeight)))
		cfg.win.blit(cfg.PIL_to_surface(img), self.grid[self.column, self.row])

