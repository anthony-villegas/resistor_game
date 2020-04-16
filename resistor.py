import pygame
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
menu_height = 100

#assigning number of rows for game and finding integer width of each square within grid
rows = 100
squareWidth = screenWidth // rows

#dictionary stores rects touple as key for all obstacles in game and obstacle type (boundary, component) as value
colliders = {}

# stores resistors, capcitors, etc for blit onto screen
elc_components = []

#FPS declared as global to allow manipulation for electrical component speed effects
fps = 60

#initializing clock for game
clock = pygame.time.Clock()

#assigning hex values for colors to use in game
black = pygame.color.Color('#000000')
white = pygame.color.Color('#ffffff')
blue = pygame.color.Color('#0000FF')
red = pygame.color.Color('#FF0000')
yellow = pygame.color.Color('#FFFF00')
wireColor = pygame.color.Color('#423629')
gridColor = pygame.color.Color('#7C7C7C')
menuColor = pygame.color.Color('#BB4D00')
menuColor = red

#set caption appearing in window of game
pygame.display.set_caption("Resistor")

#loading assets to be used in game; designed to minimize issues across operating systems
game_folder = os.path.dirname(__file__)
image_folder = os.path.join(game_folder, "img")


###########################
###########################


###########################
#ENEMIES / OBSTACLES WITHIN GAME
###########################

class Electric_Component():

    def __init__(self, pos_x, pos_y):
        self.image = pygame.Surface((squareWidth*3, squareWidth*3))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def draw(self, display):
        display.blit(self.image, (self.rect.x*squareWidth, self.rect.y*squareWidth))

    def get_position(self):
        return (self.rect.x, self.rect.y)

class Resistor(Electric_Component):

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.image = pygame.image.load(os.path.join(image_folder, "resistor_rectangle.jpg")).convert_alpha()
        self.cubes_wide = 3
        self.cubes_tall = 5

        colliders[(self.rect.x * squareWidth, self.rect.y * squareWidth, squareWidth * self.cubes_wide, squareWidth * self.cubes_tall)] = 'resistor'

class Capacitor(Electric_Component):

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.image = pygame.image.load(os.path.join(image_folder, "capacitor_tall.PNG")).convert_alpha()
        self.cubes_wide = 2
        self.cubes_tall = 5

        colliders[(self.rect.x * squareWidth, self.rect.y * squareWidth, squareWidth * self.cubes_wide, squareWidth * self.cubes_tall)] = 'capacitor'

class Battery(Electric_Component):
    
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.image = pygame.image.load(os.path.join(image_folder, 'battery_resize.PNG')).convert_alpha()
        self.cubes_wide = 5
        self.cubes_tall = 4

        colliders[(self.rect.x * squareWidth, self.rect.y * squareWidth, squareWidth * self.cubes_wide, squareWidth * self.cubes_tall)] = 'battery'

###########################
###########################


###########################
#PLAYER CLASS & FUNCTIONS
###########################

