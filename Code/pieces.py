from board import Board
from typing import Literal
class Piece:
    def __init__(self, color: str, startPos: tuple, board: Board):
        self.color = color
        self.position = startPos
        self.board = board
        self.pointVal = -1
        self.board.board[startPos[0]][startPos[1]] = self
        self.directions = []  # this can be used to mutate the movement capabilities of pieces
        self.attackDir = self.directions.copy()
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
        for move in validMoves.copy():
            if self.does_move_leave_king_in_check(move):
                validMoves.remove(move)
        return validMoves
    def move(self, newPos):
        if newPos in self.get_valid_moves():
            self.board.board[self.position[0]][self.position[1]] = None
            self.position = newPos
            oldPiece = self.board.board[newPos[0]][newPos[1]]
            self.board.board[newPos[0]][newPos[1]] = self
            return newPos, oldPiece
        return -1, None
        #return new position
    def get_attack_squares(self): #used because in example of a pinned bishop, it can still block spaces of opposing king
        attacked = set()
        row, col = self.position
        for dr, dc in self.attackDir:
            r, c = row + dr, col + dc
            while (0 <= r < self.board.getRow() and 0 <= c < self.board.getCol()):
                attacked.add((r, c))
                if self.board.getPiece((r, c)) is not None: #stop at first occupied square regardless of color owner
                    break
                if not self.sliding:
                    break
                r += dr
                c += dc
        return attacked
    def does_move_leave_king_in_check(self, newPos: tuple):
        old_pos = self.getPos()
        movedSquare = self.board.getPiece(newPos)
        self.board.board[old_pos[0]][old_pos[1]] = None
        self.position = newPos
        self.board.board[newPos[0]][newPos[1]] = self

        in_check = self.board.is_color_in_check(self.getColor())

        self.board.board[newPos[0]][newPos[1]] = movedSquare
        self.board.board[old_pos[0]][old_pos[1]] = self
        self.position = old_pos
        return in_check


    
