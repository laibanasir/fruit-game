import pygame, random, sys, os, time
from pygame.locals import *

windowWidth = 800
windowHeight = 600
size = (800, 600)
textColor = (255, 255, 255)

backgroundColor = (173, 219, 217)
FPS = 40
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 6
count = 3
topScore=0
def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # escape quits
                    terminate()
                return
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, textColor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
background = pygame.image.load("background.jpg")
windowSurface.blit(background, [0,0])
pygame.display.set_caption('Save the orange game')
pygame.mouse.set_visible(False)

playerImage = pygame.image.load('fr1.png')
knife3 = pygame.image.load('k3.png')
knife4 = pygame.image.load('k4.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('k2.png')
sample = [knife3, knife4, baddieImage]
wallLeft = pygame.image.load('fridgeleft.png')
wallRight = pygame.image.load('fridgeright.png')

font = pygame.font.SysFont(None, 42)
drawText('PRESS ANY KEY TO START THE GAME!', font, windowSurface, (windowWidth / 3) - 137, (windowHeight / 3)+80)
pygame.display.update()
waitForPlayerToPressKey()
zero = 0

while (count > 0):
    baddies = []
    score = 0
    playerRect.topleft = (windowWidth / 2, windowHeight - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0

    while True:
        score += 1

        for event in pygame.event.get():

            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = 30
            newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 23, 47),
                         'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                         'surface': pygame.transform.scale(random.choice(sample), (23, 47)),
                         }
            baddies.append(newBaddie)
            sideLeft = {'rect': pygame.Rect(0, 0, 126, 600),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface': pygame.transform.scale(wallLeft, (126, 599)),
                        }
            baddies.append(sideLeft)
            sideRight = {'rect': pygame.Rect(497, 0, 303, 600),
                         'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                         'surface': pygame.transform.scale(wallRight, (303, 599)),
                         }
            baddies.append(sideRight)

        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < windowWidth:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < windowHeight:
            playerRect.move_ip(0, PLAYERMOVERATE)

        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        for b in baddies[:]:
            if b['rect'].top > windowHeight:
                baddies.remove(b)

        font = pygame.font.SysFont(None, 38)
        windowSurface.fill(backgroundColor)
        drawText('Score: %s' % (score), font, windowSurface, 128, 0)
        drawText('Highscore: %s' % (topScore), font, windowSurface, 128, 21)
        drawText('Lifes left: %s' % (count), font, windowSurface, 128, 41)

        windowSurface.blit(playerImage, playerRect)

        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score
            break

        mainClock.tick(FPS)

    count = count - 1
    time.sleep(1)
    font = pygame.font.SysFont(None, 52)
    if (count == 0):

        drawText('Oh no, you lost!', font, windowSurface, (windowWidth / 3)+40, (windowHeight / 3)+70)
        drawText('Press any key to start again. ', font, windowSurface, (windowWidth /3) - 110, (windowHeight / 3) + 95)
        drawText('Press Escape to exit. ', font, windowSurface, (windowWidth / 3) - 110, (windowHeight / 3) + 120)
        pygame.display.update()
        time.sleep(2)
        waitForPlayerToPressKey()
        count = 3