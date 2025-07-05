import sys
import os
import numpy as np 
from numpy.random import normal

chemin_dossier_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(chemin_dossier_parent)
from classes.board_class import Board
from IA.pointDict import PointDict



def nb_stone_on_edge(board, color=1):
    k = 0
    for i in range(1, board.get_size()-1):
        if board.get_board()[i,0].get_stone() is not None:
            if board.get_board()[i,0].get_stone().get_color() == color:
                k += 1
        if board.get_board()[i,board.get_size()-1].get_stone() is not None:
            if board.get_board()[i,board.get_size()-1].get_stone().get_color() == color:
                k += 1
        
    for i in range(board.get_size()):
        if board.get_board()[0,i].get_stone() is not None:
            if board.get_board()[0,i].get_stone().get_color() == color:
                k += 1
        if board.get_board()[0,board.get_size()-1].get_stone() is not None:
            if board.get_board()[0,board.get_size()-1].get_stone().get_color() == color:
                k += 1
    return(k)

def get_num_endangered_groups(board: Board, color: int):
    '''
    Renvoie le nombre de groupe en atari pour le joueur et son
    adversaire.
    '''
    num_endangered_self = 0
    num_endangered_opponent = 0
    for group in board.get_atari_groups():
        if group.color == color:
            num_endangered_self += 1
        else:
            num_endangered_opponent += 1
    return num_endangered_self, num_endangered_opponent

def get_num_groups_with_k_liberties(board: Board, color: int, k: int) -> tuple:
    '''
    Renvoie le nombre de groupe avec exactement k libertés pour le joueur
    et son adversaire.
    '''
    num_groups_self = 0
    num_groups_opponent = 0
    for group in board.get_groups():
        if group.get_color() == color and group.get_liberties() == k:
            num_groups_self += 1
        if group.get_color() == 1 - color and group.get_liberties() == k:
            num_groups_opponent += 1
    return num_groups_self, num_groups_opponent

def get_colored_groups(board: 'Board', color: int) -> list:
    '''
    Renvoie la liste des groupes de la couleur color.
    '''
    l = []
    for group in board.get_groups():
        if group.get_color() == color:
            l.append(group)
    return(l)

def init_point_dict(board: 'Board'):
    '''
    On initialise libertydict grâce à cette fonction. libertydict sert à répertorier les intersections adjacentes aux pierres d'une couleur
    '''
    dic = PointDict()
    size = board.get_size()
    for i in range(size):
        for j in range(size):
            dic.set_groups(0, (i, j), [])
            dic.set_groups(1, (i, j), [])
            if i>0:
                stone_up = board.get_board()[i-1, j].get_stone()
                if stone_up is not None:
                    dic.add_group(stone_up.get_color(), (i, j), stone_up.get_group())
            if i<size-1:
                stone_down = board.get_board()[i+1, j].get_stone()
                if stone_down is not None:
                    dic.add_group(stone_down.get_color(), (i, j), stone_down.get_group())
            if j>0:
                stone_left = board.get_board()[i, j-1].get_stone()
                if stone_left is not None:
                    dic.add_group(stone_left.get_color(), (i, j), stone_left.get_group())
            if j<size-1:
                stone_right = board.get_board()[i, j+1].get_stone()
                if stone_right is not None:
                    dic.add_group(stone_right.get_color(), (i, j), stone_right.get_group())
    return(dic)

def get_liberties_coord(board: 'Board', group) -> list:
    '''
    Renvoie la liste des coordonnées correspondant aux positions libres
    autour du groupe
    '''
    inter_list = [] # Liste des coordonnées des intersections vides adjacentes à la chaîne.
    for stone in group.get_stones():
        for delta in [[-1,0], [0,-1], [1,0], [0,1]]:
            pos = np.array(stone.get_coord()) + delta
            # La dernière condition permet de ne pas compter deux fois les mêmes intersections.
            if pos[0] < board.get_size() and pos[1] < board.get_size() and pos[0] >= 0 and pos[1] >= 0 and not tuple(pos) in inter_list: 
                if board.get_board()[tuple(pos)].get_stone() is None:
                    inter_list.append(tuple(pos))

    return(inter_list)

def get_liberties(board, color):
    '''
    Renvoie deux listes de coordonnées correspondants aux
    position libres autour des groupes pour chaque couleur.
    '''
    liberties_self = set()
    liberties_opponent = set()
    for group in get_colored_groups(board, color):
        liberties_self = set(list(liberties_self) + get_liberties_coord(board, group))
    for group in get_colored_groups(board, 1 - color):
        liberties_opponent = set(list(liberties_opponent) + get_liberties_coord(board, group))
    return liberties_self, liberties_opponent

