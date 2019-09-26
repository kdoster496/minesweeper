import random, pygame, sys
from square import Square
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
BOXSIZE = 30
XMARGIN = BOXSIZE
YMARGIN = BOXSIZE * 2
BOARDWIDTH = int(WINDOWWIDTH / BOXSIZE) - 2
BOARDHEIGHT = int(WINDOWHEIGHT / BOXSIZE) - 3
NUMSPACES = (BOARDHEIGHT * BOARDWIDTH)
NUMMINES = int(NUMSPACES / 4)
MINESFLAGGED = 0
COVEREDSPACES = NUMSPACES

DARKGRAY = (100, 100, 100)
MIDGRAY = (150, 150, 150)
LIGHTGRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

BGCOLOR = DARKGRAY
BOXCOLOR = LIGHTGRAY


def main():
    global DISPLAYSURF
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0
    mousey = 0
    pygame.display.set_caption('Sweepminer')

    mainBoard = makeBoard()
    clickedBoxes = generateClickedBoxesData(False)

    DISPLAYSURF.fill(BGCOLOR)
    drawBoard(mainBoard, clickedBoxes)

    while True:
        mousex, mousey = -1, -1
        mouseClicked = False

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                if event.button == BUTTON_LEFT:
                    mousex, mousey = event.pos
                    mouseClicked = True
                elif event.button == BUTTON_RIGHT:
                    mousex, mousey = event.pos
                    boxx, boxy = getBoxAtPixel(mousex, mousey)
                    left, top = leftTopCoordsOfBox(boxx, boxy)
                    if not clickedBoxes[boxx][boxy]:
                        clickedBoxes[boxx][boxy] = True
                        flagMine(mainBoard, boxx, boxy)
                    else:
                        clickedBoxes[boxx][boxy] = False
                        pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left + 1, top + 1, BOXSIZE - 2, BOXSIZE - 2))
                #elif event.button == BUTTON_MIDDLE:
                    #mousex, mousey = event.pos
                    #boxx, boxy = getBoxAtPixel(mousex, mousey)
                    #if mainBoard[boxx][boxy].numAround == 0:
                        #for x in range(boxx - 1, boxx + 2):
                            #for y in range(boxy - 1, boxy + 2):
                                #if 0 <= x < BOARDWIDTH and 0 <= y < BOARDHEIGHT and not clickedBoxes[x][y]:
                                    #clickSpace(mainBoard, x, y)

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            if not clickedBoxes[boxx][boxy] and mouseClicked:
                clickedBoxes[boxx][boxy] = True
                clickSpace(mainBoard, boxx, boxy)
        if COVEREDSPACES == 0:
            wonGame()
        #print(str(COVEREDSPACES))

        pygame.display.update()


def makeBoard():
    mineSpot = []
    i = 0
    while i < NUMMINES:
        mineSpot.append(True)
        i += 1
    while i < NUMSPACES:
        mineSpot.append(False)
        i += 1
    random.shuffle(mineSpot)
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(Square(mineSpot[0]))
            del mineSpot[0]
        board.append(column)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            around(board, x, y)
    return board

def around(board, boxx, boxy):
    mineCount = 0
    for x in range(boxx - 1, boxx + 2):
        for y in range(boxy - 1, boxy + 2):
            if 0 <= x < BOARDWIDTH and 0 <= y < BOARDHEIGHT:
                if board[x][y].isMine:
                    mineCount += 1
    board[boxx][boxy].setNumber(mineCount)

