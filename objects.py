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
		self.colors = colors

		self.updateBody()


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

	def tick(self):
		for i in range(len(self.shape)):
			self.shape[i] = np.add(self.shape[i], self.facing[i])
		self.facing[1:] = self.facing[:-1]

		if any(shape[0] < 0 or shape[0] >= self.grid.rows or shape[1] < 0 or shape[1] >= self.grid.columns for shape in self.shape) or not cfg.unique(self.shape.tolist()):
			return 1
		self.updateBody()
	
	def eat(self, newColor, amount=1):
		print(f"[*] growing by {amount}")
		for _ in range(amount):
			# self.shape = self.shape, self.facing[-1]))
			self.shape = np.vstack((self.shape, np.add(np.multiply(self.facing[-1], -1), self.shape[-1])))
			self.facing = np.vstack((self.facing, self.facing[-1]))
			self.colors = np.vstack((self.colors, newColor))

		self.updateBody()


class Apple(pygame.Rect):
	def __init__(self, x, y, w, h, img):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		
		self.image = img
		super().__init__(self.x, self.y, self.width, self.height)

	def draw(self):
		img = self.image.resize((self.width, self.height))
		cfg.win.blit(cfg.PIL_to_surface(img), (self.x, self.y))

