class Board:
    def __init__(self, rows, col):
        self.rows = rows
        self.columns = col
        self.board = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(None)
            self.board.append(row)
    def empty(self, pos):
        if self.board[pos[0]][pos[1]] == None:
            return True
        return False
    def getPiece(self, pos):
        return self.board[pos[0]][pos[1]]
    def getRow(self):
        return self.rows
    def getCol(self):
        return self.columns
    def printBoard(self):
        for i in range(self.getRow()):
            for j in range(self.getCol()):
                print(type(self.board[i][j]), end=" ")
            print("")