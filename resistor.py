import pygame
import time


pygame.init()
screenWidth = 700
screenHeight = 700
win = pygame.display.set_mode((screenWidth, screenHeight))

black = pygame.color.Color('#000000')
white = pygame.color.Color('#ffffff')
blue = pygame.color.Color('#080357')

font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

pygame.display.set_caption("Electrode")
bernieImg = pygame.image.load('trump.jpg')

clock = pygame.time.Clock()


class Player(object):
    def __init__(self, xPos, yPos, width, height, vel, points):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.vel = vel
        self.points = points

    def draw(self, win):
        win.blit(bernieImg, (self.xPos, self.yPos))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.xPos > self.vel:
            self.xPos -= self.vel

        # in pygame the character position is assigned according to the top left most point. Thus, in order to ensure the character doesn't leave the screen on the right we must restrict the movement to the screenwidth - the character width. We must also account for the velocity because we don't want to be so close so as to have a single input move us past the border
        if keys[pygame.K_RIGHT] and self.xPos < screenWidth - self.width - self.vel:
            self.xPos += self.vel

        if keys[pygame.K_UP] and self.yPos > self.vel:
            self.yPos -= self.vel

        if keys[pygame.K_DOWN] and self.yPos < screenHeight - self.height - self.vel:
            self.yPos += self.vel


# # gives funcitonality for displaying text as this isn't available by default in pygame
# def textObjects(text, largeText, color):
#     # .render() built into pygame; render text, set anti aliasing to true and set color of text
#     textSurface = pygame.font.render(text, True, color)
#     # this is used to return rectangle around text to position text
#     return textSurface, textSurface.get_rect()


# def messageDisplay(text, color):
#     # assign font type and size
#     largeText = pygame.font.Font('freesansbold.ttf', 115)
#     # call for text surface and rectangle by providing text and font
#     textSurf, textRect = textObjects(text, largeText, color)
#     # centers text on screen
#     textRect.center = ((screenWidth/2), (screenHeight/2))
#     # queue text in game
#     win.blit(textSurf, textRect)

#     pygame.display.update()
#     gives time for how long text will be on screen in seconds
#     time.sleep(2)
#     restarts game after loss
#     gameLoop()

# def messageDisplay(text):
#     font = pygame.font.Font('freesansbold.ttf', 115)
#     win.blit(font.render(text, True, (0, 0, 0))
#     pygame.display.update()
#     time.sleep(2)
#     gameLoop()

# def messageDisplay():
#     text_surface = font.render(
#         'Hellow World!', antialias=True, color=blue)
#     win.blit(text_surface, (200, 200))
#     pygame.display.update()
#     time.sleep(2)
#     gameLoop()


def showScore(x, y):
    score = font.render("Score: " + str(man.points), True, blue)
    win.blit(score, (x, y))


def redrawGameWindow():
    win.fill(black)
    showScore(screenWidth/2, 2)
    man.draw(win)
    pygame.display.update()


def gameLoop():
    # mainloop
    run = True
    while run:
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        man.move(keys)

        if man.xPos < 40:
            man.points += 1

        redrawGameWindow()


man = Player(500, 500, 50, 33, 10, 0)

gameLoop()
pygame.quit()
