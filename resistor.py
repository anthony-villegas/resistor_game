import pygame
import time
import random
import os

###########################
#DECLARATION OF GLOBAL VARIABLES & INITIALIZING PYGAME
###########################

#intializing pygame
pygame.init()

#assigning values for window height and width and creating a window based on those values
screenWidth = 1000
screenHeight = 1000
display = pygame.display.set_mode((screenWidth, screenHeight))

#assigning number of rows for game and finding integer width of each square within grid
rows = 100
squareWidth = screenWidth // rows

#dictionary stores rects touple as key for all obstacles in game and obstacle type (boundary, component) as value
colliders = {}

# stores resistors, capcitors, etc for blit onto screen
elc_components = []

#FPS declared as global to allow manipulation for electrical component speed effects
fps = 60

#assigning hex values for colors to use in game
black = pygame.color.Color('#000000')
white = pygame.color.Color('#ffffff')
blue = pygame.color.Color('#0000FF')
red = pygame.color.Color('#FF0000')
yellow = pygame.color.Color('#FFFF00')
wireColor = pygame.color.Color('#423629')
playerColor = pygame.color.Color('#F1AB86')
gridColor = pygame.color.Color('#7C7C7C')

#assigning text fonts and sizes for games
font = pygame.font.Font('freesansbold.ttf', 32)

#set caption appearing in window of game
pygame.display.set_caption("Resistor")

#loading assets to be used in game; designed to minimize issues across operating systems
gameFolder = os.path.dirname(__file__)
# joings game folder and images folder
imageFolder = os.path.join(gameFolder, "img")

#variable to turn debug mode during development on or off
debug = True

###########################
###########################


###########################
#ENEMIES / OBSTACLES WITHIN GAME
###########################

