from pieces import *
from board import *
from typing import Union
import time
import pygame
import chess_items as ci
import tkinter as tk
from cryptography.fernet import Fernet
from tkinter import ttk, messagebox
import os

pygame.font.init()
pygame.mixer.init()

status = False


# Генерация ключа для шифрования
def generate_key():
    return Fernet.generate_key()

# Сохранение ключа в файл
def save_key(key):
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Загрузка ключа из файла
def load_key():
    return open("secret.key", "rb").read()

# Шифрование пароля
def encrypt_password(password):
    key = load_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Расшифровка пароля
def decrypt_password(encrypted_password):
    key = load_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

# Сохранение логина и пароля в файл
def save_credentials(username, password):
    with open("credentials.txt", "a") as f:
        f.write(f"{username}:{password.decode()}\n")

# Проверка учетных данных
def check_credentials(username, password):
    try:
        with open("credentials.txt", "r") as f:
            for line in f:
                stored_username, stored_password = line.strip().split(":")
                if stored_username == username and decrypt_password(stored_password.encode()) == password:
                    return True
    except FileNotFoundError:
        pass
    return False

# Функция для обработки регистрации
def register():
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        encrypted_password = encrypt_password(password)
        save_credentials(username, encrypted_password)
        messagebox.showinfo("Успех", "Регистрация успешна!")
    else:
        messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля.")

# Функция для обработки входа
def login():
    global status
    username = entry_login_username.get()
    password = entry_login_password.get()

    if check_credentials(username, password):
        messagebox.showinfo("Успех", "Вход выполнен успешно!")
        status = True
        root.destroy()
        # Здесь можно открыть окно игры или другое окно
    else:
        messagebox.showerror("Ошибка", "Пользователь не зарегистрирован или введены неверные учётные данные.")

# Создание ключа и его сохранение (выполнить один раз)
if not os.path.exists("secret.key"):
    key = generate_key()
    save_key(key)

# Создание основного окна
root = tk.Tk()
root.title("Регистрация и Вход")
root.geometry('%dx%d+%d+%d' % (500, 500, 670, 290))

# Создание вкладок
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both")

# Вкладка регистрации
register_tab = ttk.Frame(notebook)
notebook.add(register_tab, text="Регистрация")

label_username = tk.Label(register_tab, text="Имя пользователя:")
label_username.place(x=50, y=50)
entry_username = tk.Entry(register_tab)
entry_username.place(x=200, y=50)

label_password = tk.Label(register_tab, text="Пароль:")
label_password.place(x=50, y=100)
entry_password = tk.Entry(register_tab, show="*")
entry_password.place(x=200, y=100)

button_register = tk.Button(register_tab, text="Зарегистрироваться", command=register)
button_register.place(x=150, y=150)

# Вкладка входа
login_tab = ttk.Frame(notebook)
notebook.add(login_tab, text="Вход")

label_login_username = tk.Label(login_tab, text="Имя пользователя:")
label_login_username.place(x=50, y=50)
entry_login_username = tk.Entry(login_tab)
entry_login_username.place(x=200, y=50)

label_login_password = tk.Label(login_tab, text="Пароль:")
label_login_password.place(x=50, y=100)
entry_login_password = tk.Entry(login_tab, show="*")
entry_login_password.place(x=200, y=100)

button_login = tk.Button(login_tab, text="Войти", command=login)
button_login.place(x=150, y=150)

root.mainloop()



# Screen
WIDTH, HEIGHT = 820, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Шахматы")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BROWN = (166, 119, 91)
LIGHT_GRAY = (173, 170, 166)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

FONT = pygame.font.SysFont("comicsans", 24)
MATE_FONT = pygame.font.SysFont("comicsans", 100)
WINNER_FONT = pygame.font.SysFont("comicsans", 70)

CHECK_TEXT = FONT.render("Шах!", True, RED)
CHECKMATE_TEXT = MATE_FONT.render("Мат!", True, RED)
STALEMATE_TEXT = MATE_FONT.render("Ничья!", True, RED)
PROMOTION_TEXT = FONT.render("Выберите фигуру", True, BLACK)


