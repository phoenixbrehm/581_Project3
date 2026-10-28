from board import Board
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
        validMoves = []
        row, col = self.getPos()
        for dr, dc in self.directions:
            r, c = row + dr, col + dc
            while(0 <= r < self.board.getRow() and 0 <= c < self.board.getCol()):
                piece = self.board.getPiece((r,c))
                if piece is None:
                    validMoves.append((r,c))
                else:
                    if piece.getColor() != self.getColor():
                        validMoves.append((r,c))
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
        self.hasMoved = True
        return super().move(newPos)


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
    def can_castle_with_rook_in_col(self, rookCol):
        row, col = self.getPos()
        if self.hasMoved:
            return False
        rook = self.board.getPiece((row, rookCol))
        if not isinstance(rook, Rook) and (rook.getColor() != self.getColor() or rook.hasMoved):
            return False
    def move(self, newPos):
        self.hasMoved = True
        return super().move(newPos)