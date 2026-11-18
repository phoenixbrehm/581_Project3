from board import Board
from pieces import *
from main import setup_normal_board

def TC01():
    board = Board(8, 8)
    for r in range(8):
        for c in range(8):
            if (board.board)[r][c] != None:
                board.printBoard()
                return False

    board.printBoard()
    return True

def TC02():
    board = Board(8, 8)
    setup_normal_board(board)

    p1 = board.removePiece((1, 4))
    board.setPiece((2, 4), p1)
    q1 = board.removePiece((0, 3))
    board.setPiece((4, 7), q1)

    p2 = board.removePiece((6, 5))
    board.setPiece((5, 5), p2)
    p3 = board.removePiece((6, 6))
    board.setPiece((4, 6), p3)

    board.printBoard()
    # this should lead to white king in check 

    if board.is_color_in_check("white"):
        return True
    return False

def TC03():
    board = Board(8, 8)
    setup_normal_board(board)

    p1 = board.removePiece((1,2))
    p2 = board.removePiece((1,3))

    board.setPiece((3,2), p1)
    board.setPiece((2,3), p2)

    Bishop("white", (3, 1), board)

    # this should lead to black king in check 

    if board.is_color_in_check("black"):
        return True
    return False

def TC04():
    board = Board(8, 8)
    setup_normal_board(board)

    # regular boards should NOT have ANY color in check

    if board.is_color_in_check("white"):
        return False
    return True

def TC05():
    board = Board(8, 8)
    setup_normal_board(board)

    # regular boards should NOT have ANY color in check

    if board.is_color_in_check("black"):
        return False
    return True

def TC06():
    board = Board(8, 8)
    setup_normal_board(board) # in the traditional beginning game state of CHess, every player has a legal move
    if board.has_any_legal_move("white"):
        return True
    return False

def TC07():
    board = Board(8, 8)
    setup_normal_board(board) # in the traditional beginning game state of CHess, every player has a legal move
    if board.has_any_legal_move("black"):
        return True
    return False

def TC08():
    board = Board(8, 8) # with an empty board, there should be no legal moves for any player
    if board.has_any_legal_move("white"):
        return False
    return True

def TC09():
    board = Board(8, 8) # with an empty board, there should be no legal moves for any player
    if board.has_any_legal_move("black"):
        return False
    return True

def full_test():
    if TC01():
        print("TC01 PASS")
    else:
        print("TC01 FAIL")

    if TC02():
        print("TC02 PASS")
    else:
        print("TC02 FAIL")

    if TC03():
        print("TC03 PASS")
    else:
        print("TC03 FAIL")

    if TC04():
        print("TC04 PASS")
    else:
        print("TC04 FAIL")

    if TC05():
        print("TC05 PASS")
    else:
        print("TC05 FAIL")

    if TC06():
        print("TC06 PASS")
    else:
        print("TC06 FAIL")

    if TC07():
        print("TC07 PASS")
    else:
        print("TC07 FAIL")

    if TC08():
        print("TC08 PASS")
    else:
        print("TC08 FAIL")

    if TC09():
        print("TC09 PASS")
    else:
        print("TC09 FAIL")


full_test()