class Player:
    def __init__(self, row, column, vel, points):
        # self.image = pygame.image.load(os.path.join(image_folder, "resistor.PNG")).convert_alpha()
        #creating surfaces & rects to be displayed on screeen
        self.image = pygame.Surface((squareWidth,squareWidth))
        self.image.fill(blue)
        self.wire_width = squareWidth
        self.wire_height = squareWidth
        self.wire = pygame.Surface((self.wire_width, self.wire_height))
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
        self.farads = 0
        self.ohms = 0
        self.lives = 5
        self.level = 1
        self.comps_needed = 1
        self.wire_cords = [(self.rect.x, self.rect.y)]
        

    def draw(self, display):

        #draws wire / past player positions
        for cord in self.wire_cords:
            display.blit(self.wire, cord)


         #draws head of wire / character position
        display.blit(self.image, (self.rect.x, self.rect.y))

    def generate_wire(self):
        
    # if statement blocks wire_cords array from storing duplicate coordinates due to player character staying at a given coordiante for multiple frames

        if (self.rect.x, self.rect.y) != self.wire_cords[len(self.wire_cords) - 1]:
            self.wire_cords.append((self.rect.x, self.rect.y))

            colliders[(self.rect.x, self.rect.y, squareWidth , squareWidth)] = 'wire'

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
        #prevents collision occuring after player is starts, resets, or just collided
        if self.velx + self.vely != 0:

            #returns list of colliders{} dict pair that collides with player
            collisions = self.rect.collidedictall(colliders)

            if collisions:
                x = collisions[0][1]
                global fps
                
                #executes effect of collision based on value string in dict
                if x == "wire":
                    self.lives -= 1
                    self.points -= 20
                    self.collision()

                elif x == "capacitor":
                    #interpret horizontal movement as succesful connection
                    if self.vely == 0:
                        self.farads += 1
                        fps = 30
                        #shift player to other side of capacitor
                        if self.velx > 0:
                            self.rect.x += squareWidth *2
                        else:
                            self.rect.x -= squareWidth *2
                    else:
                        self.lives -= 1
                        self.collision()

                elif x == 'resistor':
                    #interpret vertical movement as succesful connection
                    if self.velx == 0:
                        self.ohms += 1
                        fps = 60
                        #shift to other side of resistor
                        if self.vely > 0:
                            self.rect.y += squareWidth * 5
                        else:
                            self.rect.y -= squareWidth * 5

                    else:
                        self.lives -= 1
                        self.collision()

                elif x == 'boundary':
                    self.lives -= 1
                    self.collision()
                elif x == 'battery':
                    if (self.farads + self.ohms >= self.comps_needed) and self.velx < 0:
                        self.velx, self.vely = 0, 0
                        self.level += 1
                        self.lives += 1
                        reset_game()
                    else:
                        self.collision()

    def collision(self):
        
        #set player stationary to prevent checking for further collisions
        self.velx, self.vely = 0,0
    
        cords = None
        
        if len(self.wire_cords) >2:
            #remove cords and rewind player position
            for x in range(2):
                cords = self.wire_cords.pop()
                del colliders[cords[0], cords[1], squareWidth, squareWidth]

            self.rect.x = cords[0]
            self.rect.y = cords[1]

            #slow player speed after impact
            global fps
            fps = 100

###########################
###########################

###########################
#GAME / DISPLAY FUNCTIONS
###########################

def load_enemies(display, number):
    
    if player.level == 1:
        number = 1

    for x in range(number):
        image = pygame.Surface((squareWidth*5, squareWidth*5))

        position = find_position(image.get_rect())

       # selction of random electrical component to print
        option = random.randrange(0, 2)

        if option == 0:
            elc_components.append(Resistor(position[0], position[1]))

        elif option == 1:
            elc_components.append(Capacitor(position[0], position[1]))

def find_position(rectangle):
    #function prevents overlaps
        collides = True

        x_pos, y_pos = 0,0

        while collides:

            # random row, column for electrical component
            x_pos = random.randrange(1, 97 )
            y_pos = random.randrange(12, 95)

            rectangle.x = x_pos * squareWidth
            rectangle.y = y_pos * squareWidth

            #check for collision with existing component
            collisions = rectangle.collidedictall(colliders)

            if len(collisions) == 0:
               collides = False

        return (x_pos, y_pos)

def render_text(x, y, string, color, size):
    #assigning text fonts and sizes for games
    font = pygame.font.Font('freesansbold.ttf', size)
    #creates surface on which to put text
    text = font.render(string, True, color)
    display.blit(text, (x, y))

def menu():
    # menu
    menu_surface = pygame.Surface((screenWidth, menu_height))
    menu_surface.fill(black)
    display.blit(menu_surface, (0,0))

    render_text(5, 4, f"Level: {player.level}", menuColor, 30)
    render_text(200, 4, f"Lives: {player.lives}", menuColor, 30)
    render_text(400, 4, f"Components Collected: {player.farads + player.ohms}", menuColor, 30)
    render_text(400, 50, f"Components Needed: {player.comps_needed}",menuColor, 30)
    
