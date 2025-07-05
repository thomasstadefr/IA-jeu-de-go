import multiprocessing
import pickle
from classes.board_class import Board
from IA.evaluate import evaluate
from functools import partial

def serialize_board(board):
    """Serialize the Board object using pickle."""
    return pickle.dumps(board)

def deserialize_board(serialized_board):
    """Deserialize the Board object using pickle."""
    return pickle.loads(serialized_board)

def parallel_pvs(args):
    alpha, beta, depth, serialized_board, color, move = args
    board = deserialize_board(serialized_board)
    board.play_move(move, color)
    score = -pvs(-beta, -alpha, depth - 1, serialize_board(board), 1 - color, parallel=False)[0]
    return score, move

def pvs(alpha, beta, depth, serialized_board, color, parallel=True):
    board = deserialize_board(serialized_board)

    moves = board.list_valid_moves()
    if depth == 0 or not moves:
        score = evaluate(board, color)
        return score, None

    best_score = -float('inf')
    best_move = None

    if depth > 1 and parallel:
        with multiprocessing.Pool() as pool:
            results = pool.map(parallel_pvs, [(alpha, beta, depth, serialized_board, 1 - color, move) for move in moves])
            for score, move in results:
                if score > best_score:
                    best_score = score
                    best_move = move
                if score > alpha:
                    alpha = score
                if alpha >= beta:
                    break
    else:
        for move in moves:
            board.play_move(move, color)
            valid_moves = board.list_valid_moves()
            print(f"[Serial] Exploring move {move} at depth {depth} with valid moves: {valid_moves}")
            score = -pvs(-beta, -alpha, depth - 1, serialize_board(board), 1 - color, parallel=False)[0]
            board.cancel_move()

            if score >= beta:
                return beta, None  # Beta cut-off

            if score > best_score:
                best_score = score
                best_move = move
                if score > alpha:
                    alpha = score  # Update alpha

    return best_score, best_move