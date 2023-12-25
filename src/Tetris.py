import random
import pygame
from src.Block import Block

class Tetris:
    level = 1
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    zoom = 20
    x = 100
    y = 60
    block = None
    nextBlock=None
    
    #Sets the properties of the board
    def __init__(self, height, width, shapes, shapeColors, gameDimensions, topLeft):
        self.height = height
        self.width = width
        self.shapes = shapes
        self.shapeColors = shapeColors
        self.gameDimensions = gameDimensions
        self.topLeft = topLeft


        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    #Creates a new block
    def new_block(self):
        self.block = Block(3, 0,random.randint(0, len(self.shapes) - 1), self.shapes)
                           
    def next_block(self):
        self.nextBlock=Block(3,0,random.randint(0, len(self.shapes) - 1), self.shapes)
    #Checks if the blocks touch the top of the board
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    if i + self.block.y > self.height - 1 or \
                            j + self.block.x > self.width - 1 or \
                            j + self.block.x < 0 or \
                            self.field[i + self.block.y][j + self.block.x] > 0:
                        intersection = True
                        
        return intersection

    #Checks if a row is formed and destroys that line
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def draw_next_block(self,screen):
    
        font = pygame.font.SysFont("Calibri", 30)
        label = font.render("Next Shape", 1, (128,128,128))

        sx = self.topLeft['x'] + self.gameDimensions['width'] + 200
        sy = self.topLeft['y'] + self.gameDimensions['height']/2 - 100
        format = self.nextBlock.image()
        for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.nextBlock.image():
                        pygame.draw.rect(screen, self.shapeColors[self.nextBlock.color],(sx + j*30, sy + i*30, 30, 30), 0)
    
    #Moves the block to the bottom
    def moveBottom(self):
        while not self.intersects():
            self.block.y += 1
        self.block.y -= 1
        self.freeze()

    #Moves the block down by a unit
    def moveDown(self):
        self.block.y += 1
        if self.intersects():
            self.block.y -= 1
            self.freeze()

    # This function runs once the block reaches the bottom. 
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    self.field[i + self.block.y][j + self.block.x] = self.block.color
        self.break_lines() #Checking if any row is formed
        self.block=self.nextBlock
        self.next_block() #Creating a new block
        if self.intersects(): #If blocks touch the top of the board, then ending the game by setting status as gameover
            self.state = "gameover"
    #This function moves the block horizontally
    def moveHoriz(self, dx):
        old_x = self.block.x
        self.block.x += dx
        if self.intersects():
            self.block.x = old_x

    #This function rotates the block 
    def rotate(self):
        old_rotation = self.block.rotation
        self.block.rotate()
        if self.intersects():
            self.block.rotation = old_rotation