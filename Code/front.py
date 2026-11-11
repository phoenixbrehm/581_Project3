import pygame
from pathlib import Path

#Consts
SQUARE = 80
MARGIN = 60
PIECE_SIZE = 60
BOARD_ORGIN = (MARGIN, MARGIN)
SCREEN_SIZE = (SQUARE * 8 + MARGIN * 2, SQUARE * 8 + MARGIN * 2)
FPS = 30
LIGHT = (196, 164, 132)
DARK = (101, 67, 33)



def make_board(board):
    #Makes the chess board
    surf = pygame.Surface((SQUARE * board.getCol(), SQUARE * board.getRow()))
    for row in range(board.getRow()):
        for col in range(board.getCol()):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(surf, color, (col * SQUARE, row * SQUARE, SQUARE, SQUARE))
    return surf.convert()

def load_pieces():
    icon_path = Path(__file__).resolve().parent / "icons"   #where the pictures are located
    pieces = ["pawn_white", "pawn_black", "rook_white", "rook_black", "knight_white", "knight_black", "bishop_white", "bishop_black", "queen_white", "queen_black", "king_white", "king_black"]     #list of all current implemented pieces
    file_type = "png"

    imgs = {}
    for piece in pieces:
        img = pygame.image.load(str(icon_path) + "\\" + piece + "." + file_type).convert_alpha()    #convert image to pygame
        imgs[piece] = pygame.transform.smoothscale(img, (PIECE_SIZE, PIECE_SIZE))   #make it the correct size

    return imgs

def draw_pieces(screen, board, imgs):
    offset = (SQUARE - PIECE_SIZE) // 2
    for row in range(board.getRow()):
        for col in range(board.getCol()):
            piece = board.getPiece((row, col))  #gets piece of board
            if piece is None:
                continue
            key = str(type(piece).__name__.lower()) + str("_") + str(piece.getColor())  #convert piece to key
            x = BOARD_ORGIN[0] + col * SQUARE + offset
            y = BOARD_ORGIN[1] + row * SQUARE + offset
            screen.blit(imgs[key], (x,y))   #put piece on screen

def pos_to_sqr(pos):
    x, y = pos
    return ((y - MARGIN) // SQUARE, (x - MARGIN) // SQUARE)
            

def game(board):
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE) #should make is scaleable in the future
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()

    board_surf = make_board(board)
    imgs = load_pieces()
    

    running = True
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # pygame.QUIT event means the user clicked X to close your window
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #If the mouse is clicked, print the position and the piece. Change to movement
                square = pos_to_sqr(event.pos)
                if board.in_bounds(square):
                    print(square, board.getPiece(square))

        screen.fill("black")
        screen.blit(board_surf, BOARD_ORGIN)
        draw_pieces(screen, board, imgs)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

