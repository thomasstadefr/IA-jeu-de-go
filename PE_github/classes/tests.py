import sys
import os
import cProfile

chemin_dossier_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(chemin_dossier_parent)

from classes.board_class import Board
from IA.evaluate import evaluate
from IA.search_tree import pvs, serialize_board

if __name__ == "__main__":
    board = Board(9)
    # Jouer quelques mouvements pour établir une position de départ
    board.play_move((4, 4), 1)
    board.pass_move()
    board.play_move((4, 6), 1)
    board.pass_move()
    board.play_move((5, 5), 1)
    board.play_move((4, 5), 0)

    print(board)

    alpha = -float('inf')
    beta = float('inf')
    profondeur_max = 1
    color = 0

    # Profiling
    profiler = cProfile.Profile()
    profiler.enable()

    meilleur_score, meilleur_move = pvs(alpha, beta, profondeur_max, serialize_board(board), color, parallel=True)

    profiler.disable()
    profiler.print_stats(sort='cumtime')

    print(f"Meilleur score: {meilleur_score}, Meilleur mouvement: {meilleur_move}")