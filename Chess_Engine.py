import chess, pygame, os, argparse
import chess.pgn
import datetime as dt
from random import choice
from math import inf
pygame.init()

parser = argparse.ArgumentParser(description="Run the Python Chess Engine")
parser.add_argument('--takeback', action='store_true', help='Enable takeback feature')
parser.add_argument('--evalbar', action='store_true', help='Show evaluation bar')
parser.add_argument('--fast', action='store_true', help='Use faster evaluation function')
args = parser.parse_args()

TAKEBACK_ENABLED = args.takeback
EVALBAR_ENABLED = args.evalbar
FAST_ENABLED = args.fast

if FAST_ENABLED:
    from evaluation import faster_evaluation as evaluation
else:
    from evaluation import evaluation

X = 550 if EVALBAR_ENABLED else 400
Y = 500 if TAKEBACK_ENABLED else 400
color1 = (118,150,86)
color2 = (238,238,210)

font_50 = pygame.font.Font("ChessImages/bahnschrift.ttf", 50)
font_30 = pygame.font.Font("ChessImages/bahnschrift.ttf", 30)
takeback = font_50.render("Takeback", True, (50, 50, 50), (235, 235, 235))
takeback_rect = takeback.get_rect()
takeback_rect.center = (200, 450)

def updateWindow():
    chessWindow.fill(color=(235, 235, 235))

    board_list_ = board.fen().split('/')
    board_list_[-1] = board_list_[-1].split()[0]
    board_list = [list(x) for x in board_list_]
    board_list_ = board_list[:]
    for i1, row in enumerate(board_list_):
        for i2, x in enumerate(row):
            try:
                x = int(x)
                del board_list[i1][i2]
                for _ in range(x):
                    board_list[i1].insert(i2, "_")
            except:
                continue
    if playercolor == 1:
        board_list.reverse()
    else:
        for i, x in enumerate(board_list):
            board_list[i] = x[::-1]
    for y, row in enumerate(board_list):
        for x in range(7, -1, -1):
            image = PIECE_IMAGES.get(row[x])
            if (x + (7 - y)) % 2 == 1:
                pygame.draw.rect(chessWindow, color1, pygame.Rect((50 * x), (50 * (7 - y)), 50, 50))
            else:
                pygame.draw.rect(chessWindow, color2, pygame.Rect((50 * x), (50 * (7 - y)), 50, 50))
            if image != None:
                chessWindow.blit(image, ((50 * x), (50 * (7 - y))))

    if TAKEBACK_ENABLED:
        chessWindow.blit(takeback, takeback_rect)
    pygame.display.update()
    if EVALBAR_ENABLED:
        show_eval_bar()

