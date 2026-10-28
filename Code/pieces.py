from board import Board
from typing import Literal
class Piece:
    def __init__(self, color: str, startPos: tuple, board: Board):
        self.color = color
        self.position = startPos
        self.board = board
        self.board.board[startPos[0]][startPos[1]] = self
        self.directions = []  # this can be used to mutate the movement capabilities of pieces
        self.sliding = False
    def getColor(self):
        return self.color
    def getPos(self):
        return self.position
    def get_valid_moves(self):
        validMoves = set()
        row, col = self.getPos()
        for dr, dc in self.directions:
            r, c = row + dr, col + dc
            while(0 <= r < self.board.getRow() and 0 <= c < self.board.getCol()):
                piece = self.board.getPiece((r,c))
                if piece is None:
                    validMoves.add((r,c))
                else:
                    if piece.getColor() != self.getColor():
                        validMoves.add((r,c))
                    break
                if not self.sliding:
                    break
                r += dr
                c += dc
        return validMoves
    def move(self, newPos):
        if newPos in self.get_valid_moves():
            self.board.board[self.position[0]][self.position[1]] = None
            self.position = newPos
            self.board.board[newPos[0]][newPos[1]] = self
            return newPos
        return -1
        #return new position
    def get_attack_squares(self):
        attacked = []
        row, col = self.position
        for dr, dc in self.directions:
            r, c = row + dr, col + dc
            while (0 <= r < self.board.getRow() and 0 <= c < self.board.getCol()):
                attacked.append((r, c))
                if self.board.getPiece((r, c)) is not None: #stop at first occupied square regardless of color owner
                    break
                if not self.sliding:
                    break
                r += dr
                c += dc
        return attacked
class Pawn(Piece):
    def __init__(self, color, startPos, board):
        super().__init__(color, startPos, board)
        self.pointVal = 1
        self.passant_able = False
    def get_valid_moves(self):
        pass
        #return list of valid moves
    def move(self, newPos):
        if newPos in self.get_valid_moves():
            self.position = newPos
            self.board.board[newPos[0]][newPos[1]] = self
            return newPos
        return -1
        #return new position

class Bishop(Piece):
    def __init__(self, color, startPos, board):
        super().__init__(color, startPos, board)
        self.pointVal = 3
        self.directions = [
                    (-1, -1), #upleft
                    (-1, 1), #upright
                    (1, -1), #downleft
                    (1, 1) #downright
                    ]
        self.sliding = True



class Knight(Piece):
    def __init__(self, color, startPos, board):
        super().__init__(color, startPos, board)
        self.pointVal = 3
        self.directions = [
                    (-2, -1), (-2, 1), #up 2
                    (-1, -2), (-1, 2), #up 1
                    (1, -2), (1, 2), #down 1
                    (2, -1), (2, 1) #downright
                    ]
        self.sliding = False


class Rook(Piece):
    def __init__(self, color, startPos, board):
        super().__init__(color, startPos, board)
        self.pointVal = 5
        self.hasMoved = False #if rook moves then set to true permanent
        self.directions = [
                    (-1, 0), #up
                    (1, 0), #down
                    (0, -1), #left
                    (0, 1) #right
                    ]
        self.sliding = True
    def move(self, newPos):
        move = super().move(newPos)
        if move != -1:
            self.hasMoved = True
        return move



class Queen(Piece):
    def __init__(self, color, startPos, board):
        super().__init__(color, startPos, board)
        self.pointVal = 9
        self.directions = [
                    (-1, -1), #upleft
                    (-1, 1), #upright
                    (1, -1), #downleft
                    (1, 1), #downright
                    (-1, 0), #up
                    (1, 0), #down
                    (0, -1), #left
                    (0, 1) #right
                    ]
        self.sliding = True

class King(Piece):
    def __init__(self, color, startPos, board):
        super().__init__(color, startPos, board)
        self.pointVal = float("inf")
        self.hasMoved = False #if king moves set to true (permanent), while in check do not allow, and do not allow a castle that would cross a check
        self.directions = [
                    (-1, -1), #upleft
                    (-1, 1), #upright
                    (1, -1), #downleft
                    (1, 1), #downright
                    (-1, 0), #up
                    (1, 0), #down
                    (0, -1), #left
                    (0, 1) #right
                    ]
        self.sliding = False
    def can_castle_with_rook_in_col(self, rookCol, left_right: Literal[-1, 1]):
        row, col = self.getPos()
        if self.hasMoved:
            return False
        rook = self.board.getPiece((row, rookCol))
        if not isinstance(rook, Rook):
            return False
        if (rook.getColor() != self.getColor() or rook.hasMoved):
            return False
        for c in range(col + left_right, rookCol, left_right): #checks squares between king and rook must be empty
            if not self.board.empty((row, c)):
                return False
        all_enemy_attacks = set()
        for r in range(self.board.getRow()):
            for c in range(self.board.getCol()):
                piece = self.board.getPiece((r,c))
                if piece is not None and piece.getColor() != self.getColor():
                    all_enemy_attacks.update(piece.get_attack_squares())
        for c in range(3): #checks that the king does not move through check
            if (row, col+(c*left_right)) in all_enemy_attacks:
                return False
        return True
    def get_valid_moves(self):
        moves = super().get_valid_moves()
        all_enemy_attacks = set()
        for r in range(self.board.getRow()):
            for c in range(self.board.getCol()):
                piece = self.board.getPiece((r,c))
                if piece is not None and piece.getColor() != self.getColor():
                    all_enemy_attacks.update(piece.get_attack_squares())
        for elem in all_enemy_attacks:
            if elem in moves:
                moves.remove(elem)
        if self.can_castle_with_rook_in_col(7, 1):
            moves.add(self.getPos()[0], 6)
        if self.can_castle_with_rook_in_col(0, -1):
            moves.add(self.getPos()[0], 2)
        return moves
        
    def move(self, newPos):
        move = super().move(newPos)
        if move != -1:
            self.hasMoved = True
        return move