def drawGrid():
    #draws square grid for game number 'rows'; also used for object placement and movement

    #variables to track x and y axis for line placement in generating grid
    x = 0
    y = menu_height

    #will generate amount of lines based on value of rows
    for i in range(rows):
        x = x + squareWidth
        y = y + squareWidth

        #draws varying color line on horizontal and vertical axis
        #pygame.draw.line(surface/game window, color, start position of line,end position of line )
        # pygame.draw.line(display, gridColor, (x, menu_height), (x, screenWidth))
        # pygame.draw.line(display, gridColor, (0, y), (screenHeight, y))

    #creating boundaries along edge of window to denote kill zones

    #vertical boundary
    boundaryVert = pygame.Surface((squareWidth, screenHeight))
    boundaryVert.fill(red)
    display.blit(boundaryVert, (0, menu_height))
    display.blit(boundaryVert, (screenWidth - squareWidth, menu_height))

    #horizontal boundary
    boundaryHor = pygame.Surface((screenWidth, squareWidth))
    boundaryHor.fill(red)
    display.blit(boundaryHor, (0, menu_height))
    display.blit(boundaryHor, (0, screenHeight - squareWidth))

    #adds boundaries to colliders dictionary at first run of loop
    z = 0
    if z == 0:
         #vert colliders
         colliders[(0, menu_height, squareWidth, screenHeight - menu_height)] = 'boundary'
         colliders[(screenWidth - squareWidth, menu_height, squareWidth, screenHeight - menu_height)] ='boundary'
         #hor colliders
         colliders[(0,menu_height, screenWidth,squareWidth)] = 'boundary'
         colliders[(0, screenHeight - squareWidth , screenWidth, screenHeight)] = 'boundary'
         z = 1

def reset_game():
    #clear board for next lvel
    player.wire_cords.clear()
    elc_components.clear()
    colliders.clear()
    #reset player, battery to standard position + colliders
    player.rect.x = 49 * squareWidth
    player.rect.y = 96 * squareWidth
    player.wire_cords = [(player.rect.x, player.rect.y)]
    colliders[(battery.rect.x * squareWidth, battery.rect.y * squareWidth, squareWidth * battery.cubes_wide, squareWidth * battery.cubes_tall)] = 'battery'
    #reload enemies, update player atributes
    if player.level ==1:

        load_enemies(display, 1)
        player.comps_needed = 1
    
    else:
        load_enemies(display, player.level * 3)
        player.comps_needed = player.level * 2

    player.farads = 0
    player.ohms = 0
    player.velx = 0
    player.vely = 0
    
def update_game():
    #blit everything on screen and check for events
    player.move()
    display.fill(white)
    drawGrid()
    menu()
    player.checkCollision()
    player.generate_wire()
    player.draw(display)
    battery.draw(display)
    for x in elc_components:
        x.draw(display)

    pygame.display.update()

def start_screen(start):
    
    if start == True:
        #screen when starting game
        render_text(400, 500, "resistor", red, 64)
        render_text(400, 650, "use arrows to move", white, 20)
        render_text(400, 700, "press any key to begin", white, 18)
    else:
        #screen upon death
        render_text(400, 500, "resistored", red, 64)
        render_text(400, 600, "press any key to restart", blue, 18)

    pygame.display.flip()
    #waiting for user input to start game
    wait = True
    while wait:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                wait= False

###########################
###########################

###########################
#MAIN LOOP AND OBJECT INITIALIZATION
###########################

#def __init__(self, row, column, vel, points):
player = Player(49, 96 , 10, 0)
battery = Battery(50, 94.9)

reset = True

def main():
    
    start_screen(True)

    global reset

    # gameloop
    run = True
    while run:
        pygame.time.delay(fps)

        #tracks all events/inputs by user that occur
        for event in pygame.event.get():

            #if user presses exit then will stop gameLoop and end game
            if event.type == pygame.QUIT:
                run = False

          #game over screen if player dies
        
        #game over screen if death
        if player.lives == 0:
            start_screen(False)
            
            player.lives = 5
            player.level = 1
            player.comps_needed = .5
            reset_game()
            

        if reset == True:
             load_enemies(display, 1)
             reset = False

        # checkCollisions(player.rect, colliders)
        update_game()


#quit pygame
main()
pygame.quit()

###########################
###########################
