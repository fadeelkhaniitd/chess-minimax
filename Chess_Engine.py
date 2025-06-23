import os
import time
import argparse
import datetime as dt
from random import choice
from math import inf
from time import perf_counter as pc

import chess
import chess.pgn
import pygame

# Initialization
pygame.init()

# =================== Config ===================
parser = argparse.ArgumentParser(description="Run the Python Chess Engine")
parser.add_argument('--takeback', action='store_true', help='Enable takeback feature')
# Time control arguments
parser.add_argument('--time', type=int, default=300, help='Total time per side in seconds (default: 300)')
parser.add_argument('--inc', type=int, default=0, help='Increment per move in seconds (default: 0)')
args = parser.parse_args()

TAKEBACK_ENABLED = args.takeback
TOTAL_TIME = args.time
INCREMENT = args.inc

# Time control state
remaining_time = {chess.WHITE: TOTAL_TIME, chess.BLACK: TOTAL_TIME}
move_start_time = None

# Evaluation function
from evaluation import evaluation

# GUI Dimensions
BOARD_SIZE = 400
CLOCK_HEIGHT = 40
TAKEBACK_HEIGHT = 60
X = BOARD_SIZE
Y = BOARD_SIZE + 2 * CLOCK_HEIGHT + (TAKEBACK_HEIGHT if TAKEBACK_ENABLED else 0)

# Colors
BG_COLOR = (235, 235, 235)
LIGHT_SQUARE = (238, 238, 210)
DARK_SQUARE = (118, 150, 86)
MOVE_BLUE = (130, 191, 255)
MOVE_RED = (255, 110, 120)

# Load fonts
font_50 = pygame.font.Font("ChessImages/bahnschrift.ttf", 50)
font_30 = pygame.font.Font("ChessImages/bahnschrift.ttf", 30)

# Create window
chessWindow = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Chess Engine')
pygame.display.set_icon(pygame.image.load('ChessImages/chess-board.png'))

# Piece images
PIECE_IMAGES = {
    "R": pygame.image.load("ChessImages/white_rook.png"),
    "r": pygame.image.load("ChessImages/black_rook.png"),
    "N": pygame.image.load("ChessImages/white_knight.png"),
    "n": pygame.image.load("ChessImages/black_knight.png"),
    "B": pygame.image.load("ChessImages/white_bishop.png"),
    "b": pygame.image.load("ChessImages/black_bishop.png"),
    "Q": pygame.image.load("ChessImages/white_queen.png"),
    "q": pygame.image.load("ChessImages/black_queen.png"),
    "K": pygame.image.load("ChessImages/white_king.png"),
    "k": pygame.image.load("ChessImages/black_king.png"),
    "P": pygame.image.load("ChessImages/white_pawn.png"),
    "p": pygame.image.load("ChessImages/black_pawn.png"),
    "_": None,
}

# State
playercolor = 1  # default value (white)
game_moves = []
move_ordering_table = []
is_running = True

# GUI elements for takeback
takeback = font_50.render("Takeback", True, (50, 50, 50), BG_COLOR)
takeback_rect = takeback.get_rect(center=(200, 450))

# Game setup
board = chess.Board()
starting_fen = chess.STARTING_FEN
board.set_fen(starting_fen)

game = chess.pgn.Game()
x = dt.datetime.now()
game.headers.update({
    'Event': 'Chess Engine',
    'Date': x.strftime("%Y.%m.%d")
})
i = 1
while os.path.exists(f"PGNs/game{i}.pgn"):
    i += 1

# --- Move Ordering Helper ---
def move_ordering(board, only_captures=False):
    move_scores = []
    for move in board.legal_moves:
        if only_captures and not board.is_capture(move):
            continue
        score = 0
        # Captures: MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
        if board.is_capture(move):
            victim = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)
            if victim and attacker:
                values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
                score += 10 * values[victim.piece_type] - values[attacker.piece_type]
            else:
                score += 5  # fallback for en passant or promotion
        # Checks
        board.push(move)
        if board.is_check():
            score += 2
        board.pop()
        # Promotions
        if move.promotion:
            score += 8
        move_scores.append((score, move))
    move_scores.sort(reverse=True, key=lambda x: x[0])
    return [move for score, move in move_scores]