def show_eval_bar():
    val = (evaluation(board) / 100)
    val_text = font_30.render(f'{round(val, 1)}', True, (20, 20, 20), (235, 235, 235))
    pygame.draw.rect(chessWindow, (0, 0, 0), pygame.Rect(452, 199, 15, 4))
    val_rect = val_text.get_rect()
    val_rect.center = (485 + (val_rect.width // 2), 200)
    chessWindow.blit(val_text, val_rect)
    pygame.draw.rect(chessWindow, (0, 0, 0),
                     pygame.Rect(483, 201 - (val_rect.height / 2), val_rect.width + 4, val_rect.height), 1)

    if val < -10:
        val = -10
    elif val > 10:
        val = 10
    if playercolor == 1:
        pygame.draw.rect(chessWindow, (0, 0, 0), pygame.Rect(410, 0, 41, 200 - (val * 40)))
        pygame.draw.rect(chessWindow, (0, 0, 0), pygame.Rect(410, 200 - (val * 40), 40, 200 + (val * 40)), 2)
    if playercolor == -1:
        pygame.draw.rect(chessWindow, (0, 0, 0), pygame.Rect(410, 200 + (val * 40), 41, 200 - (val * 40)))
        pygame.draw.rect(chessWindow, (0, 0, 0), pygame.Rect(410, 0, 40, 200 + (val * 40)), 2)
    pygame.display.update()

def choose_player_color():
    chessWindow.fill(color=(235, 235, 235))
    white_img = PIECE_IMAGES.get('K')
    black_img = PIECE_IMAGES.get('k')
    white_rect = white_img.get_rect()
    black_rect = black_img.get_rect()
    white_rect.center = ((X-150)//2, 5*Y//8)
    black_rect.center = ((X-150)//2 + 150, 5*Y//8)
    chessWindow.blit(white_img, white_rect)
    chessWindow.blit(black_img, black_rect)
    text = font_30.render('Choose color by clicking', True, (20, 20, 20), (235, 235, 235))
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
    while not moved:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if TAKEBACK_ENABLED:
                    if y > 400:
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
                    file, rank = pygame.mouse.get_pos()
                    file //= 50
                    rank = 7 - (rank // 50)
                    if playercolor == -1:
                        file = 7 - file
                        rank = 7 - rank
                    piece = board.piece_at(chess.square(file, rank))
                    if piece != None:
                        if (piece.color == True and playercolor == 1) or (piece.color == False and playercolor == -1):
                            piece_selected = True

                            moves = []
                            for move in board.legal_moves:
                                if move.from_square == chess.square(file, rank):
                                    moves.append(move)

                            for move in moves:
                                displayx = (move.to_square % 8) * 50
                                displayy = (7 - (move.to_square // 8)) * 50
                                if playercolor == -1:
                                    square = 63 - move.to_square
                                    displayx = (square % 8) * 50
                                    displayy = (7 - (square // 8)) * 50
                                width = 4
                                color1 = (130, 191, 255)
                                color2 = (255, 110, 120)
                                if board.piece_at(chess.square(move.to_square % 8, move.to_square // 8)) == None:
                                    pygame.draw.rect(chessWindow, color1, pygame.Rect(displayx, displayy, width, 50))
                                    pygame.draw.rect(chessWindow, color1, pygame.Rect(displayx + 50 - width, displayy, width, 50))
                                    pygame.draw.rect(chessWindow, color1, pygame.Rect(displayx, displayy, 50, width))
                                    pygame.draw.rect(chessWindow, color1, pygame.Rect(displayx, displayy + 50 - width, 50, width))
                                else:
                                    pygame.draw.rect(chessWindow, color2, pygame.Rect(displayx, displayy, width, 50))
                                    pygame.draw.rect(chessWindow, color2, pygame.Rect(displayx + 50 - width, displayy, width, 50))
                                    pygame.draw.rect(chessWindow, color2, pygame.Rect(displayx, displayy, 50, width))
                                    pygame.draw.rect(chessWindow, color2, pygame.Rect(displayx, displayy + 50 - width, 50, width))
                                pygame.display.update()

                elif piece_selected == True:
                    piece_selected = False
                    updateWindow()
                    file2, rank2 = pygame.mouse.get_pos()
                    file2 //= 50
                    rank2 = 7 - (rank2 // 50)
                    if playercolor == -1:
                        rank2 = 7 - rank2
                        file2 = 7 - file2
                    for move in moves:
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
                                chessWindow.fill(color2)
                                chessWindow.blit(PIECE_IMAGES.get(dict1.get(playercolor)[0]), (100, 175 - 75 * playercolor))
                                chessWindow.blit(PIECE_IMAGES.get(dict1.get(playercolor)[1]), (150, 175 - 75 * playercolor))
                                chessWindow.blit(PIECE_IMAGES.get(dict1.get(playercolor)[2]), (200, 175 - 75 * playercolor))
                                chessWindow.blit(PIECE_IMAGES.get(dict1.get(playercolor)[3]), (250, 175 - 75 * playercolor))
                                pygame.display.update()
                                break

                elif piece_selected == None:
                    mousex3, mousey3 = pygame.mouse.get_pos()
                    mousex3 //= 50
                    mousey3 //= 50

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

def game_over():
    global game, i
    node = game
    for move in game_moves:
        node = node.add_variation(move)

    print(str(board.outcome().termination).split('.')[1])
    print(board.outcome().result())
    game.headers['Result'] = board.result()
    print(game)
    with open(f"PGNs/game{i}.pgn", "w") as file:
        file.write(f"{game}\n")

move_ordering_table = []
def computer_move(depth = 4):
    global move_ordering_table

    def minimax(board, depth, alpha, beta):
        if depth == 0:
            return evaluation(board), []

        if board.outcome() != None:
            return evaluation(board), []

        if depth == depth_: moves = move_ordering_table.copy()
        else: moves = [move for move in board.legal_moves]

        best_val = -inf if board.turn else inf
        best_moves = []
        if depth == depth_:
            all_vals = []
        for move in moves:
            board.push(move)
            curr_val, curr_moves = minimax(board, depth - 1, alpha, beta)
            board.pop()
            if depth == depth_:
                all_vals.append(curr_val)
            if (best_val < curr_val and board.turn == True) or (best_val > curr_val and board.turn == False):
                best_val = curr_val
                if board.turn: alpha = max(alpha, best_val)
                else: beta = min(beta, best_val)
                best_moves = [move]
            elif best_val == curr_val:
                best_moves.append(move)
            if beta < alpha:
                if depth == depth_:
                    min_ = min(all_vals) - 1
                    for _ in range(len(moves) - len(all_vals)):
                        all_vals.append(min_)
                break

        if depth == depth_:
            return best_val, best_moves, all_vals
        else:
            return best_val, best_moves

    all_moves = list(board.legal_moves)
    move_ordering_table = all_moves.copy()

    for depth_ in range(1, depth + 1):
        val, moves, all_vals = minimax(board, depth_, -inf, inf)
        list_ = list(zip(all_vals, move_ordering_table))
        list_.sort(key = lambda subarray: subarray[0])
        move_ordering_table.clear()
        move_ordering_table = [x[1] for x in list_]
        del list_

    move = choice(moves)
    board.push(move)
    game_moves.append(move)
    updateWindow()

chessWindow = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Chess Engine')
pygame.display.set_icon(pygame.image.load('ChessImages/chess-board.png'))
PIECE_IMAGES = {"R": pygame.image.load(r"ChessImages/white_rook.png"),
                "r": pygame.image.load(r"ChessImages/black_rook.png"),
                "N": pygame.image.load(r"ChessImages/white_knight.png"),
                "n": pygame.image.load(r"ChessImages/black_knight.png"),
                "B": pygame.image.load(r"ChessImages/white_bishop.png"),
                "b": pygame.image.load(r"ChessImages/black_bishop.png"),
                "Q": pygame.image.load(r"ChessImages/white_queen.png"),
                "q": pygame.image.load(r"ChessImages/black_queen.png"),
                "K": pygame.image.load(r"ChessImages/white_king.png"),
                "k": pygame.image.load(r"ChessImages/black_king.png"),
                "P": pygame.image.load(r"ChessImages/white_pawn.png"),
                "p": pygame.image.load(r"ChessImages/black_pawn.png"),
                "_": None
                }

playercolor = choose_player_color()

starting_fen = chess.STARTING_FEN
board = chess.Board()
board.set_fen(starting_fen)
game_moves = []

game = chess.pgn.Game()
game.headers['Event'] = 'Chess Engine'
game.headers['White'] = 'Player' if playercolor == 1 else 'Computer'
game.headers['Black'] = 'Player' if playercolor == -1 else 'Computer'
x = dt.datetime.now()
game.headers['Date'] = x.strftime("%Y.%m.%d")
i = 1
while os.path.exists(f"PGNs/game{i}.pgn"): i += 1

is_running = True
updateWindow()
if playercolor == 1:
    while is_running:
        playermove()
        if is_running == False: break
        if board.outcome() != None:
            game_over()
            break

        computer_move()
        if board.outcome() != None:
            game_over()
            break

elif playercolor == -1:
    while is_running:
        computer_move()
        if is_running == False: break
        if board.outcome() != None:
            game_over()
            break

        playermove()
        if board.outcome() != None:
            game_over()
            break

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            break
