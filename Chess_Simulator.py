from copy import deepcopy
import pygame
pygame.init()

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
                "p": pygame.image.load(r"ChessImages/black_pawn.png")
                }
file_convert_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g' ,'h']
color_index_conversion = {1:0, -1:1}

# indexes are as below
# 0: piece type     - string
# 1: piece color    - int (1 : White, -1 : Black, 0 : No piece)
# 2: piece number   - int
# 3: symbol letter  - string
# 4: value          - int
board = [
         [['Rook', 1, 1, "R", 5],
          ['Pawn', 1, 1, "P", 1],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          ['Pawn', -1, 1, "p", 1],
          ['Rook', -1, 1, "r", 5]],
         [['Knight', 1, 1, "N", 3],
          ['Pawn', 1, 2, "P", 1],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          ['Pawn', -1, 2, "p", 1],
          ['Knight', -1, 1, "n", 3]],
         [['Bishop', 1, 1, "B", 3],
          ['Pawn', 1, 3, "P", 1],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          ['Pawn', -1, 3, "p", 1],
          ['Bishop', -1, 1, "b", 3]],
         [['Queen', 1, 1, "Q", 9],
          ['Pawn', 1, 4, "P", 1],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          ['Pawn', -1, 4, "p", 1],
          ['Queen', -1, 1, "q", 9]],
         [['King', 1, 1, "K", 0],
          ['Pawn', 1, 5, "P", 1],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          ['Pawn', -1, 5, "p", 1],
          ['King', -1, 1, "k", 0]],
         [['Bishop', 1, 2, "B", 3],
          ['Pawn', 1, 6, "P", 1],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          ['Pawn', -1, 6, "p", 1],
          ['Bishop', -1, 2, "b", 3]],
         [['Knight', 1, 2, "N", 3],
          ['Pawn', 1, 7, "P", 1],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          ['Pawn', -1, 7, "p", 1],
          ['Knight', -1, 2, "n", 3]],
         [['Rook', 1, 2, "R", 5],
          ['Pawn', 1, 8, "P", 1],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          [None, 0, None, "", None],
          ['Pawn', -1, 8, "p", 1],
          ['Rook', -1, 2, "r", 5]]]

game = []

#first for white, second for black
kingHasMoved = [False, False]
kingHasBeenChecked = [False, False]
kingRookHasMoved = [False, False]
queenRookHasMoved = [False, False]

# get position of a specific piece
def getPos(piecetype:str, piececolor:int, piecenumber:int, board:list):
    for x in range(8):
        for y in range(8):
            if board[x][y][0] == piecetype and board[x][y][1] == piececolor and board[x][y][2] == piecenumber:
                return (file_convert_list[x] + str(y+1))


# get piece on a specific box
def getPiece(pos:str):
    posx = file_convert_list.index(pos[0]) + 1
    posy = int(pos[1])
    for x in range(8):
        for y in range(8):
            if [x, y] == [posx - 1, posy - 1]:
                return [board[x][y][0], board[x][y][1], board[x][y][2], board[x][y][3], board[x][y][4]]


def getMoves(pos:str, board:list):
    piece = getPiece(pos)[0]
    color = getPiece(pos)[1]
    file = file_convert_list.index(pos[0]) + 1
    rank = int(pos[1])

    moves_for_each_piece = {
        'Knight': ((1, 2), (2, 1), (-1, 2), (1, -2), (2, -1), (-2, 1), (-1, -2), (-2, -1)),
        'Bishop': ((1, 1), (1, -1), (-1, -1), (-1, 1)),
        'Rook': ((0, 1), (1, 0), (0, -1), (-1, 0)),
        'Queen': ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)),
        'King': ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    }
    ranges = dict(Knight=2, Bishop=8, Rook=8, Queen=8, King=2)
    possiblemoves = []

    if piece == None:
        pass
    elif piece == 'Pawn':
        if color == 1:
            if rank == 2:
                if board[file - 1][rank - 1 + (2 * color)][0] == None:
                    possiblemoves.append([file, (rank + (2 * color)), False])
        else:
            if rank == 7:
                if board[file - 1][rank - 1 + (2 * color)][0] == None:
                    possiblemoves.append([file, (rank + (2 * color)), False])

        if 0 < (rank + color) < 9:
            if board[file - 1][rank - 1 + color][0] == None:
                possiblemoves.append([file, (rank + color), False])

        if 0 < (rank + color) < 9 and 0 < (file - 1) < 9:
            if board[file - 2][rank - 1 + color][1] == (-1 * color):
                possiblemoves.append([(file - 1), (rank + color), True])

        if 0 < (rank + color) < 9 and 0 < (file + 1) < 9:
            if board[file][rank - 1 + color][1] == (-1 * color):
                possiblemoves.append([(file + 1), (rank + color), True])
    else:
        for move in moves_for_each_piece.get(piece):
            range_ = 0
            for x in range(1, ranges.get(piece)):
                if range_ == (x - 1):
                    posx, posy = file + (x * move[0]), rank + (x * move[1])
                    if 0 < posx < 9 and 0 < posy < 9:
                        if board[posx - 1][posy - 1][1] == 0:
                            possiblemoves.append([posx, posy, False])
                            range_ += 1
                        elif board[posx - 1][posy - 1][1] == (-1 * color):
                            possiblemoves.append([posx, posy, True])

    return possiblemoves


