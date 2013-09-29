import pygame, sys, random
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 600
WINDOWHEIGHT = 480
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10

BOARDWIDTH = 10
BOARDHEIGHT = 7

#assert for debug , when the bug occurred , the string line will tell where the bug is 
assert (WINDOWWIDTH * WINDOWHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches'

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#Making the source code look pretty

#           R    G    B
GRAY =     (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE =    (255, 255, 255)
RED =      (255, 0, 0)
GREEN =    (0, 255, 0)
BLUE =     (0, 0, 255)
YELLOW =   (255,255,0)
ORANGE =   (255, 188 , 0)
PURPLE =   (255, 0, 255)
CYAN =     (0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHTLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

#the frontpage is not bigger than the background, if not , bug occurred
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT,'BOARD IS TOO BIG FOR THE NUMBER OF THE COLORS AND THE SHAPES'

#the global statement is evil

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    mousex = 0
    mousey = 0
    pygame.display.set_caption('memory_puzzle')
    
    mainboard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)
    
#start the animation
    firstSelection = None
    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainboard)
    
#the game loop

    while True:
        mouseClicked = False
        
        DISPLAYSURF.fill(BGCOLOR)#drawing the window
        drawBoard(mainBoard, revealedBoxes)
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOSUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                
                boxx, boxy = getBoxPixel(mousex, mousey)
                if boxx != None and boxy != None:
                    #the mouse in currently on the box 
                    if not revealedBoxes[boxx][boxy]:
                        drawHighlighBox(boxx, boxy)
                    if not revealedBoxes[boxx][boxy] and mouseClicked:
                        revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                        revealBoxes[boxx][boxy] = True  #set the box as revealed 
                    if firstSelection == None:
                        firstSelection = (boxx, boxy)
                    else:#the mouse was the second box clicked
                        #check if the two boxes are matched 
                        icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0],firstSelection[1])
                        icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
                        
                        if icon1shape != icon2shape or icon1color != icon2color:
                            pygame.time.wait(1000)
                            coverBoxesAnimation(mainBoard,[(firstSelection[0], firstSelection[1]), (boxx,boxy)])
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = Flase
                            revealedBoxes[boxx][boxy] = False
                            
                            #handing if the player is won
                            
                        elif hasWon(revealedBoxes):
                            gameWonAnimation(mainBoard)
                            pygame.time.wait(2000)
                            
                            #reset the board
                            mainBoard = getRandomizedBoard()
                            revealedBoxes = generateRevealedBoxesData(False)
                            
                            #show the fully unrevealed board for a second 
                            drawBoard(mainBoard, revealedBoxes)
                            pygame.display.update()
                            pygame.time.wait(1000)
                            
                            #reply the start game information
                            startGameAnimation(mainBoard)
                        firstSelection = None #reset the firstSelection variable
                        #draw the screen and wait a clock time
                        pygame.display.update()
                        FPSCLOCK.tick(FPS)
                    
#creating the 'revealedboxes 'data structure
                    
def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    #get the list of every possible shapes and colors
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))
    
    random.shuffle(icons) #randomize the order of the icons list
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)#calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2
    random.shuffle(icons)
    
    #placing the icons on the board
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]# remove the icon as we assign them
        board.append(column)
    return board

def splitIntoGroupsOf(groupSize, thelist):
    
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

def leftTopCoordsOfBox(boxx, boxy):
    
    left = boxx * (BOXSIZE * GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE * GAPSIZE) + YMARGIN
    return (left, top)


            
        
                    
                    
                    
            
    