def draw_screen(
    board: Board,
    current_player: Color,
    piece_moves: list[str],
    draw_moves: bool,
    check: bool,
    is_flipped: bool,
    auto_flip: bool,
) -> None:
    SCREEN.fill(WHITE)
    SCREEN.blit(ci.CHESS_BOARD, (0, 0))

    pygame.draw.rect(SCREEN, DARK_BROWN, (600, 380, 400, 220))
    draw_current_player(current_player)
    SCREEN.blit(CHECK_TEXT, (665, 520)) if check else None

    draw_pieces(board, is_flipped)
    if draw_moves:
        draw_available_moves(piece_moves, is_flipped)

    draw_options(auto_flip)
    SCREEN.blit(ci.RESET_BUTTON, (760, 560))
    pygame.display.update()


def draw_pieces(board: Board, is_flipped: bool) -> None:
    squares = board.squares
    for row in range(len(squares)):
        for col in range(len(squares[row])):
            piece: Union[Piece, None] = squares[row][col]
            if piece is not None:
                r, c = get_row_col_with_flip(row, col, is_flipped)
                if piece.is_clicked:
                    pygame.draw.rect(SCREEN, YELLOW, (c * 75, r * 75, 75, 75))
                SCREEN.blit(piece.img, (c * 75, r * 75))


def draw_options(auto_flip: bool) -> None:
    auto_flip_text = FONT.render("Авто поворот", True, BLACK)
    flip_text = FONT.render("Поворот", True, BLACK)
    SCREEN.blit(auto_flip_text, (610, 386))
    SCREEN.blit(flip_text, (610, 420))
    if auto_flip:
        SCREEN.blit(ci.ON_BUTTON, (770, 390))
    else:
        SCREEN.blit(ci.OFF_BUTTON, (770, 390))
    SCREEN.blit(ci.FLIP_ICON, (770, 425))


def draw_winner(current_player: Color, is_checkmate: bool) -> None:
    if is_checkmate:
        SCREEN.blit(CHECKMATE_TEXT, (100, 200))
        winner_color = "Чёрные" if current_player == Color.WHITE else "Белые"
        winner_text = WINNER_FONT.render(f"{winner_color} победили!!!", True, BLACK)
        SCREEN.blit(winner_text, (90, 300))
    else:
        SCREEN.blit(STALEMATE_TEXT, (100, 200))
    pygame.display.update()


def draw_available_moves(piece_moves: list[str], is_flipped: bool) -> None:
    for move in piece_moves:
        row, col = get_row_col(move)
        row, col = get_row_col_with_flip(row, col, is_flipped)
        pygame.draw.circle(SCREEN, DARK_BROWN, (col * 75 + 37, row * 75 + 37), 10)


def draw_current_player(current_player: Color) -> None:
    current_text = FONT.render("Ход:", True, BLACK)
    player: str = "Белых" if current_player == Color.WHITE else "Чёрных"
    color_of_player = WHITE if current_player == Color.WHITE else BLACK
    current_player_text = FONT.render(player, True, color_of_player)
    SCREEN.blit(current_text, (680, 460))
    SCREEN.blit(current_player_text, (670, 490))


def draw_promote_options() -> None:
    pygame.draw.rect(SCREEN, LIGHT_GRAY, (600, 0, 400, 150))
    SCREEN.blit(PROMOTION_TEXT, (610, 20))
    SCREEN.blit(ci.WHITE_QUEEN, (630, 50))
    SCREEN.blit(ci.WHITE_ROOK, (720, 50))
    SCREEN.blit(ci.WHITE_KNIGHT, (630, 100))
    SCREEN.blit(ci.WHITE_BISHOP, (720, 100))
    pygame.display.update()


def get_row_col_with_flip(row: int, col: int, is_flipped: bool) -> tuple[int]:
    if is_flipped:
        return 7 - row, 7 - col
    return row, col


def validate_chosen_piece(current_player: Color, board: Board, index: tuple[int]) -> bool:
    piece: Union[Piece, None] = board.squares[index[0]][index[1]]

    if piece is None:
        return False
    elif piece.color != current_player:
        return False
    else:
        piece_moves: list[str] = board.get_valid_moves(piece.pos)
        actual_piece_moves: list[str] = board.moves_to_not_in_check(piece, piece_moves)
        if len(actual_piece_moves) == 0:
            return False
    return True


def get_piece_moves(board: Board, piece: Piece) -> list[str]:
    piece_moves: list[str] = board.get_valid_moves(piece.pos)
    actual_piece_moves: list[str] = board.moves_to_not_in_check(piece, piece_moves)
    return actual_piece_moves


