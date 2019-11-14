import numpy as np

import pygame

import config as cfg


class Box(cfg.pygame.Rect):
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
		self.isBodyPart = False
		self.lineWidth = int(lineWidth)
		super().__init__(self.x, self.y, self.width, self.height)
	
	def draw(self, surface: cfg.pygame.Surface):
		cfg.pygame.draw.rect(surface, self.color, self)
		cfg.pygame.draw.rect(surface, self.edgeColor, self, self.lineWidth)



class Grid:
	'''
	The Grid object represents a grid full of boxes

	'''
	def __init__(self, x, y, w, h, rows, cols):
		self.x = x
		self.y = y

		self.width = w
		self.height = h

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
		self.boxWidth = self.width/self.columns
		self.boxHeight = self.height/self.rows

		for row in range(self.rows):
			for column in range(self.columns):
				self.boxes[row, column] = Box(self.x+self.boxWidth*column, self.y+self.boxHeight*row, self.boxWidth, self.boxHeight, self.width//150+1)


	def draw(self, surface: cfg.pygame.Surface):
		'''
		Draws all the boxes in the grid
		
		'''
		self.updateBoxes()
		for row in range(self.rows):
			for column in range(self.columns):
				self.boxes[row, column].draw(surface)



class Snake:
	def __init__(self, shape, grid: Grid, colors):
		self.grid = grid
		self.length = len(shape)
		self.facing = (0, 1)
		self.shape = shape
		self.body = np.empty((len(shape)), dtype=Box)
		self.colors = colors

		self.updateBody()


	def updateBody(self):
		i = 0
		for x, y in self.shape:
			self.body[i] = self.grid[y][x]
			i+=1

	def draw(self):
		for i, rect in enumerate(self.body):
			pygame.draw.rect(cfg.win, self.colors[i], rect)

