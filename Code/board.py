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
    def in_bounds(self, pos: tuple):
            val, num = pos
            return 0 <= val < self.rows and 0 <= num < self.columns
    def empty(self, pos: tuple):
        if not self.in_bounds(pos):
            return False
        return self.board[pos[0]] [pos[1]] is None
    def getPiece(self, pos: tuple):
        if not self.in_bounds(pos): 
            return None
        return self.board[pos[0]][pos[1]]
    def setPiece(self, pos: tuple, piece):
        if not self.in_bounds(pos):
            raise ValueError(f"{pos} off the board")
        self.board[pos[0]][pos[1]] = piece
    def removePiece(self, pos: tuple):
        piece = self.getPiece(pos)
        self.setPiece(pos, None)
        return piece
    """def movePiece(self, start: tuple, end: tuple):
        piece = self.getPiece(start)
        if piece is None:
            raise ValueError(f"No piece at {start}")
        caught = self.getPiece(end)
        self.setPiece(end, piece)
        self.setPiece(start, None)
        piece.setPos(end)
        return caught"""
    def getRow(self):
        return self.rows
    def getCol(self):
        return self.columns
    def printBoard(self):
        for i in range(self.getRow()):
            for j in range(self.getCol()):
                piece = self.board[i][j]
                if piece is None:
                    print(" .", end=" ")
                else: 
                    print(type(piece).__name__[:2], end=" ")
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
            if king is None:
                return False
            king_pos = king.getPos()
        king_pos = king.getPos()
        for r in range(self.getRow()):
            for c in range(self.getCol()):
                piece = self.getPiece((r,c))
                if piece is not None and piece.getColor() != color:
                    if king_pos in piece.get_attack_squares():
                        return True
        return False
    def has_any_legal_move(self, color):
        for r in range(self.getRow()):
            for c in range(self.getCol()):
                piece = self.getPiece((r,c))
                if piece is not None and piece.getColor() == color:
                    if len(piece.get_valid_moves()) > 0:
                        return True
        return False
    def is_checkmate(self, color):
        return self.is_color_in_check(color) and not self.has_any_legal_move(color)
    def is_stalemate(self, color):
        return not self.is_color_in_check(color) and not self.has_any_legal_move(color)
    def get_board_state(self, color):
        if self.is_checkmate(color):
            return "checkmate"
        elif self.is_stalemate(color):
            return "stalemate"
        elif self.is_color_in_check(color):
            return "check"
        else:
            return "normal"