def is_dangerous_liberty(board: Board, point: tuple, color: int) -> bool:
    '''
    Apporte une information disant si les groupes sont au nombre de deux, et si
    chacun de ces deux groupes a seulement deux degrés de liberté (dans ce cas
    on a un danger qui nous pousse à protéger les deux groupes immédiatemment
    pour éviter de perdre l'un des deux).
    '''
    libertydict = init_point_dict(board)
    self_groups = libertydict.get_groups(color, point)
    return len(self_groups) == 2 and self_groups[0].get_liberties() == 2 and self_groups[1].get_liberties() == 2


def counter_move(board: Board):
    '''
    Compte le nombre de pierres sur le plateau
    '''
    counter = 0
    for i in range(board.get_size()):
        for j in range(board.get_size()):
            if board.get_board()[(i,j)].get_stone() is not None:
                counter += 1
    return counter


def get_neighbors(board, position, distance=2):
    """
    Renvoie les cases autour d'une position donnée à une certaine distance sur le plateau.
    """
    x, y = position
    neighbors = []
    directions = [(dx, dy) for dx in range(-distance, distance + 1) for dy in range(-distance, distance + 1)
                  if abs(dx) == distance or abs(dy) == distance]

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < board.get_size() and 0 <= new_y < board.get_size() and board.get_board()[new_x, new_y].get_stone() is not None:
            neighbors.append((new_x, new_y))

    return set(neighbors)


def get_largest_group(board):
    groups = board.get_groups()
    max_l = 0
    max_g = None
    for group in groups:
        if group.get_color() == 1:
            if len(group.get_stones()) > max_l:
                max_l = len(group.get_stones())
                max_g = group
    return max_g

def count_empty_neighbors_in_biggest_chain(board, distance=2):
    """
    Renvoie le nombre de cases vides autour d'une chaîne de coordonnées à une certaine distance sur le plateau.
    """
    group = get_largest_group(board)
    empty_neighbors = set()
    
    for stone in group.get_stones():
        neighbors = get_neighbors(board, stone.get_coord(), distance)
        for neighbor in neighbors:
            x, y = neighbor
            if board.get_board()[x,y].get_stone() is None:
                empty_neighbors.add(neighbor)
    
    return len(empty_neighbors)



def evaluate(board: 'Board', color: int):
    '''
    Renvoie le score pour un plateau et une couleur donnée.
    '''
    score_win = 1000 - counter_move(board)

    opponent = 1 - color

    nb_edge = nb_stone_on_edge(board)
    edge_penalty = nb_edge * 10

    neigh_bonus = -count_empty_neighbors_in_biggest_chain(board) # Encourages to extend the biggest chain in empty spaces

    # Initial score
    score = score_win + neigh_bonus + edge_penalty

    # Score for endangered groups
    num_endangered_self, num_endangered_opponent = get_num_endangered_groups(board, color)
    if num_endangered_opponent > 0:
        score -= 10
    elif num_endangered_self > 1:
        score += 10

    # Score for dangerous liberties
    liberties_self, liberties_opponent = get_liberties(board, color)
    for liberty in liberties_opponent:
        if is_dangerous_liberty(board, liberty, opponent):
            score = -score / 2 

    for liberty in liberties_self:
        if is_dangerous_liberty(board, liberty, color):
            libertydict = init_point_dict(board)
            self_groups = libertydict.get_groups(color, liberty)
            liberties = get_liberties_coord(board, self_groups[0]) + get_liberties_coord(board, self_groups[0])
            able_to_save = False
            for lbt in liberties:
                if len(libertydict.get_groups(opponent, lbt)) > 0:
                    able_to_save = True
                    break
            if not able_to_save:
                score = score / 2 

    # Score for groups
    num_groups_2lbt_self, num_groups_2lbt_oppo = get_num_groups_with_k_liberties(board, color, 2)
    score_groups = num_groups_2lbt_oppo - num_groups_2lbt_self

    # Score for liberties
    num_shared_liberties_self = 0
    num_shared_liberties_oppo = 0
    libertydict = init_point_dict(board)
    for liberty in liberties_self:
        num_shared_liberties_self += len(libertydict.get_groups(color, liberty)) - 1
    for liberty in liberties_opponent:
        num_shared_liberties_oppo += len(libertydict.get_groups(opponent, liberty)) - 1
    score_liberties = num_shared_liberties_oppo - num_shared_liberties_self

    score += score_groups + score_liberties

    return score