import pygame
from pathlib import Path
from pieces import Pawn, Checkers

#Consts
SQUARE = 80
MARGIN = 60
PIECE_SIZE = 60
BOARD_ORGIN = (MARGIN, MARGIN)
SCREEN_SIZE = (SQUARE * 8 + MARGIN * 2, SQUARE * 8 + MARGIN * 2)
FPS = 30
LIGHT = (196, 164, 132)
DARK = (101, 67, 33)
SELECT_COLOR = (246, 246, 105, 140)  #translucent yellow on the selected piece's square
MOVE_COLOR = (40, 40, 40, 110)       #translucent dots/rings for available moves
CHECK_COLOR = (220, 40, 40, 150)     #translucent red on a king that is in check
TEXT_COLOR = (230, 230, 230)
PROMOTION_KEYS = {
    pygame.K_q: "queen",
    pygame.K_r: "rook",
    pygame.K_b: "bishop",
    pygame.K_n: "knight",
}



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
    pieces = ["pawn_white", "pawn_black", "rook_white", "rook_black", "knight_white", "knight_black", "bishop_white", "bishop_black", "queen_white", "queen_black", "king_white", "king_black", "checkers_white", "checkers_black", "kingchecker_white", "kingchecker_black", "wall_white", "wall_black"]     #list of all current implemented pieces
    file_type = "png"

    imgs = {}
    for piece in pieces:
        img = pygame.image.load(str(icon_path) + "\\" + piece + "." + file_type).convert_alpha()    #convert image to pygame
        imgs[piece] = pygame.transform.scale(img, (PIECE_SIZE, PIECE_SIZE))   #make it the correct size

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

def sqr_to_pos(square):
    #top left pixel of a board square
    row, col = square
    return (BOARD_ORGIN[0] + col * SQUARE, BOARD_ORGIN[1] + row * SQUARE)

def find_king(board, color):
    from pieces import King
    for row in range(board.getRow()):
        for col in range(board.getCol()):
            piece = board.getPiece((row, col))
            if isinstance(piece, King) and piece.getColor() == color:
                return (row, col)
    return None

def draw_highlights(screen, board, selected, moves, state):
    #Draws check highlight, the selected square, and the available moves
    overlay = pygame.Surface((SQUARE, SQUARE), pygame.SRCALPHA)

    if state in ("check", "checkmate"):
        king_sqr = find_king(board, board.get_turn())
        if king_sqr is not None:
            overlay.fill(CHECK_COLOR)
            screen.blit(overlay, sqr_to_pos(king_sqr))

    if selected is not None:
        overlay.fill(SELECT_COLOR)
        screen.blit(overlay, sqr_to_pos(selected))

    for move in moves:
        overlay.fill((0, 0, 0, 0))
        center = (SQUARE // 2, SQUARE // 2)
        if board.getPiece(move) is not None:
            pygame.draw.circle(overlay, MOVE_COLOR, center, SQUARE // 2 - 2, 6)  #ring for a capture
        else:
            pygame.draw.circle(overlay, MOVE_COLOR, center, SQUARE // 7)          #dot for an empty square
        screen.blit(overlay, sqr_to_pos(move))

def status_text(board, state, promoting=None, jumping=None):
    turn = board.get_turn().capitalize()
    if promoting is not None:
        return f"{turn}: promote with Q, R, B or N"
    if jumping is not None:
        return f"{turn}: keep jumping, or right-click to stop"
    if state == "checkmate":
        winner = "Black" if board.get_turn() == "white" else "White"
        return f"Checkmate! {winner} wins."
    if state == "stalemate":
        return "Stalemate! It's a draw."
    if state == "check":
        return f"{turn} to move - Check!"
    return f"{turn} to move (Turn {board.get_turn_count()})"

def draw_status(screen, font, board, state, promoting=None, jumping=None):
    text = font.render(status_text(board, state, promoting, jumping), True, TEXT_COLOR)
    rect = text.get_rect(center=(SCREEN_SIZE[0] // 2, MARGIN // 2))
    screen.blit(text, rect)

def game(board):
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE) #should make is scaleable in the future
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    board_surf = make_board(board)
    imgs = load_pieces()

    selected = None     #square of the currently selected piece
    moves = set()       #valid moves of the selected piece
    promoting = None    #pawn waiting for the player to pick what it promotes to
    jumping = None      #checker in the middle of a multijump
    state = board.get_board_state(board.get_turn())
    game_over = False

    def end_turn():
        #swap turns and check the state for the next player
        nonlocal selected, moves, promoting, jumping, state, game_over
        selected, moves, promoting, jumping = None, set(), None, None
        board.switch_turns()
        state = board.get_board_state(board.get_turn())
        if state in ("checkmate", "stalemate"):
            game_over = True

    def after_move(piece):
        #decide whether the turn is over, or the player still has to promote / can keep jumping
        nonlocal selected, moves, promoting, jumping
        if isinstance(piece, Pawn) and piece.can_promote():
            promoting = piece
            selected, moves = piece.getPos(), set()
        elif isinstance(piece, Checkers):
            more_jumps = piece.get_followup_jumps()
            if more_jumps:
                jumping = piece
                selected, moves = piece.getPos(), more_jumps
            else:
                piece.finish_turn()
                end_turn()
        else:
            end_turn()

    running = True
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # pygame.QUIT event means the user clicked X to close your window
                running = False

            elif event.type == pygame.KEYDOWN and promoting is not None and event.key in PROMOTION_KEYS:
                #Pawn promotion: Q, R, B or N
                promoting.promotion(PROMOTION_KEYS[event.key])
                end_turn()

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and promoting is None and jumping is not None:
                #Multijump: click a highlighted square to keep jumping, right-click or click the checker to stop
                square = pos_to_sqr(event.pos)
                if event.button == 3 or (event.button == 1 and square == jumping.getPos()):
                    jumping.finish_turn()
                    end_turn()
                elif event.button == 1 and square in moves:
                    jumping.move(square)
                    piece, jumping = jumping, None
                    after_move(piece)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over and promoting is None:
                square = pos_to_sqr(event.pos)
                if not board.in_bounds(square):
                    selected, moves = None, set()
                    continue

                clicked = board.getPiece(square)

                if selected is not None and square in moves:
                    #Move the selected piece
                    piece = board.getPiece(selected)
                    new_pos, taken = piece.move(square)
                    selected, moves = None, set()
                    if new_pos == -1:
                        continue
                    after_move(piece)

                elif clicked is not None and clicked.getColor() == board.get_turn():
                    #Select (or switch to) one of the current player's pieces
                    if selected == square:
                        selected, moves = None, set()
                    else:
                        selected = square
                        moves = clicked.get_valid_moves()

                else:
                    #Clicked an empty square / enemy piece that isn't a valid move
                    selected, moves = None, set()

        screen.fill("black")
        screen.blit(board_surf, BOARD_ORGIN)
        draw_highlights(screen, board, selected, moves, state)
        draw_pieces(screen, board, imgs)
        draw_status(screen, font, board, state, promoting, jumping)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