def validate_target_piece(
    board: Board, piece: Piece, piece_moves: list[str], index: tuple[int]
) -> bool:
    target_square: str = get_square_name(index[0], index[1])
    if target_square == piece.pos:
        return False
    if target_square not in piece_moves:
        return False
    if board.get_checked_when_move(piece, target_square):
        return False
    return True


def promotion() -> Union[type, None]:
    draw_promote_options()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 630 <= pos[0] <= 690:
                    if 50 <= pos[1] <= 100:
                        return Queen
                    elif 100 <= pos[1] <= 150:
                        return Knight
                elif 720 <= pos[0] <= 780:
                    if 50 <= pos[1] <= 100:
                        return Rook
                    elif 100 <= pos[1] <= 150:
                        return Bishop


def move(board: Board, piece: Piece, chosen_square: str, target_square: str) -> None:
    is_a_pawn: bool = isinstance(piece, Pawn)
    is_a_king: bool = isinstance(piece, King)
    promote_type = None
    if is_a_pawn:  # Check for promotion
        if piece.can_promote(target_square):
            promote_type = promotion()
    if is_a_king:
        do_castle: bool = piece.castle(target_square)
    board.update(
        chosen_square,
        target_square,
        is_pawn=is_a_pawn,
        do_castle=(is_a_king and do_castle),
    )
    piece.pos = target_square
    if promote_type is not None:
        promote_piece_row, promote_piece_col = get_row_col(target_square)
        board.squares[promote_piece_row][promote_piece_col] = promote_type(
            target_square, piece.color
        )
    ci.MOVE_SOUND.play()


def start():
    board: Board = Board()
    auto_flip: bool = False
    is_flipped: bool = False
    current_player: Color = Color.WHITE
    is_choosing_target: bool = False
    can_move_piece: bool = False
    check: bool = False
    is_mate: bool = False
    is_checkmate: bool = False
    piece_moves: list[str] = []

    running = True
    while running:
        if auto_flip:
            is_flipped: bool = current_player == Color.BLACK
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = pygame.mouse.get_pos()
                if 760 <= row <= 790 and 385 <= col <= 405:
                    auto_flip = not auto_flip
                if 760 <= row <= 790 and 420 <= col <= 440:
                    auto_flip = False
                    is_flipped = not is_flipped
                if 760 <= row and 560 <= col:
                    board = Board()
                    current_player = Color.WHITE
                row = row // 75
                col = col // 75
                row, col = get_row_col_with_flip(row, col, is_flipped)
                if 0 <= row < 8 and 0 <= col < 8:
                    if not is_choosing_target:
                        if validate_chosen_piece(current_player, board, (col, row)):
                            piece: Piece = board.squares[col][row]
                            piece.is_clicked = True
                            piece_moves: list[str] = get_piece_moves(
                                board, board.squares[col][row]
                            )
                            is_choosing_target = True
                    else:
                        is_choosing_target = False
                        if validate_target_piece(board, piece, piece_moves, (col, row)):
                            can_move_piece = True
                            target: str = get_square_name(col, row)
                            current_player = (
                                Color.BLACK
                                if current_player == Color.WHITE
                                else Color.WHITE
                            )
                        else:
                            piece.is_clicked = False
        if can_move_piece:
            king_pos: str = board.get_king_pos(get_opposite_color(piece.color))
            king: King = board.get_piece(king_pos)
            move(board, piece, piece.pos, target)
            # If check
            if board.can_check(board.get_piece(target)):
                king.in_check = True
                check = True
                moves_to_cover_check: list = board.move_to_avoid_mate(
                    get_opposite_color(piece.color)
                )
                king_moves_to_live: list = board.get_valid_moves(king_pos)
                # If there are moves to cover check
                if moves_to_cover_check:
                    # Extend with the king's moves
                    moves_to_cover_check.extend(king_moves_to_live)
                else:  # If there are no moves to cover check
                    if not king_moves_to_live:
                        is_mate = True
                        is_checkmate = True
            else:  #  If not check
                king.in_check = False
                check = False
                if board.stalemate(get_opposite_color(piece.color)):
                    is_mate = True
            can_move_piece = False
            piece.is_clicked = False

        draw_screen(
            board,
            current_player,
            piece_moves,
            is_choosing_target,
            check,
            is_flipped,
            auto_flip,
        )
        if is_mate:
            draw_winner(current_player, is_checkmate)
            time.sleep(5)
            running = False
    pygame.quit()


if __name__ == "__main__":
    if status:
        start()