def updateWindow():
    color1 = (118,150,86)
    color2 = (238,238,210)
    for x in range(8):
        for y in range(7, -1, -1):
            image = PIECE_IMAGES.get(board[x][y][3])
            if (x + (7 - y)) % 2 == 1:
                pygame.draw.rect(chessWindow, color1, pygame.Rect((50 * x), (50 * (7 - y)), 50, 50))
            else:
                pygame.draw.rect(chessWindow, color2, pygame.Rect((50 * x), (50 * (7 - y)), 50, 50))
            if image != None:
                chessWindow.blit(image, ((50 * x), (50 * (7 - y))))

    pygame.display.update()


def inCheck(color, board1):
    global kingHasBeenChecked

    kingpos = getPos('King', color, 1, board1)
    kingpos_file = file_convert_list.index(kingpos[0]) + 1
    kingpos_rank = int(kingpos[1])

    for x in range(8):
        for y in range(8):
            if board[x][y][1] == (-1 * color):
                for move in getMoves(file_convert_list[x] + str(y + 1), board):
                    if move[:2] == [kingpos_file, kingpos_rank]:
                        if color == 1:
                            kingHasBeenChecked[0] = True
                        else:
                            kingHasBeenChecked[1] = True

    for x in range(8):
        for y in range(8):
            if board1[x][y][1] == (-1 * color):
                for move in getMoves(file_convert_list[x] + str(y + 1), board1):
                    if move[:2] == [kingpos_file, kingpos_rank]:
                        return True

    return False


def getAllMoves(color):
    all_moves = []
    for x in range(8):
        for y in range(8):
            if board[x][y][1] == color:
                for move in getMoves(file_convert_list[x] + str(y + 1), board):
                    all_moves.append([[x + 1, y + 1], move])

    return all_moves


# check for possible moves for a color when that color is in check
def movesWhenInCheck(color):
    all_moves = getAllMoves(color)
    moves_when_in_check = []
    for move in all_moves:
        boardcopy = deepcopy(board)

        boardcopy[move[1][0] - 1][move[1][1] - 1] = boardcopy[move[0][0] - 1][move[0][1] - 1]
        boardcopy[move[0][0] - 1][move[0][1] - 1] = [None, 0, None, "", None]

        if inCheck(color, boardcopy) == False:
            moves_when_in_check.append(move)

    return moves_when_in_check


# check for moves which exposes the king to check
def prohibitedMoves(color):
    all_moves = getAllMoves(color)
    prohibitied_moves = []
    for move in all_moves:
        boardcopy = deepcopy(board)

        boardcopy[move[1][0] - 1][move[1][1] - 1] = boardcopy[move[0][0] - 1][move[0][1] - 1]
        boardcopy[move[0][0] - 1][move[0][1] - 1] = [None, 0, None, "", None]

        if inCheck(color, boardcopy) == True:
            prohibitied_moves.append(move)

    return prohibitied_moves


def canCastleKingside(color):
    all_moves = getAllMoves(-1 * color)
    index = color_index_conversion.get(color)
    inlane = 0
    for move in all_moves:
        if move[:2] in [[6, (index * 7) + 1], [7, (index * 7) + 1]]:
            inlane += 1

    if kingHasMoved[index] == False and kingHasBeenChecked[index] == False and kingRookHasMoved[index] == False and board[7][index * 7][0] != None:
        if board[5][index * 7][0] == None and board[6][index * 7][0] == None:
            if inlane == 0:
                return True