class Electric_Component():
    
    def __init__(self, image, pos_x, pos_y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def draw(self, display):
        display.blit(self.image, (self.rect.x*squareWidth, self.rect.y*squareWidth))

class Resistor(Electric_Component):
    
    def __init__(self, image, pos_x, pos_y):
        super().__init__(image, pos_x, pos_y)

        self.cubes_wide = 3
        self.cubes_tall = 3

        colliders[(self.rect.x * squareWidth, self.rect.y * squareWidth, squareWidth * self.cubes_wide, squareWidth * self.cubes_tall)] = 'resistor'

class Capacitor(Electric_Component):

    def __init__(self, image, pos_x, pos_y):
        super().__init__(image, pos_x, pos_y)

        self.cubes_wide = 3
        self.cubes_tall = 3

        colliders[(self.rect.x * squareWidth, self.rect.y * squareWidth, squareWidth * self.cubes_wide, squareWidth * self.cubes_tall)] = 'capacitor'

###########################
###########################


###########################
#PLAYER CLASS & FUNCTIONS
###########################

class Player:
    def __init__(self, row, column, vel, points):
        # self.image = pygame.image.load(os.path.join(imageFolder, "nyancat.jpg")).convert()
        #creating surfaces & rects to be displayed on screeen
        self.image = pygame.Surface((squareWidth,squareWidth))
        self.image.fill(blue)
        self.wire = pygame.Surface((squareWidth, squareWidth))
        self.wire.fill(black)
        self.rect = self.image.get_rect()
        #gives column/row values for player rectangle; same logic as Resistor.draw()
        self.rect.x = row * squareWidth 
        self.rect.y = column * squareWidth 
        #seperate velocities for x and y to force orthogonal movment
        self.vel = vel
        self.velx = 0
        self.vely = 0
        # data storage for scores and collision detection
        self.points = points
        self.wire_cords = [(self.rect.x, self.rect.y)]
        self.collision_number = 0

    def draw(self, display):
   
         # if statement blocks wire_cords array from storing duplicate coordinates due to player character staying at a given coordiante for multiple frames
        if (self.rect.x, self.rect.y) != self.wire_cords[len(self.wire_cords) - 1]:
            self.wire_cords.append((self.rect.x, self.rect.y))
            
            colliders[(self.rect.x, self.rect.y, squareWidth , squareWidth)] = 'wire'
        
        #draws wire / past player positions
        for cord in self.wire_cords:
            display.blit(self.wire, cord)

        
         #draws head of wire / character position
        display.blit(self.image, (self.rect.x, self.rect.y)) 
    
  
    def move(self):
        #go through list of keyboard input
        keys = pygame.key.get_pressed()

        if keys:
            if keys[pygame.K_LEFT]:
                self.velx = self.vel * -1
                self.vely = 0
            elif keys[pygame.K_RIGHT]:
                self.velx = self.vel
                self.vely = 0
            elif keys[pygame.K_UP]:
                self.vely = self.vel * -1
                self.velx = 0
            elif keys[pygame.K_DOWN]:
                self.vely = self.vel
                self.velx = 0

        #change player position based on vel components
        self.rect.x += self.velx
        self.rect.y += self.vely
    
    def checkCollision(self):
        #returns list of colliders{} dict pair that collides with player
        collisions = self.rect.collidedictall(colliders)
        
        if collisions:
            x = collisions[0][1]
            print(x)

            global fps

            #executes effect of collision based on value string in dict
            if x == "wire":
                    self.points -= 20
                    fps = 100
            elif x == "capacitor":
                    self.points += 20
                    fps = 30

            elif x == 'resistor':
                    self.points += 30
                    fps = 60

###########################
###########################

###########################
#GAME / DISPLAY FUNCTIONS
###########################

def load_enemies(display, number):

    for x in range(number):
        image = pygame.Surface((squareWidth*3, squareWidth*3))

        # rand coordinates for electrical component
        x_pos = random.randrange(squareWidth, rows)
        y_pos = random.randrange(squareWidth, rows)
       
       # selction of random electrical component to print
        option = random.randrange(0, 2)

        if option == 0:
            image.fill(blue)
            elc_components.append(Resistor(image, x_pos, y_pos))

        elif option == 1:
            image.fill(yellow)
            elc_components.append(Capacitor(image, x_pos, y_pos))

def showScore(x, y):
    #creates surface on which to place text, places text, then blits surface at position x, y
    score = font.render("Score: " + str(player.points), True, playerColor)
    display.blit(score, (x, y))

def drawGrid():  
    #draws square grid for game number 'rows'; also used for object placement and movement
    
    #variables to track x and y axis for line placement in generating grid
    x = 0
    y = 0
    
    #will generate amount of lines based on value of rows
    for i in range(rows):
        x = x + squareWidth
        y = y + squareWidth

        #draws varying color line on horizontal and vertical axis
        #pygame.draw.line(surface/game window, color, start position of line,end position of line )
        pygame.draw.line(display, gridColor, (x, 0), (x, screenWidth))
        pygame.draw.line(display, gridColor, (0, y), (screenHeight, y))

    #creating boundaries along edge of window to denote kill zones

    #vertical boundary
    boundaryVert = pygame.Surface((squareWidth, screenHeight))
    boundaryVert.fill(red)
    display.blit(boundaryVert, (0, 0))
    display.blit(boundaryVert, (screenWidth - squareWidth, 0))
    #horizontal boundary
    boundaryHor = pygame.Surface((screenWidth, squareWidth))
    boundaryHor.fill(red)
    display.blit(boundaryHor, (0,0))
    display.blit(boundaryHor, (0, screenHeight - squareWidth))

    #adds boundaries to colliders dictionary at first run of loop
    # z = 0
    # if z == 0:
    #     #vert colliders
    #     colliders[(0, 0, squareWidth, screenHeight)] = 'boundary'
    #     colliders[(screenWidth - squareWidth, 0, squareWidth, screenHeight)] ='boundary'
    #     #hor colliders
    #     colliders[(0,0, screenWidth,squareWidth)] = 'boundary'
    #     colliders[(screenHeight - squareWidth, screenWidth, screenHeight)] = 'boundary'
    #     z = z +1
    
def redrawGameWindow():
    display.fill(white)
    drawGrid()
    player.draw(display)
    showScore(screenWidth/2, 2)

    for x in elc_components:
        x.draw(display)

    pygame.display.update()

###########################
###########################

###########################
#MAIN LOOP AND OBJECT INITIALIZATION
###########################

# enemy = ElectricComponent(playerColor)
# enemy2 = ElectricComponent(yellow)

#def __init__(self, row, column, vel, points):
player = Player(21, 21 , 10, 0)

def main():
    #initializing clock for game
    clock = pygame.time.Clock()

    enemy_reset = True

    # gameloop
    run = True
    while run:
        
        pygame.time.delay(fps)

        #tracks all events/inputs by user that occur
        for event in pygame.event.get():

            #if user presses exit then will stop gameLoop and end game
            if event.type == pygame.QUIT:
                run = False

        player.move()

        if enemy_reset == True:

            load_enemies(display, 6)
            enemy_reset = False
            

        player.checkCollision()
       
        # checkCollisions(player.rect, colliders)
        redrawGameWindow()

#quit pygame
main()
pygame.quit()

###########################
###########################
