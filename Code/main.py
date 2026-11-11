from board import Board
from pieces import *
from front import game

def setup_normal_board(board):
    back_row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    for col, piece_class in enumerate(back_row):
        piece_class("black", (0, col), board)
        piece_class("white", (7, col), board)
    for col in range(8):
        Pawn("black", (1, col), board)
        Pawn("white", (6, col), board)

def main():
    board = Board(8, 8)
    setup_normal_board(board)
    game(board)
main()