def canCastleQueenside(color):
    all_moves = getAllMoves(-1 * color)
    index = color_index_conversion.get(color)
    inlane = 0
    for move in all_moves:
        if move[:2] in [[2, (index * 7) + 1], [3, (index * 7) + 1], [4, (index * 7) + 1]]:
            inlane += 1
            break

    if kingHasMoved[index] == False and kingHasBeenChecked[index] == False and queenRookHasMoved[index] == False and board[0][index * 7][0] != None:
        if board[1][index * 7][0] == None and board[2][index * 7][0] == None and board[3][index * 7][0] == None:
            if inlane == 0:
                return True


def checkmate(color, board):
    if inCheck(color, board) == True and len(movesWhenInCheck(color)) == 0:
        return True


def stalemate(color, board):
    if inCheck(color, board) == False and len(getAllMoves(color)) == 0:
        return True


def playermove():
    global playercolor, is_running
    piece_selected = False
    moved = False
    while not moved:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if piece_selected == False:
                    mousex, mousey = pygame.mouse.get_pos()
                    mousex //= 50
                    mousey //= 50
                    file = mousex + 1
                    rank = 8 - mousey

                    if board[file - 1][rank - 1][1] == playercolor:
                        piece_selected = True

                        moves = []
                        if inCheck(playercolor, board) != True:
                            moves = getMoves(file_convert_list[file - 1] + str(rank), board)
                            for x in prohibitedMoves(playercolor):
                                if x[0] == [file, rank]:
                                    moves.remove(x[1])

                            if canCastleKingside(playercolor) == True:
                                if board[file - 1][rank - 1][0] == 'King':
                                    moves.append([7, (color_index_conversion.get(playercolor) * 7) + 1, 'Castle'])

                            if canCastleQueenside(playercolor) == True:
                                if board[file - 1][rank - 1][0] == 'King':
                                    moves.append([3, (color_index_conversion.get(playercolor) * 7) + 1, 'Castle'])
                        else:
                            for x in movesWhenInCheck(playercolor):
                                if x[0] == [file, rank]:
                                    moves.append(x[1])

                        for move in moves:
                            displayx = (move[0] - 1) * 50
                            displayy = (8 - move[1]) * 50
                            width = 4
                            color1 = (130, 191, 255)
                            color2 = (255, 110, 120)
                            if move[2] != True:
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
                    mousex2, mousey2 = pygame.mouse.get_pos()
                    mousex2 //= 50
                    mousey2 //= 50
                    file2 = mousex2 + 1
                    rank2 = 8 - mousey2

                    for move in moves:
                        if move[:2] == [file2, rank2]:
                            moved = True
                            board[file2 - 1][rank2 - 1] = board[file - 1][rank - 1]
                            board[file - 1][rank - 1] = [None, 0, None, "", None]
                            game.append([f"{file_convert_list[file - 1] + str(rank)}", f"{file_convert_list[file2 - 1] + str(rank2)}"])
                            if board[file2 - 1][rank2 - 1][0] == 'King':
                                kingHasMoved[color_index_conversion.get(playercolor)] = True
                            elif board[file2 - 1][rank2 - 1][0:3:2] == ['Rook', 2]:
                                kingRookHasMoved[color_index_conversion.get(playercolor)] = True
                            elif board[file2 - 1][rank2 - 1][0:3:2] == ['Rook', 1]:
                                queenRookHasMoved[color_index_conversion.get(playercolor)] = True

                            if move[2] == 'Castle':
                                if board[file2 - 1][rank2 - 1][0] == 'King':
                                    if [file2, rank2] == [7, 1]:
                                        board[5][0] = board[7][0]
                                        board[7][0] = [None, 0, None, "", None]
                                    elif [file2, rank2] == [3, 1]:
                                        board[3][0] = board[0][0]
                                        board[0][0] = [None, 0, None, "", None]
                                    elif [file2, rank2] == [7, 8]:
                                        board[5][7] = board[7][7]
                                        board[7][7] = [None, 0, None, "", None]
                                    elif [file2, rank2] == [3, 8]:
                                        board[3][7] = board[0][7]
                                        board[0][7] = [None, 0, None, "", None]

                            if board[file2 - 1][rank2 - 1][0] == 'Pawn':
                                dict1 = {1: ['Q', 'R', 'B', 'N'], -1: ['q', 'r', 'b', 'n']}
                                if (rank2 == 8 and playercolor == 1) or (rank2 == 1 and playercolor == -1):
                                    moved = False
                                    piece_selected = None
                                    chessWindow.fill(color2)
                                    chessWindow.blit(PIECE_IMAGES.get(dict1.get(playercolor)[0]), (100, 175 - 75 * playercolor))
                                    chessWindow.blit(PIECE_IMAGES.get(dict1.get(playercolor)[1]), (150, 175 - 75 * playercolor))
                                    chessWindow.blit(PIECE_IMAGES.get(dict1.get(playercolor)[2]), (200, 175 - 75 * playercolor))
                                    chessWindow.blit(PIECE_IMAGES.get(dict1.get(playercolor)[3]), (250, 175 - 75 * playercolor))
                                    pygame.display.update()
                                else:
                                    updateWindow()
                                    playercolor *= -1
                                    break
                            else:
                                updateWindow()
                                playercolor *= -1
                                break

                elif piece_selected == None:
                    mousex3, mousey3 = pygame.mouse.get_pos()
                    mousex3 //= 50
                    mousey3 //= 50

                    color_mousey3_conversion = {1:2, -1:5}
                    if mousey3 == color_mousey3_conversion.get(playercolor):
                        if mousex3 == 2:
                            max_num = 0
                            for x in range(8):
                                for y in range(8):
                                    if board[x][y][0] == 'Queen' and board[x][y][1] == playercolor:
                                        if board[x][y][2] > max_num:
                                            max_num = board[x][y][2]

                            if playercolor == 1:
                                board[file2 - 1][rank2 - 1] = ["Queen", playercolor, max_num + 1, "Q", 9]
                            else:
                                board[file2 - 1][rank2 - 1] = ["Queen", playercolor, max_num + 1, "q", 9]

                        elif mousex3 == 3:
                            max_num = 0
                            for x in range(8):
                                for y in range(8):
                                    if board[x][y][0] == 'Rook' and board[x][y][1] == playercolor:
                                        if board[x][y][2] > max_num:
                                            max_num = board[x][y][2]

                            if playercolor == 1:
                                board[file2 - 1][rank2 - 1] = ["Rook", playercolor, max_num + 1, "R", 5]
                            else:
                                board[file2 - 1][rank2 - 1] = ["Rook", playercolor, max_num + 1, "r", 5]

                        elif mousex3 == 4:
                            max_num = 0
                            for x in range(8):
                                for y in range(8):
                                    if board[x][y][0] == 'Bishop' and board[x][y][1] == playercolor:
                                        if board[x][y][2] > max_num:
                                            max_num = board[x][y][2]

                            if playercolor == 1:
                                board[file2 - 1][rank2 - 1] = ["Bishop", playercolor, max_num + 1, "B", 3]
                            else:
                                board[file2 - 1][rank2 - 1] = ["Bishop", playercolor, max_num + 1, "b", 3]

                        elif mousex3 == 5:
                            max_num = 0
                            for x in range(8):
                                for y in range(8):
                                    if board[x][y][0] == 'Knight' and board[x][y][1] == playercolor:
                                        if board[x][y][2] > max_num:
                                            max_num = board[x][y][2]

                            if playercolor == 1:
                                board[file2 - 1][rank2 - 1] = ["Knight", playercolor, max_num + 1, "N", 3]
                            else:
                                board[file2 - 1][rank2 - 1] = ["Knight", playercolor, max_num + 1, "n", 3]

                        moved = True
                        updateWindow()
                        playercolor *= -1
                        break


chessWindow = pygame.display.set_mode((400, 400))
pygame.display.set_caption('Chess Simulator')
pygame.display.set_icon(pygame.image.load('ChessImages/chess-board.png'))
updateWindow()

playercolor = 1
is_running = True
while is_running:
    playermove()
    if is_running == False: break
    if checkmate(playercolor, board):
        print("\nWhite wins!")
        break
    elif stalemate(playercolor, board):
        print("\nStalemate")
        break

    playermove()
    if checkmate(playercolor, board):
        print("\nBlack wins!")
        break
    elif stalemate(playercolor, board):
        print("\nStalemate")
        break

end = False
while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
            break