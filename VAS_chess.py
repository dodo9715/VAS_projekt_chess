import chess
import chess.svg
import chess.engine

def evaluate_board(board):
    evaluation = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue
        value = {
            chess.PAWN: 10,
            chess.KNIGHT: 30,
            chess.BISHOP: 30,
            chess.ROOK: 50,
            chess.QUEEN: 90,
            chess.KING: 900
        }[piece.piece_type]

        value = value if piece.color == chess.WHITE else -value
        evaluation += value

    evaluation += 0.1 * len(list(board.legal_moves))

    return evaluation


def minimax(board, depth, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move(board, depth):
    legal_moves = list(board.legal_moves)
    best_move = None
    best_eval = float('-inf')

    for move in legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, False)
        board.pop()

        print(f"Potez: {move.uci()}, Evaluacija: {eval}")

        if eval > best_eval:
            best_eval = eval
            best_move = move
            
        print(f"Najbolji potez: {best_move.uci()}, Najbolja evaluacija: {best_eval}")
    
    return best_move

def is_legal_move(board, move):
    legal_moves = list(board.legal_moves)
    return move in legal_moves

def main():
    board = chess.Board()
    depth = 4  # Moguća je promjena dubine, veći broj označava dulje vrijeme pokreta

    while not board.is_game_over():
        print(board)
        if board.turn == chess.WHITE:
            legal_moves = list(board.legal_moves)
            moves_list = " ".join(move.uci() for move in legal_moves)
            print("Legalni potezi:", moves_list)
            user_move = input("Upišite svoj potez (iz liste mogucih): ")
            if is_legal_move(board, chess.Move.from_uci(user_move)):
                board.push(chess.Move.from_uci(user_move))
            else:
                print("Nedozvoljen potez. Pokušajte ponovo.")
        else:
            print("AI razmišlja...")
            best_move = find_best_move(board, depth)
            print("AI potez:", best_move)
            board.push(best_move)

    print("Game Over!")
    print("Rezultat: {}".format(board.result()))

if __name__ == "__main__":
    main()
