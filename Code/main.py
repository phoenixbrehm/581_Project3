from board import Board
from pieces import *

def main():
    board = Board(8, 8)
    Rook("black", (0,0), board)
    board.printBoard()
    print(board.getPiece((0,0)).getColor())
main()