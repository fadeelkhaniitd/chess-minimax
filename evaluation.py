import chess

def evaluation(board):
    outcome = board.outcome()
    if outcome != None:
        if outcome.result() == "1-0":
            return 20000
        elif outcome.result() == "0-1":
            return -20000

    val = 0

    pawn_position_vals = ((0,  0,  0,  0,  0,  0,  0,  0,
                            50, 50, 50, 50, 50, 50, 50, 50,
                            10, 10, 20, 30, 30, 20, 10, 10,
                             5,  5, 10, 25, 25, 10,  5,  5,
                             0,  0,  0, 20, 20,  0,  0,  0,
                             5, -5,-10,  0,  0,-10, -5,  5,
                             5, 10, 10,-20,-20, 10, 10,  5,
                             0,  0,  0,  0,  0,  0,  0,  0), (0,  0,  0,  0,  0,  0,  0,  0,
                            5, 10, 10,-20,-20, 10, 10,  5,
                            5, -5,-10,  0,  0,-10, -5,  5,
                             0,  0,  0, 20, 20,  0,  0,  0,
                             5,  5, 10, 25, 25, 10,  5,  5,
                             10, 10, 20, 30, 30, 20, 10, 10,
                             50, 50, 50, 50, 50, 50, 50, 50,
                             0,  0,  0,  0,  0,  0,  0,  0))
    knight_position_vals = ((-50,-40,-30,-30,-30,-30,-40,-50,
                            -40,-20,  0,  0,  0,  0,-20,-40,
                            -30,  0, 10, 15, 15, 10,  0,-30,
                            -30,  5, 15, 20, 20, 15,  5,-30,
                            -30,  0, 15, 20, 20, 15,  0,-30,
                            -30,  5, 10, 15, 15, 10,  5,-30,
                            -40,-20,  0,  5,  5,  0,-20,-40,
                            -50,-40,-30,-30,-30,-30,-40,-50), (-50,-40,-30,-30,-30,-30,-40,-50,
                            -40,-20,  0,  5,  5,  0,-20,-40,
                            -30,  5, 10, 15, 15, 10,  5,-30,
                            -30,  0, 15, 20, 20, 15,  0,-30,
                            -30,  5, 15, 20, 20, 15,  5,-30,
                            -30,  0, 10, 15, 15, 10,  0,-30,
                            -40,-20,  0,  0,  0,  0,-20,-40,
                            -50,-40,-30,-30,-30,-30,-40,-50))
    bishop_position_vals = ((-20,-10,-10,-10,-10,-10,-10,-20,
                              -10,  0,  0,  0,  0,  0,  0,-10,
                              -10,  0,  5, 10, 10,  5,  0,-10,
                              -10,  5,  5, 10, 10,  5,  5,-10,
                              -10,  0, 10, 10, 10, 10,  0,-10,
                              -10, 10, 10, 10, 10, 10, 10,-10,
                              -10,  5,  0,  0,  0,  0,  5,-10,
                              -20,-10,-10,-10,-10,-10,-10,-20), (-20, -10, -10, -10, -10, -10, -10, -20
                              -10,  5,  0,  0,  0,  0,  5,-10,
                              -10, 10, 10, 10, 10, 10, 10,-10,
                              -10,  0, 10, 10, 10, 10,  0,-10,
                              -10,  5,  5, 10, 10,  5,  5,-10,
                              -10,  0,  5, 10, 10,  5,  0,-10,
                              -10,  0,  0,  0,  0,  0,  0,-10,
                              -20,-10,-10,-10,-10,-10,-10,-20,))
    rook_position_vals = ((0,  0,  0,  0,  0,  0,  0,  0,
                          5, 10, 10, 10, 10, 10, 10,  5,
                         -5,  0,  0,  0,  0,  0,  0, -5,
                         -5,  0,  0,  0,  0,  0,  0, -5,
                         -5,  0,  0,  0,  0,  0,  0, -5,
                         -5,  0,  0,  0,  0,  0,  0, -5,
                         -5,  0,  0,  0,  0,  0,  0, -5,
                          0,  0,  0,  5,  5,  0,  0,  0), (0, 0, 0, 5, 5, 0, 0, 0,
                           -5, 0, 0, 0, 0, 0, 0, -5,
                           -5, 0, 0, 0, 0, 0, 0, -5,
                           -5, 0, 0, 0, 0, 0, 0, -5,
                           -5, 0, 0, 0, 0, 0, 0, -5,
                           -5, 0, 0, 0, 0, 0, 0, -5,
                           5, 10, 10, 10, 10, 10, 10, 5,
                           0, 0, 0, 0, 0, 0, 0, 0))
    queen_position_vals = ((-20,-10,-10, -5, -5,-10,-10,-20,
                            -10,  0,  0,  0,  0,  0,  0,-10,
                            -10,  0,  5,  5,  5,  5,  0,-10,
                             -5,  0,  5,  5,  5,  5,  0, -5,
                              0,  0,  5,  5,  5,  5,  0, -5,
                            -10,  5,  5,  5,  5,  5,  0,-10,
                            -10,  0,  5,  0,  0,  0,  0,-10,
                            -20,-10,-10, -5, -5,-10,-10,-20), (-20, -10, -10, -5, -5, -10, -10, -20,
                            -10, 0, 5, 0, 0, 0, 0, -10,
                            -10, 5, 5, 5, 5, 5, 0, -10,
                            0, 0, 5, 5, 5, 5, 0, -5,
                            -5, 0, 5, 5, 5, 5, 0, -5,
                            -10, 0, 5, 5, 5, 5, 0, -10,
                            -10, 0, 0, 0, 0, 0, 0, -10,
                            -20, -10, -10, -5, -5, -10, -10, -20))
    king_position_vals = ((-30,-40,-40,-50,-50,-40,-40,-30,
                            -30,-40,-40,-50,-50,-40,-40,-30,
                            -30,-40,-40,-50,-50,-40,-40,-30,
                            -30,-40,-40,-50,-50,-40,-40,-30,
                            -20,-30,-30,-40,-40,-30,-30,-20,
                            -10,-20,-20,-20,-20,-20,-20,-10,
                             20, 20,  0,  0,  0,  0, 20, 20,
                             20, 30, 10,  0,  0, 10, 30, 20), (20, 30, 10, 0, 0, 10, 30, 20,
                           20, 20, 0, 0, 0, 0, 20, 20,
                           -10, -20, -20, -20, -20, -20, -20, -10,
                           -20, -30, -30, -40, -40, -30, -30, -20,
                           -30, -40, -40, -50, -50, -40, -40, -30,
                           -30, -40, -40, -50, -50, -40, -40, -30,
                           -30, -40, -40, -50, -50, -40, -40, -30,
                           -30, -40, -40, -50, -50, -40, -40, -30))
    piece_vals = {1: 100, 2: 320, 3: 330, 4: 500, 5: 900, 6: 0}
    position_vals = {1: pawn_position_vals, 2: knight_position_vals, 3: bishop_position_vals, 4: rook_position_vals, 5: queen_position_vals, 6: king_position_vals}
    color = {chess.WHITE: 1, chess.BLACK: -1}

    bishops = dict()
    rooks = dict()
    white_bishops = 0
    black_bishops = 0
    white_king_square = None
    black_king_square = None
    white_castled = False
    black_castled = False
    white_mobility = 0
    black_mobility = 0
    white_pawn_files = set()
    black_pawn_files = set()
    white_pawnsq = []
    black_pawnsq = []

    # Endgame detection: if both sides have only king + pawns or minor pieces, or total material is low
    total_material = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece == None:
            continue
        total_material += piece_vals[piece.piece_type]

    endgame = total_material < 2400  # e.g., less than a rook and two minor pieces each

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece == None:
            continue

        val += piece_vals[piece.piece_type] * color[piece.color]
        try:
            val += position_vals[piece.piece_type][piece.color][square] * color[piece.color]
        except IndexError:
            pass

        if piece.piece_type == 3:
            bishops[square] = piece.color
            if piece.color == chess.WHITE:
                white_bishops += 1
            else:
                black_bishops += 1
        if piece.piece_type == 4:
            rooks[square % 8] = piece.color
        if piece.piece_type == 6:
            if piece.color == chess.WHITE:
                white_king_square = square
            else:
                black_king_square = square
        if piece.piece_type == 1:
            if piece.color == chess.WHITE:
                white_pawn_files.add(chess.square_file(square))
                white_pawnsq.append(square)
            else:
                black_pawn_files.add(chess.square_file(square))
                black_pawnsq.append(square)

    # Bishop pair bonus
    if white_bishops >= 2:
        val += 40
    if black_bishops >= 2:
        val -= 40

    # King safety (penalize exposed king, reward castling, adjust in endgame)
    if white_king_square is not None:
        king_file = chess.square_file(white_king_square)
        king_rank = chess.square_rank(white_king_square)
        if not endgame:
            # Penalize king in the center
            if king_file in [3, 4] and king_rank <= 1:
                val += 20
            elif king_file in [2, 5]:
                val += 10
            else:
                val -= 20
        else:
            # Reward king activity in endgame
            val += 2 * (king_rank - 1)
    if black_king_square is not None:
        king_file = chess.square_file(black_king_square)
        king_rank = chess.square_rank(black_king_square)
        if not endgame:
            if king_file in [3, 4] and king_rank >= 6:
                val -= 20
            elif king_file in [2, 5]:
                val -= 10
            else:
                val += 20
        else:
            val -= 2 * (6 - king_rank)

    # Pawn structure: isolated pawns and passed pawns
    for sq in white_pawnsq:
        file = chess.square_file(sq)
        # Isolated pawn
        if (file - 1 not in white_pawn_files) and (file + 1 not in white_pawn_files):
            val -= 15
        # Passed pawn
        passed = True
        for r in range(chess.square_rank(sq) + 1, 8):
            for f in [file - 1, file, file + 1]:
                if 0 <= f < 8:
                    opp_sq = chess.square(f, r)
                    opp_piece = board.piece_at(opp_sq)
                    if opp_piece and opp_piece.piece_type == 1 and opp_piece.color == chess.BLACK:
                        passed = False
        if passed:
            val += 20 + 5 * chess.square_rank(sq)
    for sq in black_pawnsq:
        file = chess.square_file(sq)
        if (file - 1 not in black_pawn_files) and (file + 1 not in black_pawn_files):
            val += 15
        passed = True
        for r in range(chess.square_rank(sq) - 1, -1, -1):
            for f in [file - 1, file, file + 1]:
                if 0 <= f < 8:
                    opp_sq = chess.square(f, r)
                    opp_piece = board.piece_at(opp_sq)
                    if opp_piece and opp_piece.piece_type == 1 and opp_piece.color == chess.WHITE:
                        passed = False
        if passed:
            val -= 20 + 5 * (7 - chess.square_rank(sq))

    # Mobility: reward more legal moves
    white_mobility = len(list(board.legal_moves)) if board.turn == chess.WHITE else 0
    board.push(chess.Move.null())
    black_mobility = len(list(board.legal_moves)) if board.turn == chess.BLACK else 0
    board.pop()
    val += 2 * white_mobility
    val -= 2 * black_mobility

    # Existing doubled pawns, rook on open file, etc. logic
    def pawns_in_file(file):
        white_pawns = black_pawns = 0
        for rank in range(8):
            piece = board.piece_at(((rank * 8) + file))
            if piece == None:
                continue
            if piece.piece_type == 1:
                if piece.color:
                    white_pawns += 1
                else:
                    black_pawns += 1
        return white_pawns, black_pawns

    pawns = [(pawns_in_file(x)) for x in range(8)]
    pawns.append(0)
    for file in range(8):
        white_pawns, black_pawns = pawns[file]
        if white_pawns > 1:
            val -= 10 * (white_pawns - 1)
        if black_pawns > 1:
            val += 10 * (black_pawns - 1)

        try: white_pawns_left, black_pawns_left = pawns[file - 1]
        except TypeError: white_pawns_left = black_pawns_left = 0
        try: white_pawns_right, black_pawns_right = pawns[file + 1]
        except TypeError: white_pawns_right = black_pawns_right = 0

    for square, color_ in bishops.items():
        for offset in (9, 7, -9, -7):
            try: piece_ = board.piece_at(square + offset)
            except IndexError: pass
            else:
                if piece_:
                    if piece_.piece_type == 1:
                        val -= 8 * color[color_]

    for x, color_ in rooks.items():
        a, b = pawns[x]
        if (a == 0 and color_) or (b == 0 and not color_):
            if (b == 0 and color_) or (a == 0 and not color_):
                val += 12 * color[color_]
            else:
                val += 5 * color[color_]
    if list(rooks.values()).count(chess.WHITE) > 1:
        val += 18
    if list(rooks.values()).count(chess.BLACK) > 1:
        val -= 18

    return val