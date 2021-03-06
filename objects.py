import random

import numpy as np
import pygame

import config as cfg


class Box(pygame.Rect):
	'''
	The Box object represents on box on a grid
	'''
	def __init__(self, x, y, w, h, lineWidth, color=cfg.GREEN, borderColor=cfg.DARK_GREEN):
		self.color = color
		self.borderColor = borderColor
		
		self.x = int(x)
		self.y = int(y)
		self.width = w
		self.height = h

		self.lineWidth = int(lineWidth)
		super().__init__(self.x, self.y, self.width, self.height)

	def draw(self, surface: pygame.Surface):
		pygame.draw.rect(surface, self.color, self)							# Draw box
		pygame.draw.rect(surface, self.borderColor, self, self.lineWidth)	# Draw border



class Grid:
	'''
	The Grid object represents a grid full of boxes
	'''
	def __init__(self, x, y, w, h, rows, cols, color=None, boxBorderColor=None):
		self.x = x
		self.y = y

		self.width = int(w)
		self.height = int(h)

		self.rows = int(rows)
		self.columns = int(cols)

		self.color = color
		self.boxBorderColor = boxBorderColor

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
				if self.color and self.boxBorderColor:
					self.boxes[row, column] = Box(
						self.x+self.boxWidth*column,	# x-coordinate
						self.y+self.boxHeight*row,		# y-coordinate
						self.boxWidth,
						self.boxHeight,
						self.width//300,				# lineWidth
						color=self.color,
						borderColor=self.boxBorderColor
					)
				else:
					self.boxes[row, column] = Box(self.x+self.boxWidth*column, self.y+self.boxHeight*row, self.boxWidth, self.boxHeight, self.width//200)

	def draw(self, surface: pygame.Surface):
		'''
		Draws all the boxes in the grid
		
		'''
		self.updateBoxes()
		for row in range(self.rows):
			for column in range(self.columns):
				self.boxes[row, column].draw(surface)



class Snake:
	def __init__(self, shape, facing, grid: Grid, colors, headImage, appleImage, pickupSound, score=0):
		self.grid = grid
		self.shape = np.array(shape)
		self.facing = np.array(facing)
		self.colors = colors
		self.score = score
		self.apple = None
		self.headImage = headImage
		self.appleImage = appleImage
		self.pickupSound = pickupSound

		self.updateBody()
		self.generateApple()

	def updateBody(self):
		# Test if the length of shape, facing and colors are equal
		assert len(self.shape)==len(self.facing)==len(self.colors), f"Snake has a len(self.shape)={len(self.shape)} but len(self.facing)={len(self.facing)} but len(self.colors)={len(self.colors)}"
		
		self.body = np.empty((len(self.shape)), dtype=Box)
		i = 0
		for column, row in self.shape:
			self.body[i] = self.grid[row,column]
			i+=1

	def draw(self, surface):
		self.updateBody()
		for i, rect in enumerate(self.body):
			if self.headImage and i == 0:
				surface.blit(
					pygame.transform.scale(
						pygame.transform.rotate(
							self.headImage,
							np.rad2deg(np.arctan2(*self.facing[0])) # Converts cartesian directions to degrees
						),
						(rect.width, rect.height)
					),
					(rect.x, rect.y)
				)
			else:
				pygame.draw.rect(surface, self.colors[i], rect)
		if self.apple:
			self.apple.draw(surface)

	def tick(self):
		for i in range(len(self.shape)):
			self.shape[i] = np.add(self.shape[i], self.facing[i])

		if any(pos[0] < 0 or pos[0] >= self.grid.columns or pos[1] < 0 or pos[1] >= self.grid.rows for pos in self.shape) or not cfg.unique(self.shape.tolist()):
			return 1

		if self.grid.boxes[self.shape[0][1], self.shape[0][0]] == self.grid.boxes[self.apple.row, self.apple.column]:
			pygame.mixer.Sound.play(self.pickupSound)
			self.score += 1
			self.grow(cfg.mapArrayToRainBow(np.linspace(0, 1, len(self.colors)+1), len(self.shape)))
			self.generateApple()
		self.facing[1:] = self.facing[:-1]

		self.updateBody()

	def generateApple(self, amount=1):
		while True:
			generatedPosition = np.random.randint(0, self.grid.columns), np.random.randint(0, self.grid.rows)
			if any([part == list(generatedPosition) for part in self.shape.tolist()]): # Check if generatedPosition is inside the snake
				continue # Python equivalent of a do while loop
			break
		self.apple = Apple(*generatedPosition, self.grid, self.appleImage)

	def grow(self, newColors, amount=1):
		print(f"[*] growing by {amount}")
		for _ in range(amount):
			self.shape = np.vstack((self.shape, np.add(np.multiply(self.facing[-1], -1), self.shape[-1])))
			self.facing = np.vstack((self.facing, self.facing[-1]))
			self.colors = newColors



class Apple:
	def __init__(self, column, row, grid, img):
		self.column = column
		self.row = row
		self.grid = grid
		self.image = img

	def draw(self, surface):
		img = self.image.resize((int(self.grid.boxWidth), int(self.grid.boxHeight)))
		surface.blit(cfg.PIL_to_surface(img), self.grid[self.row, self.column])



class Button(pygame.sprite.Sprite):
	def __init__(self, rect, img=None, color=cfg.RED):
		self.rect = pygame.Rect(rect)
		self.color = color
		self.image = img
		pygame.sprite.Sprite.__init__(self)

	def hover(self, point):
		mouseX, mouseY = point
		if self.rect.x < mouseX < self.rect.right and self.rect.y < mouseY < self.rect.bottom:
			return True
		return False

	def draw(self, win):
		pygame.draw.rect(win, self.color, self.rect)
		if self.image:
			win.blit(self.image, np.array(self.rect.center) - np.array(self.image.get_size())/2)
