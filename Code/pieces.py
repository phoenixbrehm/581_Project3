class Piece:
    def __init__(self, color: str, startPos: tuple, board: board):
        self.color = color
        self.position = startPos
        self.board = board


class Pawn(Piece):
    def __init__(self, color, startPos):
        super().__init__(color, startPos)
        self.pointVal = 1
        self.passant_able = False
    def get_valid_moves(self):
        pass
        #return list of valid moves
    def move(self, newPos):
        if newPos in self.get_valid_moves():
            self.position = newPos
            return newPos
        return -1
        #return new position

class Bishop(Piece):
    def __init__(self, color, startPos):
        super().__init__(color, startPos)
        self.pointVal = 3
    def get_valid_moves(self):
        #left diag
        #iterate (-1, +1), stop when wall or another piece
        pass
    def move(self, newPos):
        if newPos in self.get_valid_moves():
            self.position = newPos
            return newPos
        return -1
        #return new position

class Knight(Piece):
    def __init__(self, color, startPos):
        super().__init__(color, startPos)
        self.pointVal = 3
    def get_valid_moves(self):
        pass
        #return list of valid moves
    def move(self, newPos):
        if newPos in self.get_valid_moves():
            self.position = newPos
            return newPos
        return -1
        #return new position

class Rook(Piece):
    def __init__(self, color, startPos):
        super().__init__(color, startPos)
        self.pointVal = 5
        self.canCastle = True #if rook moves then set to false
    def get_valid_moves(self):
        pass
        #return list of valid moves
    def move(self, newPos):
        if newPos in self.get_valid_moves():
            self.position = newPos
            return newPos
        return -1
        #return new position

class Queen(Piece):
    def __init__(self, color, startPos):
        super().__init__(color, startPos)
        self.pointVal = 9
    def get_valid_moves(self):
        pass
        #return list of valid moves
    def move(self, newPos):
        if newPos in self.get_valid_moves():
            self.position = newPos
            return newPos
        return -1
        #return new position

class King(Piece):
    def __init__(self, color, startPos):
        super().__init__(color, startPos)
        self.pointVal = float("inf")
        self.canCastle = True #if king moves set to false (permanent), while in check set to false, and do not allow a castle that would cross a check
    def get_valid_moves(self):
        pass
        #return list of valid moves
    def move(self, newPos):
        if newPos in self.get_valid_moves():
            self.position = newPos
            return newPos
        return -1
        #return new position