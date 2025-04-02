from abc import ABC, abstractmethod
from enum import Enum, auto
import chess_items as ci
import pygame


class Color(Enum):

    WHITE = auto()
    BLACK = auto()


class Piece(ABC):
    symbol: str = "?"
    is_clicked = False


    def __init__(self, pos: str, color: Color) -> None:
        self.pos: str = pos
        self.color: Color = color

    def __repr__(self) -> str:
        return f"Piece: {self.symbol} {self.color}"

    def square_in_board(self, target: str) -> bool:
        letter, number = target[0], target[1]
        if letter.isalpha() and number.isnumeric():
            if letter in "abcdefgh" and number in "12345678":
                return True
        return False

    @abstractmethod
    def can_move(self, target: str) -> bool:
        pass


class Rook(Piece):

    has_castled = False

    def __init__(self, pos: str, color: Color) -> None:
        super().__init__(pos, color)
        self.symbol = "wR" if self.color == Color.WHITE else "bR"
        self.img = pygame.transform.scale(
            ci.WHITE_ROOK if self.color == Color.WHITE else ci.BLACK_ROOK, (70, 70)
        )

    def can_move(self, target: str) -> bool:
        if self.square_in_board(target):
            if target[0] == self.pos[0] or target[1] == self.pos[1]:
                return True
        return False


class Bishop(Piece):
    def __init__(self, pos: str, color: Color) -> None:
        super().__init__(pos, color)
        self.symbol = "wB" if self.color == Color.WHITE else "bB"
        self.img = pygame.transform.scale(
            ci.WHITE_BISHOP if self.color == Color.WHITE else ci.BLACK_BISHOP, (70, 70)
        )

    def can_move(self, target: str) -> bool:
        if self.square_in_board(target):
            if abs(ord(target[0]) - ord(self.pos[0])) == abs(
                int(target[1]) - int(self.pos[1])
            ):
                return True
        return False


class Queen(Piece):
    def __init__(self, pos: str, color: Color) -> None:
        super().__init__(pos, color)
        self.symbol = "wQ" if self.color == Color.WHITE else "bQ"
        self.img = pygame.transform.scale(
            ci.WHITE_QUEEN if self.color == Color.WHITE else ci.BLACK_QUEEN, (70, 70)
        )

    def can_move(self, target: str) -> bool:
        if self.square_in_board(target):
            if target[0] == self.pos[0] or target[1] == self.pos[1]:
                return True
            elif abs(ord(target[0]) - ord(self.pos[0])) == abs(
                int(target[1]) - int(self.pos[1])
            ):
                return True
        return False


class King(Piece):

    in_check = False
    has_castled = True

    def __init__(self, pos: str, color: Color) -> None:
        super().__init__(pos, color)
        self.symbol = "wK" if self.color == Color.WHITE else "bK"
        self.img = pygame.transform.scale(
            ci.WHITE_KING if self.color == Color.WHITE else ci.BLACK_KING, (70, 70)
        )

    def castle(self, target: str) -> bool:
        if self.square_in_board(target):
            if target[1] == self.pos[1] and abs(ord(target[0]) - ord(self.pos[0])) == 2:
                return True
        return False

    def can_move(self, target: str) -> bool:
        if self.square_in_board(target):
            if (
                abs(ord(target[0]) - ord(self.pos[0])) <= 1
                and abs(int(target[1]) - int(self.pos[1])) <= 1
            ):
                return True
            elif (
                target[1] == self.pos[1]
                and abs(ord(target[0]) - ord(self.pos[0])) == 2
                and not self.has_castled
                and not self.in_check
                and self.pos[0] == "e"
            ):
                return True
        return False


class Knight(Piece):

    def __init__(self, pos: str, color: Color) -> None:
        super().__init__(pos, color)
        self.symbol = "wN" if self.color == Color.WHITE else "bN"
        self.img = pygame.transform.scale(
            ci.WHITE_KNIGHT if self.color == Color.WHITE else ci.BLACK_KNIGHT, (70, 70)
        )

    def can_move(self, target: str) -> bool:
        if self.square_in_board(target):
            if (
                abs(ord(target[0]) - ord(self.pos[0])) == 2
                and abs(int(target[1]) - int(self.pos[1])) == 1
            ):
                return True
            elif (
                abs(ord(target[0]) - ord(self.pos[0])) == 1
                and abs(int(target[1]) - int(self.pos[1])) == 2
            ):
                return True
        return False


class Pawn(Piece):

    jump = False  # If the pawn moves two squares, jump will be True

    def __init__(self, pos: str, color: Color) -> None:
        super().__init__(pos, color)
        self.symbol = "wP" if self.color == Color.WHITE else "bP"
        self.img = pygame.transform.scale(
            ci.WHITE_PAWN if self.color == Color.WHITE else ci.BLACK_PAWN, (70, 70)
        )

    def move_diagonal(self, target: str, color: Color) -> bool:
        if color == Color.WHITE:
            if abs(ord(target[0]) - ord(self.pos[0])) == 1:
                if int(target[1]) - int(self.pos[1]) == 1:
                    return True
        else:
            if abs(ord(target[0]) - ord(self.pos[0])) == 1:
                if int(target[1]) - int(self.pos[1]) == -1:
                    return True
        return False

    def can_promote(self, target: str) -> bool:
        if self.color == Color.WHITE:
            if target[1] == "8":
                return True
        else:
            if target[1] == "1":
                return True
        return False

    def can_move(self, target: str) -> bool:
        if self.square_in_board(target):
            if self.color == Color.WHITE:
                if target[0] == self.pos[0]:
                    if int(target[1]) - int(self.pos[1]) == 1:
                        return True
                    elif int(target[1]) - int(self.pos[1]) == 2 and self.pos[1] == "2":
                        self.jump = True
                        return True
                else:
                    return self.move_diagonal(target, self.color)  # Capture diagonally
            elif self.color == Color.BLACK:
                if target[0] == self.pos[0]:
                    if int(target[1]) - int(self.pos[1]) == -1:
                        return True
                    elif int(target[1]) - int(self.pos[1]) == -2 and self.pos[1] == "7":
                        self.jump = True
                        return True
                else:
                    return self.move_diagonal(target, self.color)  # Capture diagonally
        return False