# --- Quiescence Search (no transposition table) ---
def quiescence(board, alpha, beta, maximizing):
    stand_pat = evaluation(board)
    if maximizing:
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat
    else:
        if stand_pat <= alpha:
            return alpha
        if beta > stand_pat:
            beta = stand_pat
    for move in move_ordering(board, only_captures=True):
        board.push(move)
        score = quiescence(board, alpha, beta, not maximizing)
        board.pop()
        if maximizing:
            if score > alpha:
                alpha = score
            if alpha >= beta:
                break
        else:
            if score < beta:
                beta = score
            if beta <= alpha:
                break
    return alpha if maximizing else beta

# --- Minimax with Alpha-Beta, Move Ordering, Quiescence (no TT) ---
def computermove(depth=4, time_left=None):
    import copy
    import time
    search_board = board.copy()
    def minimax(board, depth, alpha, beta, maximizing, time_limit=None, start_time=None):
        if time_limit is not None and start_time is not None:
            if time.time() - start_time > time_limit:
                return None, None  # Signal timeout
        if depth == 0 or board.is_game_over():
            return quiescence(board, alpha, beta, maximizing), None
        best_move = None
        moves = move_ordering(board)
        if maximizing:
            max_eval = -inf
            for move in moves:
                board.push(move)
                eval, _ = minimax(board, depth - 1, alpha, beta, False, time_limit, start_time)
                board.pop()
                if eval is None:
                    return None, None  # Timeout
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = inf
            for move in moves:
                board.push(move)
                eval, _ = minimax(board, depth - 1, alpha, beta, True, time_limit, start_time)
                board.pop()
                if eval is None:
                    return None, None  # Timeout
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
    maximizing = board.turn
    # Dynamic time allocation
    if time_left is not None:
        time_limit = max(1.0, time_left * 0.02)
    else:
        time_limit = None
    best_move = None
    best_score = None
    start_time = time.time() if time_limit is not None else None
    for d in range(1, depth + 10):  # Allow going deeper if time allows
        elapsed = time.time() - start_time if start_time is not None else 0
        if time_limit is not None and elapsed > time_limit:
            break
        score, move = minimax(search_board, d, -inf, inf, maximizing, time_limit, start_time)
        if score is None or move is None:
            break  # Timeout during this depth
        best_move = move
        best_score = score
    if best_move:
        board.push(best_move)
        game_moves.append(best_move)
        updateWindow()

