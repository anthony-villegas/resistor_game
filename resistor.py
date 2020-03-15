import pygame
import time
import random
import os

#intializing pygame
pygame.init()

#assigning values for window height and width and creating a window based on those values
screenWidth = 800
screenHeight = 800
win = pygame.display.set_mode((screenWidth, screenHeight))

#assigning number of rows for game and finding integer width of each square within grid
rows = 80
squareWidth = screenWidth // rows

#assigning hex values for colors to use in game
black = pygame.color.Color('#000000')
white = pygame.color.Color('#ffffff')
blue = pygame.color.Color('#0000FF')
red = pygame.color.Color('#FF0000')
yellow = pygame.color.Color('#FFFF00')

#assigning text fonts and sizes for games
font = pygame.font.Font('freesansbold.ttf', 32)

#set caption appearing in window of game
pygame.display.set_caption("Resistor")

#loading assets to be used in game; designed to minimize issues across operating systems
gameFolder = os.path.dirname(__file__)
# joings game folder and images folder
imageFolder = os.path.join(gameFolder, "img")


class Resistor(object):
    def __init__(self):
        self.image = pygame.Surface((squareWidth, squareWidth))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(rows)
        self.rect.y = random.randrange(rows)       

    def draw(self):
        #self.rect.y/x contains an integer value for row. Multiplying this value by squareWidth serves to ensure resistor is placed in an integer value row or column on a normally pixel valued screen
        win.blit(self.image, (self.rect.x*squareWidth+1, self.rect.y*squareWidth+1))

class Player(object):
    def __init__(self, row, column, vel, points):
        # self.image = pygame.image.load(os.path.join(imageFolder, "trump.jpg")).convert()
        self.image = pygame.Surface((squareWidth,squareWidth))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        #gives column/row values for player rectangle; same logic as Resistor.draw()
        self.rect.x = row * squareWidth 
        self.rect.y = column * squareWidth 
        #seperate velocities for x and y to force orthogonal movment
        self.vel = vel
        self.velx = 0
        self.vely = 0
        self.points = points

    #draws player at given row 
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
   
    def move(self):
        keys = pygame.key.get_pressed()

        if keys:
            if keys[pygame.K_LEFT]:
                self.velx = self.vel * -1
                self.vely = 0
            if keys[pygame.K_RIGHT]:
                self.velx = self.vel
                self.vely = 0
            if keys[pygame.K_UP]:
                self.vely = self.vel * -1
                self.velx = 0
            if keys[pygame.K_DOWN]:
                self.vely = self.vel
                self.velx = 0

        self.rect.x += self.velx
        self.rect.y += self.vely
                
#creates surface on which to place text, places text, then blits surface at position x, y
def showScore(x, y):
    score = font.render("Score: " + str(man.points), True, yellow)
    win.blit(score, (x, y))

#draws square grid for game number 'rows'; invisible in actual game but used for object placement and movement
def drawGrid():  
    #variables to track x and y axis for line placement in generating grid
    x = 0
    y = 0

    #will generate amount of lines based on value of rows
    for i in range(rows):
        x = x + squareWidth
        y = y + squareWidth

        #draws varying color line on horizontal and vertical axis
        #pygame.draw.line(surface/game window, color, start position of line,end position of line )
        pygame.draw.line(win, black, (x, 0), (x, screenWidth))
        pygame.draw.line(win, black, (0, y), (screenHeight, y))


def redrawGameWindow():
    win.fill(black)
    drawGrid()
    showScore(screenWidth/2, 2)
    man.draw(win)
    enemy.draw()
    pygame.display.update()


def main():
    #initializing clock for game
    clock = pygame.time.Clock()

    # gameloop
    run = True
    while run:
        pygame.time.delay(60)

        #tracks all events/inputs by user that occur
        for event in pygame.event.get():

            #if user presses exit then will stop gameLoop and end game
            if event.type == pygame.QUIT:
                run = False

        man.move()

        redrawGameWindow()


enemy = Resistor()
#def __init__(self, row, column, vel, points):
man = Player(21, 21 , 40, 0)

main()
pygame.quit()
