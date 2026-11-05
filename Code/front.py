import pygame
from board import Board
from pieces import *


#Consts
SQUARE = 80
MARGIN = 60
BOARD_ORGIN = (MARGIN, MARGIN)
SCREEN_SIZE = (SQUARE * 8 + MARGIN * 2, SQUARE * 8 + MARGIN * 2)
FPS = 30
LIGHT = (196, 164, 132)
DARK = (101, 67, 33)

#Our Board class - just a filler for now maybe
board = Board(8, 8)

def make_board():
    #Makes the chess board
    surf = pygame.Surface((SQUARE * board.getRow(), SQUARE * board.getCol()))
    for row in range(board.getRow()):
        for col in range(board.getCol()):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(surf, color, (col * SQUARE, row * SQUARE, SQUARE, SQUARE))
    return surf.convert()

def make_pieces():
    pass
    #will later get pieces from a file source
            

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED)
    pygame.display.set_caption("Chess")
    clock = pygame.Clock()
    running = True


    #center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2) #idk if I need this might be helpful later

    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # pygame.QUIT event means the user clicked X to close your window
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #If the mouse is clicked
                print(event.pos)

        screen.fill("black") #make a black background
        screen.blit(make_board(), BOARD_ORGIN) #put the board on the screen


        # flip() the display to put your work on screen
        pygame.display.flip()


    pygame.quit()

main()