def format_time(secs):
    mins = int(secs // 60)
    s = int(secs % 60)
    return f"{mins}:{s:02}"

def updateWindow(live_white_time=None, live_black_time=None, highlight_moves=None, selected_square=None):
    chessWindow.fill(color=BG_COLOR)
    font = font_30
    # Clamp times to zero for display
    white_time = max(0, live_white_time if live_white_time is not None else remaining_time[chess.WHITE])
    black_time = max(0, live_black_time if live_black_time is not None else remaining_time[chess.BLACK])
    board_top = CLOCK_HEIGHT
    board_left = (X - BOARD_SIZE) // 2
    # Draw clocks in correct orientation
    if playercolor == 1:
        black_clock = font.render(f"Black: {format_time(black_time)}", True, (20,20,20), BG_COLOR)
        black_rect = black_clock.get_rect(center=(X//2, CLOCK_HEIGHT//2))
        chessWindow.blit(black_clock, black_rect)
        white_clock = font.render(f"White: {format_time(white_time)}", True, (20,20,20), BG_COLOR)
        white_rect = white_clock.get_rect(center=(X//2, BOARD_SIZE + CLOCK_HEIGHT + CLOCK_HEIGHT//2))
        chessWindow.blit(white_clock, white_rect)
    else:
        white_clock = font.render(f"White: {format_time(white_time)}", True, (20,20,20), BG_COLOR)
        white_rect = white_clock.get_rect(center=(X//2, CLOCK_HEIGHT//2))
        chessWindow.blit(white_clock, white_rect)
        black_clock = font.render(f"Black: {format_time(black_time)}", True, (20,20,20), BG_COLOR)
        black_rect = black_clock.get_rect(center=(X//2, BOARD_SIZE + CLOCK_HEIGHT + CLOCK_HEIGHT//2))
        chessWindow.blit(black_clock, black_rect)
    # Build board matrix for display
    board_matrix = [[None for _ in range(8)] for _ in range(8)]
    for y in range(8):
        for x in range(8):
            if playercolor == 1:
                sq = chess.square(x, 7 - y)
            else:
                sq = chess.square(7 - x, y)
            piece = board.piece_at(sq)
            board_matrix[y][x] = piece.symbol() if piece else "_"
    # Draw board
    for y in range(8):
        for x in range(8):
            image = PIECE_IMAGES.get(board_matrix[y][x])
            rect = pygame.Rect(board_left + (50 * x), board_top + (50 * y), 50, 50)
            if (x + y) % 2 == 1:
                pygame.draw.rect(chessWindow, DARK_SQUARE, rect)
            else:
                pygame.draw.rect(chessWindow, LIGHT_SQUARE, rect)
            if image is not None:
                chessWindow.blit(image, rect.topleft)
    # Highlight selected square and moves
    if highlight_moves is not None and selected_square is not None:
        sel_file = chess.square_file(selected_square)
        sel_rank = chess.square_rank(selected_square)
        if playercolor == 1:
            sx = board_left + sel_file * 50
            sy = board_top + (7 - sel_rank) * 50
        else:
            sx = board_left + (7 - sel_file) * 50
            sy = board_top + sel_rank * 50
        pygame.draw.rect(chessWindow, (255, 255, 0), pygame.Rect(sx, sy, 50, 50), 4)
        for move in highlight_moves:
            to_file = chess.square_file(move.to_square)
            to_rank = chess.square_rank(move.to_square)
            if playercolor == 1:
                tx = board_left + to_file * 50
                ty = board_top + (7 - to_rank) * 50
            else:
                tx = board_left + (7 - to_file) * 50
                ty = board_top + to_rank * 50
            color = MOVE_RED if board.is_capture(move) else MOVE_BLUE
            pygame.draw.rect(chessWindow, color, pygame.Rect(tx, ty, 50, 50), 4)
    # Takeback button (fixed position below everything)
    if TAKEBACK_ENABLED:
        takeback_y = BOARD_SIZE + 2 * CLOCK_HEIGHT + (TAKEBACK_HEIGHT // 2)
        takeback_rect_centered = takeback.get_rect(center=(X//2, takeback_y))
        chessWindow.blit(takeback, takeback_rect_centered)
    pygame.display.update()

def choose_player_color():
    chessWindow.fill(color=BG_COLOR)
    white_img = PIECE_IMAGES.get('K')
    black_img = PIECE_IMAGES.get('k')
    white_rect = white_img.get_rect()
    black_rect = black_img.get_rect()
    white_rect.center = ((X-150)//2, 5*Y//8)
    black_rect.center = ((X-150)//2 + 150, 5*Y//8)
    chessWindow.blit(white_img, white_rect)
    chessWindow.blit(black_img, black_rect)
    text = font_30.render('Choose color by clicking', True, (20, 20, 20), BG_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (X//2, 3*Y//8)
    chessWindow.blit(text, text_rect)
    pygame.display.update()
    selected = False
    while not selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = pygame.mouse.get_pos()
                if 5*Y//8 - 25 <= mousey <= 5*Y//8 + 25:
                    if (X-150)//2 - 25 <= mousex <= (X-150)//2 + 25:
                        return 1
                    elif (X-150)//2 + 125 <= mousex <= (X-150)//2 + 175:
                        return -1

def playermove():
    piece_selected = False
    moved = False
    move_start = time.time()
    clock = pygame.time.Clock()
    board_left = (X - BOARD_SIZE) // 2
    board_top = CLOCK_HEIGHT
    selected_square = None
    highlight_moves = None
    while not moved:
        now = time.time()
        live_time = max(0, remaining_time[board.turn] - (now - move_start))
        # Immediate time forfeit for human
        if live_time <= 0:
            updateWindow(live_white_time=0 if board.turn == chess.WHITE else None,
                         live_black_time=0 if board.turn == chess.BLACK else None)
            game_over("White lost on time" if board.turn == chess.WHITE else "Black lost on time")
            return
        # Only highlight if a piece is selected
        updateWindow(live_white_time=live_time if board.turn == chess.WHITE else None,
                     live_black_time=live_time if board.turn == chess.BLACK else None,
                     highlight_moves=highlight_moves, selected_square=selected_square)
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if TAKEBACK_ENABLED:
                    if y > BOARD_SIZE + 2 * CLOCK_HEIGHT:
                        try:
                            board.pop()
                            game_moves.pop()
                        except: pass
                        try:
                            board.pop()
                            game_moves.pop()
                        except: pass
                        updateWindow()
                        continue
                if piece_selected == False:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if playercolor == 1:
                        file = (mouse_x - board_left) // 50
                        rank = 7 - ((mouse_y - board_top) // 50)
                    else:
                        file = 7 - ((mouse_x - board_left) // 50)
                        rank = ((mouse_y - board_top) // 50)
                    if not (0 <= file < 8 and 0 <= rank < 8):
                        continue
                    piece = board.piece_at(chess.square(file, rank))
                    if piece != None:
                        if piece.color == board.turn:
                            piece_selected = True
                            selected_square = chess.square(file, rank)
                            highlight_moves = [move for move in board.legal_moves if move.from_square == selected_square]
                            continue  # Go to next frame to show highlights
                elif piece_selected == True:
                    mouse_x2, mouse_y2 = pygame.mouse.get_pos()
                    if playercolor == 1:
                        file2 = (mouse_x2 - board_left) // 50
                        rank2 = 7 - ((mouse_y2 - board_top) // 50)
                    else:
                        file2 = 7 - ((mouse_x2 - board_left) // 50)
                        rank2 = ((mouse_y2 - board_top) // 50)
                    if not (0 <= file2 < 8 and 0 <= rank2 < 8):
                        piece_selected = False
                        selected_square = None
                        highlight_moves = None
                        continue
                    for move in highlight_moves:
                        if move.to_square == (8 * rank2) + file2:
                            if move.promotion == None:
                                moved = True
                                board.push(move)
                                game_moves.append(move)
                                updateWindow()
                                return move
                            else:
                                dict1 = {1: ['Q', 'R', 'B', 'N'], -1: ['q', 'r', 'b', 'n']}
                                moved = False
                                piece_selected = None
                                selected_square = None
                                highlight_moves = None
                                chessWindow.fill(MOVE_RED)
                                chessWindow.blit(PIECE_IMAGES.get(dict1.get(playercolor)[0]), (100, 175 - 75 * playercolor))
                                chessWindow.blit(PIECE_IMAGES.get(dict1.get(playercolor)[1]), (150, 175 - 75 * playercolor))
                                chessWindow.blit(PIECE_IMAGES.get(dict1.get(playercolor)[2]), (200, 175 - 75 * playercolor))
                                chessWindow.blit(PIECE_IMAGES.get(dict1.get(playercolor)[3]), (250, 175 - 75 * playercolor))
                                pygame.display.update()
                                break
                    piece_selected = False
                    selected_square = None
                    highlight_moves = None
                elif piece_selected == None:
                    mousex3, mousey3 = pygame.mouse.get_pos()
                    mousex3 = (mousex3 - board_left) // 50
                    mousey3 = (mousey3 - board_top) // 50
                    color_mousey3_conversion = {1:2, -1:5}
                    if mousey3 == color_mousey3_conversion.get(playercolor):
                        if mousex3 == 2: move.promotion = chess.QUEEN
                        elif mousex3 == 3: move.promotion = chess.ROOK
                        elif mousex3 == 4: move.promotion = chess.BISHOP
                        elif mousex3 == 5: move.promotion = chess.KNIGHT
                        board.push(move)
                        game_moves.append(move)
                        moved = True
                        updateWindow()
                        return move

def game_over(reason=None):
    node = game
    for move in game_moves:
        node = node.add_variation(move)
    # Prepare result message
    if reason:
        result_msg = reason
    elif board.outcome():
        result_msg = str(board.outcome().termination).split('.')[1]
    else:
        result_msg = "Game over"
    # Save PGN
    game.headers['Result'] = board.result() if board.outcome() else '*'
    with open(f"PGNs/game{i}.pgn", "w") as file:
        file.write(f"{game}\n")
    # Show result message on screen with overlay
    updateWindow()
    overlay = pygame.Surface((X, Y), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # semi-transparent black
    chessWindow.blit(overlay, (0, 0))
    font_big = pygame.font.Font("ChessImages/bahnschrift.ttf", 60)
    gameover_surface = font_big.render("Game Over", True, (255, 255, 255))
    gameover_rect = gameover_surface.get_rect(center=(X//2, Y//2 - 40))
    chessWindow.blit(gameover_surface, gameover_rect)
    font = font_50
    msg_surface = font.render(result_msg, True, (255, 200, 50))
    msg_rect = msg_surface.get_rect(center=(X//2, Y//2 + 30))
    chessWindow.blit(msg_surface, msg_rect)
    pygame.display.update()
    # Wait for user to close window
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
    pygame.quit()
    exit()

# Run the game
if __name__ == '__main__':
    playercolor = choose_player_color()
    game.headers['White'] = 'Player' if playercolor == 1 else 'Computer'
    game.headers['Black'] = 'Player' if playercolor == -1 else 'Computer'

    updateWindow()

    while is_running:
        if board.outcome():
            game_over()
            break

        move_start_time = time.time()
        if (board.turn and playercolor == 1) or (not board.turn and playercolor == -1):
            playermove()
            move_time = time.time() - move_start_time
            remaining_time[board.turn ^ 1] -= move_time
            remaining_time[board.turn ^ 1] += INCREMENT
        else:
            import threading
            import time as _time
            done = [False]
            def engine_thread():
                computermove(time_left=remaining_time[board.turn])
                done[0] = True
            t = threading.Thread(target=engine_thread)
            t.start()
            comp_start = _time.time()
            clock = pygame.time.Clock()
            while not done[0]:
                now = _time.time()
                live_time = max(0, remaining_time[board.turn] - (now - comp_start))
                # Immediate time forfeit for engine
                if live_time <= 0:
                    updateWindow(live_white_time=0 if board.turn == chess.WHITE else None,
                                 live_black_time=0 if board.turn == chess.BLACK else None)
                    game_over("White lost on time" if board.turn == chess.WHITE else "Black lost on time")
                    is_running = False
                    break
                updateWindow(live_white_time=live_time if board.turn == chess.WHITE else None,
                             live_black_time=live_time if board.turn == chess.BLACK else None)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_running = False
                        break
                clock.tick(20)
            t.join()
            move_time = _time.time() - move_start_time
            remaining_time[board.turn ^ 1] -= move_time
            remaining_time[board.turn ^ 1] += INCREMENT
        # Clamp times to zero
        remaining_time[chess.WHITE] = max(0, remaining_time[chess.WHITE])
        remaining_time[chess.BLACK] = max(0, remaining_time[chess.BLACK])
        # Check for time forfeit
        if remaining_time[chess.WHITE] <= 0:
            game_over("White lost on time")
            break
        if remaining_time[chess.BLACK] <= 0:
            game_over("Black lost on time")
            break
        updateWindow()