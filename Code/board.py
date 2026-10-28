class Board:
    def __init__(self, rows: int, col: int):
        self.rows = rows
        self.columns = col
        self.board = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(None)
            self.board.append(row)
    def empty(self, pos: tuple):
        if self.board[pos[0]][pos[1]] == None:
            return True
        return False
    def getPiece(self, pos: tuple):
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
    def is_color_in_check(self, color):
        from pieces import King
        king = None
        for r in range(self.getRow()):
            for c in range(self.getCol()):
                piece = self.getPiece((r, c))
                if(piece is not None and isinstance(piece, King) and piece.getColor() == color):
                    king = piece
                    break
            if king is not None:
                break
        king_pos = king.getPos()
        for r in range(self.getRow()):
            for c in range(self.getCol()):
                piece = self.getPiece((r,c))
                if piece is not None and piece.getColor() != color:
                    if king_pos in piece.get_attack_squares():
                        return True
        return False