class Pawn(Piece):
    def __init__(self, color, startPos, board):
        super().__init__(color, startPos, board)
        self.pointVal = 1
        self.firstMove = True
        self.firstMoveTurnNo = -1
        self.firstMoveDoubleMove = False
        if self.color == "white":
            self.directions = [
                    (-1, 0) #up
                    ] # need to multiply by -1 if black (pawns move down internally instead)
            self.attackDir = [(-1, -1), (-1, 1)]
        else:
            self.directions = [
                    (1, 0) #down
            ]
            self.attackDir = [(1, -1), (1, 1)]
    def get_valid_moves(self):
        validMoves = set()
        row, col = self.getPos()
        for dr, dc in self.directions:
            r, c = row + dr, col + dc
            while(0 <= r < self.board.getRow() and 0 <= c < self.board.getCol()):
                piece = self.board.getPiece((r,c))
                if piece is None:
                    validMoves.add((r,c))
                """else:
                    if piece.getColor() != self.getColor():
                        validMoves.add((r,c))
                    break""" # not for a pawn
                doubleMove = r+dr
                if(0 <= doubleMove < self.board.getRow()):
                    if self.firstMove and self.board.getPiece((doubleMove,c)) is None and self.board.getPiece((r,c)) is None:
                        validMoves.add((doubleMove,c))
                if not self.sliding:
                    break
                r += dr
                c += dc
        attackSquares = self.get_attack_squares()
        leftPiece = None
        rightPiece = None
        if col > 0:
            leftPiece = self.board.getPiece((row, col - 1))
        if col < self.board.getCol() - 1:
            rightPiece = self.board.getPiece((row, col + 1))

        
        for square in attackSquares:
            if(self.board.getPiece(square) is not None):
                validMoves.add(square)
                continue
            if square[1] < self.position[1]: #left attack check for passent
                if(isinstance(leftPiece, Pawn) and leftPiece.firstMoveTurnNo == self.board.get_turn_count()-1 and leftPiece.getColor() != self.getColor() and leftPiece.firstMoveDoubleMove):
                    validMoves.add(square)
            elif square[1] > self.position[1]: #right attack check for passent
                if(isinstance(rightPiece, Pawn) and rightPiece.firstMoveTurnNo == self.board.get_turn_count()-1 and rightPiece.getColor() != self.getColor() and rightPiece.firstMoveDoubleMove):
                    validMoves.add(square)
        for move in validMoves.copy():
            if self.does_move_leave_king_in_check(move):
                validMoves.remove(move)
        return validMoves
    def move(self, newPos):
        oldPos = self.position
        move, takenpiece = super().move(newPos)
        if move == -1:
            return -1, None
        if self.firstMove:
            if abs(oldPos[0] - newPos[0]) == 2:
                self.firstMoveDoubleMove = True
            self.firstMove = False
            self.firstMoveTurnNo = self.board.get_turn_count()
        if takenpiece is None and oldPos[1] != newPos[1]: #this means we did en passent
            takenpiece = self.board.getPiece((self.position[0]-self.attackDir[0][0], self.position[1])) #go back/fwd to the peice that we moved behind since self.pos is already updated
            self.board.removePiece(takenpiece.position)
        if (move[0] == self.board.getRow() - 1 and self.getColor() == "black") or (move[0] == 0 and self.getColor() == "white"):
            self.promotion()
        return move, takenpiece
    def promotion(self):
        choices = {
            "bishop": Bishop,
            "knight": Knight,
            "rook": Rook,
            "queen": Queen
        }
        choice = input("Promote to: (bishop, knight, rook, queen): ").lower()
        while choice not in choices:
            print("Invalid choice, try again.")
            choice = input("Promote to: (bishop, knight, rook, queen): ").lower()
        newPiece = choices[choice](self.color, self.position, self.board) #due to our init we will automatically replace our pawn
        return newPiece
    def does_move_leave_king_in_check(self, newPos: tuple):
        old_pos = self.getPos()
        movedSquare = self.board.getPiece(newPos)
        if movedSquare is None and old_pos[1] != newPos[1]:
            self.board.board[old_pos[0]][old_pos[1]] = None
            self.position = newPos
            self.board.board[newPos[0]][newPos[1]] = self
            takenpiece = self.board.board[self.position[0]-self.attackDir[0][0]][self.position[1]]
            self.board.board[self.position[0]-self.attackDir[0][0]][self.position[1]] = None #takenpiece has enpassent piece

            in_check = self.board.is_color_in_check(self.getColor())

            self.board.board[newPos[0]][newPos[1]] = movedSquare
            self.board.board[old_pos[0]][old_pos[1]] = self
            self.board.board[self.position[0]-self.attackDir[0][0]][self.position[1]] = takenpiece
            self.position = old_pos
        else:
            self.board.board[old_pos[0]][old_pos[1]] = None
            self.position = newPos
            self.board.board[newPos[0]][newPos[1]] = self

            in_check = self.board.is_color_in_check(self.getColor())

            self.board.board[newPos[0]][newPos[1]] = movedSquare
            self.board.board[old_pos[0]][old_pos[1]] = self
            self.position = old_pos
        return in_check
        

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
        self.attackDir = self.directions.copy()



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
        self.attackDir = self.directions.copy()

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
        self.attackDir = self.directions.copy()
    def move(self, newPos):
        move, takenpiece = super().move(newPos)
        if move != -1:
            self.hasMoved = True
        return move, takenpiece



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
        self.attackDir = self.directions.copy()

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
        self.attackDir = self.directions.copy()




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

        if self.board.is_color_in_check(self.getColor()):
            return False
        all_enemy_attacks = set()
        for r in range(self.board.getRow()):
            for c in range(self.board.getCol()):
                piece = self.board.getPiece((r,c))
                if piece is not None and piece.getColor() != self.getColor():
                    all_enemy_attacks.update(piece.get_attack_squares())
        for step in range(1, 3): #checks that the king does not move through check
            if (row, col+(step*left_right)) in all_enemy_attacks:
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
        rooksPos = []
        for r in range(self.board.getRow()):
            for c in range(self.board.getCol()):
                piece = self.board.getPiece((r,c))
                if isinstance(piece, Rook) and piece.getColor() == self.getColor():
                    rooksPos.append(piece.getPos())
        for elem in rooksPos:
            l_or_r = 0
            if elem[1] > self.getPos()[1]:
                l_or_r = 1
            elif elem[1] < self.getPos()[1]:
                l_or_r = -1
            if self.can_castle_with_rook_in_col(elem[1], l_or_r):
                moves.add((self.getPos()[0], self.getPos()[1]+(2*l_or_r)))
        return moves
        
    def move(self, newPos):
        old_row, old_col = self.getPos()
        is_castling = False
        if newPos[0] == old_row and abs(newPos[1] - old_col) == 2:
            is_castling = True
        move, takenpiece = super().move(newPos)
        if move == -1:
            return -1, None
        self.hasMoved = True



        if is_castling:
            rook_old_col = None
            if newPos[1] > old_col:
                for c in range(old_col+1, self.board.getCol()):
                    piece = self.board.getPiece((old_row, c))
                    if isinstance(piece, Rook) and not piece.hasMoved:
                        rook_old_col = c #if there are multiple rooks in a row, we castle with the first rook at least 2 spaces away
                        break
                rook_new_col = old_col + 1
            else:
                for c in range(old_col-1, -1, -1):
                    piece = self.board.getPiece((old_row, c))
                    if isinstance(piece, Rook) and not piece.hasMoved:
                        rook_old_col = c #if there are multiple rooks in a row, we castle with the first rook at least 2 spaces away
                        break
                rook_new_col = old_col - 1
            if rook_old_col is not None:
                rook = self.board.getPiece((old_row, rook_old_col))
                if rook:
                    self.board.board[old_row][rook_old_col] = None
                    rook.position = (old_row, rook_new_col)
                    self.board.board[old_row][rook_new_col] = rook
                    rook.hasMoved = True
        return move, takenpiece