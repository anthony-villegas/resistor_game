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

#assigning hex values for colors to use in game
black = pygame.color.Color('#000000')
white = pygame.color.Color('#ffffff')
blue = pygame.color.Color('#0000FF')
red = pygame.color.Color('#FF0000')

#assigning text fonts and sizes for games
font = pygame.font.Font('freesansbold.ttf', 32)

#set caption appearing in window of game
pygame.display.set_caption("Resistor")

#loading assets to be used in game; designed to minimize issues across operating systems
gameFolder = os.path.dirname(__file__)
# joings game folder and images folder
imageFolder = os.path.join(gameFolder, "img")


#initializing clock for game
clock = pygame.time.Clock()

class Component(object):

    def __init__(self, level):
        self.level = level

    #assigns properties of each electric component (resistor and capacitor)
    def resistor(self):
        pass
    
    def capacitor(self):
        pass

    #provides functionality for drawing resistor and capacitor
    def drawComponent(self, win):
        pass

    #will randomly generate player field based on level progression of player
    def generateComponents(self, level):
        pass

class Resistor(object):
    def __init__(self):
        self.image = pygame.Surface((20, 10))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screenWidth - self.rect.width)
        self.rect.y = random.randrange(screenHeight - self.rect.height)
    
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
       



class Player(object):
    def __init__(self, xPos, yPos, vel, points):
        self.image = pygame.image.load(os.path.join(imageFolder, "trump.jpg")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos
        self.vel = vel
        self.velx = 0
        self.vely = self.vel
        self.points = points

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
            

        # if keys[pygame.K_LEFT] and self.rect.left > self.vel:
        #     self.rect.x -= self.vel

        # # in pygame the character position is assigned according to the top left most point. Thus, in order to ensure the character doesn't leave the screen on the right we must restrict the movement to the screenwidth - the character width. We must also account for the velocity because we don't want to be so close so as to have a single input move us past the border
        # if keys[pygame.K_RIGHT] and self.xPos < screenWidth - self.width - self.vel:
        #     self.xPos += self.vel

        # if keys[pygame.K_UP] and self.yPos > self.vel:
        #     self.yPos -= self.vel

        # if keys[pygame.K_DOWN] and self.yPos < screenHeight - self.height - self.vel:
        #     self.yPos += self.vel


def showScore(x, y):
    score = font.render("Score: " + str(man.points), True, red)
    win.blit(score, (x, y))


def redrawGameWindow():
    win.fill(black)
    showScore(screenWidth/2, 2)
    man.draw(win)
    enemy.draw(win)
    pygame.display.update()


def gameLoop():
    # mainloop
    run = True
    while run:
        pygame.time.delay(100)

        #tracks all events/inputs by user that occur
        for event in pygame.event.get():

            #if user presses exit then will stop gameLoop and end game
            if event.type == pygame.QUIT:
                run = False

            #if user presses a key then this key will be sent to Player class to determine movement
            # if event.type == KEYDOWN:
            #     man.move(event.key)

    

        man.move()

        redrawGameWindow()

enemy = Resistor()
man = Player(500, 500, 10, 0)

gameLoop()
pygame.quit()