def clickSpace(board, boxx, boxy):
    if board[boxx][boxy].isMine:
        if not board[boxx][boxy].flagged:
            for x in range(BOARDWIDTH):
                for y in range(BOARDHEIGHT):
                    if board[x][y].isMine:
                        if not board[x][y].flagged:
                            left, top = leftTopCoordsOfBox(x, y)
                            pygame.draw.rect(DISPLAYSURF, RED, (left + 1, top + 1, BOXSIZE - 2, BOXSIZE - 2))

    else:
        font = getScaledFont(BOXSIZE, BOXSIZE, str(board[boxx][boxy].numDisplay), 'Comic Sans')
        tl = leftTopCoordsOfBox(boxx, boxy)
        pygame.draw.rect(DISPLAYSURF, MIDGRAY, (tl[0] + 1, tl[1] + 1, BOXSIZE - 2, BOXSIZE - 2))
        center = tl + (BOXSIZE / 2, BOXSIZE / 2)
        text = font.render(str(board[boxx][boxy].numDisplay), 1, BLACK)
        text_rect = text.get_rect(center=(tl[0] + (BOXSIZE / 2), tl[1] + (BOXSIZE / 2)))
        DISPLAYSURF.blit(text, text_rect)
        global COVEREDSPACES
        COVEREDSPACES -= 1
        #if board[boxx][boxy].numDisplay == 0:
            #for x in range(boxx - 1, boxx + 2):
                #for y in range(boxy - 1, boxy + 2):
                    #if 0 <= x < BOARDWIDTH and 0<= y < BOARDHEIGHT and not clickedBoxes[x][y]:
                        ##clickSpace(board, x, y)
                        #font = getScaledFont(BOXSIZE, BOXSIZE, str(board[x][y].numDisplay), 'Comic Sans')
                        #tl = leftTopCoordsOfBox(x, y)
                        #pygame.draw.rect(DISPLAYSURF, MIDGRAY, (tl[0] + 1, tl[1] + 1, BOXSIZE - 2, BOXSIZE - 2))
                        #center = tl + (BOXSIZE / 2, BOXSIZE / 2)
                        #text = font.render(str(board[x][y].numDisplay), 1, BLACK)
                        #text_rect = text.get_rect(center=(tl[0] + (BOXSIZE / 2), tl[1] + (BOXSIZE / 2)))
                        #DISPLAYSURF.blit(text, text_rect)
                        #COVEREDSPACES -= 1
                        ##if board[x][y].numDisplay == 0:


def flagMine(board, boxx, boxy):
    global MINESFLAGGED
    MINESFLAGGED += 1
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, BLUE, (left + 1, top + 1, BOXSIZE - 2, BOXSIZE - 2))
    global COVEREDSPACES
    COVEREDSPACES -= 1
    board[boxx][boxy].flagMine()
    for x in range(boxx - 1, boxx + 2):
        for y in range(boxy - 1, boxy + 2):
            if 0 <= x < BOARDWIDTH and 0<= y < BOARDHEIGHT:
                board[x][y].numAround -= 1

def wonGame():
    font = getScaledFont(WINDOWWIDTH, WINDOWHEIGHT, 'You win', 'Comic Sans')
    tl = WINDOWWIDTH / 2, WINDOWHEIGHT / 2
    text = font.render('You win', 1, BLACK)
    text_rect = text.get_rect(center= (tl[0], tl[1]))
    DISPLAYSURF.blit(text, text_rect)

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * BOXSIZE + XMARGIN
    top = boxy * BOXSIZE + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawBoard(board, revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left + 1, top + 1, BOXSIZE - 2, BOXSIZE - 2))
            if revealed[boxx][boxy]:
                clickSpace(board, boxx, boxy)


def generateClickedBoxesData(val):
    clickedBoxes = []
    for i in range(BOARDWIDTH):
        row = []
        for j in range(BOARDHEIGHT):
            row.append(val)
        clickedBoxes.append(row)
    return clickedBoxes


def getScaledFont(max_w, max_h, text, font_name):
    font_size = 0
    font = pygame.font.SysFont(font_name, font_size)
    w, h = font.size(text)
    while w < max_w and h < max_h:
        font_size += 1
        font = pygame.font.SysFont(font_name, font_size)
        w, h = font.size(text)
    return pygame.font.SysFont(font_name, font_size - 1)


if __name__ == '__main__':
    main()
