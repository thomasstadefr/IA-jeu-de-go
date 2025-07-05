import numpy as np 
import sys, pygame
import os
import copy

chemin_dossier_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(chemin_dossier_parent)
from classes.intersection_class import Intersection
from classes.stone_class import Stone
from classes.group_class import Group

# Classe du plateau
class Board():
    def __init__(self, size: int) -> None:
        '''
        Initialise une instance de la classe Board.

        Args:
            size: Taille du plateau (9, 13 ou 19).
        '''
        self.__size = size
        self.__board = np.array([[Intersection((i,j)) for i in range(size)] for j in range(size)]) # size 9, 13 ou 19.
        self.__turn = 0 # Tour du joueur 0 (Noir).
        self.__last_moves = [] # Liste de couples (coordonnnées du coup joué, liste des chaînes capturées ou contient l'élément "passe" lorqu'un joueur passe son tour)
        self.__cancelled_moves = []
        self.__live = True # Booléen qui indique si on regarde dans les coups précédents ou si on est en direct pour savoir si on peut jouer
        self.__allow = True
        self.__black_captured = [] # Pierres noires capturées par Blanc.
        self.__white_captured = [] # Pierres blanches capturées par Noir.
        self.__groups = [] # Liste des chaînes du plateau.
        # Utile ? : self.__last_groups = [] # Liste de listes de Group (historique des chaînes créées).
        self.__passed_moves = 0 # Nombre de coups successifs passés.
        self.__nb_moves = 0 # Nombre de coups depuis le début de la partie.
        self.__mat_dead_stones = np.zeros((self.__size, self.__size))
        
    def get_board(self) -> np.array:
        '''
        Fournit le tableau de plateau

        Returns:
            Un tableaux NumPy représentant le tableau.
        '''
        return self.__board
    
    def get_turn(self):
        return self.__turn
    
    def get_size(self) -> int:
        '''
        Fournit la taille du plateau.

        Returns:
            Un entier correspondant à la taille du plateau.
        '''
        return self.__size
    
    def get_groups(self) -> int:
        '''
        Fournit la liste des chaînes.

        Returns:
            La liste correspondante.
        '''
        return self.__groups
    
    def get_live(self):
        return self.__live
    
    def get_allow(self):
        return self.__allow
    
    def get_atari_groups(self):
        l = []
        for group in self.__groups:
            if group.get_liberties == 1:
                l.append(group)
        return(l)
    
    def get_len_black_captured(self):
        return len(self.__black_captured)
    
    def get_len_white_captured(self):
        return len(self.__white_captured)
    
    def get_list_played_moves(self):
        nb_played_moves = len(self.__last_moves)
        turn = self.__turn
        l_moves = []
        for i in range(nb_played_moves):
            last_move = self.__last_moves[nb_played_moves-1-i]
            if last_move != "passe":
                l_moves.append((last_move[0], turn))
            turn = 1-turn
        l_moves.reverse()
        return l_moves

    def __str__(self) -> str:
        '''
        Affiche le plateau de manière rudimentaire dans la console. 
        Il suffira de faire print(board) où board est une instance de la
        classe Board. 'O' pour Noir et 'X' pour Blanc.
        
        Returns:
            La chaîne de caractère correspondante.
        '''
        board_str = " "
        for i in range(self.__size):
            board_str += "  "+ str(i) + " "
        board_str += "\n"
        for i in range(self.__size):
            board_str += str(i)
            for j in range(self.__size):
                if self.__board[i, j].get_stone() is None:
                    board_str += "| _ "
                elif self.__board[i, j].get_stone().get_color() == 0:
                    board_str += "| O "
                else:
                    board_str += "| X "
            board_str += "|\n"
        return board_str

    def print_all(self):
        print("\n\n", self, "\n")
        for g in self.get_groups():
            print(g)
        print("last moves : ", self.__last_moves, "\n")
        print("canceled moves :", self.__cancelled_moves, "\n")
        print("black captured :", self.__black_captured, "\n")
        print("white captured :", self.__white_captured, "\n")
        print("turn :", self.__turn, "\n")

    def set_board(self, new_board):
        self.__board = new_board
    
    def is_a_valid_move(self, coord:tuple, color:int, play:bool):
        '''
        Vérifie si un coup est possible. Va de paire avec la fonction play_move().
        Doit vérifier si les coordonnées sont dans le plateau, si la case est libre,
        éviter le ko, éviter le suicide de la pierre.

        Args:
            coord: Coordonnées du coup à jouer.
            color: Couleur du joueur (0 ou 1).
            play: Indique si le coup va être effectivement joué ou non.

        Returns:
            Un couple avec un booléen et un couple contenant la nouvelle pierre et le nouveau
            groupe si le coup est valide (renvoie ((False, (None, None)) sinon).
        '''
        # On vérifie que la pierre est dans le plateau
        if coord[0] >= self.__size or coord[1] >= self.__size or coord[0] < 0 or coord[1] < 0:
            #print("Les coordonnées sont en dehors du plateau.")
            return (False, (None, None))
        
        # On vérifie que l'intersection n'est pas occupée.
        if self.__board[coord].get_stone() is not None:
            #print("L'emplacement est déjà occupé.")
            return (False, (None, None))
        
        # On vérifie que la règle interdisant les répétitions est respectée
        if len(self.__last_moves)>=2 and self.__last_moves[-2] != "passe" and self.__last_moves[-2][0] == coord:
            return (False, (None, None))
        
        # On met à jour les chaînes s'il y a connexion lorsque la pierre est placée.
        group_list = [] # Liste des groupes déjà visités.
        for delta in [[-1,0], [0,-1], [1,0], [0,1]]:
            pos = np.array(coord) + delta # On vérifie les positions autour de la pierre.
            # On s'assure que la pierre est dans le plateau.
            if pos[0] < self.__size and pos[1] < self.__size and pos[0] >= 0 and pos[1] >= 0:
                # On vérifie que les pierres autour sont de la même couleur que la pierre placée.
                if self.__board[tuple(pos)].get_stone() is not None and self.__board[tuple(pos)].get_stone().get_color() == color:
                    # On s'assure que le groupe étudié n'est pas déjà dans la liste des groupes déjà vus.
                    if self.__board[tuple(pos)].get_stone().get_group() not in group_list:
                        group_list.append(self.__board[tuple(pos)].get_stone().get_group())

        # On crée un nouveau groupe correspondant à la fusion des groupes adjacents
        new_stone = Stone(color, coord)
        new_group = Group(color, [new_stone])
        for group in group_list:
            new_group = Group.merge(new_group, group) # Fusion des groupes.

        self.__board[coord].set_stone(new_stone)
        new_group.update_liberties_new_stone(self) # On met à jour avant de vérifier le suicide.

        if new_group.get_liberties() == 0:
            self.__board[coord].set_stone(None)
            self.update_board()
            return (False, (None, None))
        else:
            for group in group_list:            
                if group in self.__groups:
                    self.__groups.remove(group) # On retire les anciens groupes car ils sont remplacés par le nouveau groupe qui est bien vivant
            self.__board[coord].set_stone(None)
            if play == 0: # Si on ne va pas jouer le coup, on rajoute les groupes supprimés précédemment en splitant.
                for old_group in new_group.split(new_stone, self):
                    self.add_group(old_group)
            self.update_board()
            new_group_list = self.__groups

            if new_group not in new_group_list and play == 1:
                new_group_list.append(new_group)
            return (True, (new_stone, new_group_list))
        


    def play_move(self, coord: tuple, color: int) -> None:
        '''
        Joue un coup. Doit s'assurer que le coup est valide, puis
        mettre à jour les degrés de liberté, les chaînes, changer 
        self.__turn, etc.

        Args:
            coord: Coordonnées de la pierre à jouer
            color: Couleur de la pierre à jouer
        '''
        if self.__allow: # Si on est autorisé à jouer, soit on est en direct, soit on est dans le passé et on revient vers le direct, soit on est dans le passé et on débute une nouvelle variante
            if not(self.__live): # Cas où on est dans le passé mais on a le droit de débuter une nouvelle variante
                while self.__cancelled_moves:
                    self.__cancelled_moves.pop()
                self.__live = True

            res = self.is_a_valid_move(coord, color, True)
            if res[0]:
                new_stone = res[1][0] # On récupère la pierre jouée
                new_group_list = res[1][1] # On récupère le nouveau groupe
                '''if new_stone.get_color() == 0 and new_stone in self.__black_captured:
                    self.__black_captured.remove(new_stone)
                elif new_stone.get_color() == 1 and new_stone in self.__white_captured:
                    self.__white_captured.remove(new_stone)'''
                self.set_groups(new_group_list)
                self.__board[coord].set_stone(new_stone) # On la place sur le plateau
                self.__turn = 1 - self.__turn # Changer le tour
                self.__nb_moves += 1 # On augmente le nombre de tour
                self.__passed_moves = 0

                captures = self.update_board() # On met à jour tout les degrés de libertés des chaînes et des pierres du plateau.
                self.__last_moves.append((coord, captures)) 
        self.print_all()
                
    def play_list_moves(self, list_moves) -> None:
        for (coord, color) in list_moves:
            self.play_move(coord, color)

    def get_last_moves(self):
        return self.__last_moves

    def update_board(self):
        '''
        Met à jour les degrés de liberté de chaque chaîne et chaque pierre.
        Supprime les chaînes qui n'auraient plus de degrés de libertés. 
        Stocke les groupes capturés pour les enragistrer dans la liste des captures pour last_move

        Returns:
            Renvoie la liste des groupes capturées.
        '''

        captures = []



        for group in self.__groups:
            group.update_liberties(self) # Met à jour les degrés de liberté du groupe
            
            # Le groupe est capturé
            if group.get_liberties() == 0: 
                captures.append(group)
                for stone in group.get_stones(): # On supprime les pierres du groupe
                    stone.set_group(group) # On rappelle à la pierre à quel groupe elle appartient.
                    if stone.get_color() == 0:
                        self.__black_captured.append(stone) # Ajout aux pierres capturées par Blanc
                    else:
                        self.__white_captured.append(stone) # Ajout aux pierres capturées par Noir
                    self.__board[(stone.get_coord())].set_stone(None) # On retire la pierre du plateau
                self.__groups.remove(group) # On retire le groupe de la liste des groupes du plateau
                self.update_board() # On rappelle la même fonction pour mettre à jour les degrés de liberté avec le groupe en moins.
            
            # Le groupe n'est pas capturé
            else:
                for stone in group.get_stones():
                    stone.set_group(group)
                    stone.update_liberties(self) # On met à jour les degrés de liberté de chaque pierre.
            group.sort_stones() # Trier les groupes permet de détecter les groupes identiques.

        return captures

    def pass_move(self) -> None:
        self.__turn = 1 - self.__turn
        self.__passed_moves += 1
        self.__last_moves.append("passe")
        self.print_all()
    
    def set_groups(self, group_list):
        self.__groups = group_list
        return
    
    def add_group(self, g):
        self.__groups.append(g)

    def remove_group(self, g):
        self.__groups.remove(g)
           
    def show_last_move(self):
        last_moves = self.__last_moves
        if last_moves:
            self.__turn = 1-self.__turn #Changer le tour
            if last_moves[-1] == "passe":
                self.__passed_moves = self.__passed_moves - 1   #On gère le cas où le coup précédant était de passer
                last_moves.pop()
                self.__cancelled_moves.append("passe")
            else:
                coord, captured_groups = last_moves.pop()

                #Retirer la pierre qu'on souhaite annuler de la chaîne où elle est enregistrée
                s = self.__board[coord].get_stone()
                self.__board[coord].set_stone(None)
                g = s.get_group()
                self.remove_group(g)
                new_groups = s.get_group().split(s, self)
                for ng in new_groups:
                    for ns in ng.get_stones():
                        ns.set_group(ng)
                    self.add_group(ng)              
            
                #Rétablir les pierres capturées et les enlever de la liste des pierres capturées
                for group in captured_groups:
                    self.__groups.append(group)
                    for stone in group.get_stones():
                        stone_coord = stone.get_coord()
                        self.__board[stone_coord].set_stone(stone)
                        stone.set_group(group)
                        stone.update_liberties(self)
                        color = stone.get_color()
                        if color == 0:
                            self.__black_captured.remove(stone)
                        else:
                            self.__white_captured.remove(stone)
                    group.update_liberties(self)
                self.update_board()
                self.__cancelled_moves.append(coord)
            self.__allow = False
            self.__live = False
        self.print_all()

    def show_next_move(self):
        cancelled_moves = self.__cancelled_moves
        if cancelled_moves:
            coord = cancelled_moves.pop()
            if coord == "passe":
                self.pass_move()
            else:
                self.__allow = True
                self.__live = True
                self.play_move(coord, self.__turn)
                if self.__cancelled_moves:
                    self.__allow = False
                    self.__live = False
        self.print_all()

    def show_start_pos(self):
        while self.__last_moves:
            self.show_last_move()

    def show_live_pos(self):
        while self.__cancelled_moves:
            self.show_next_move()

    def cancel_move(self):
        self.show_last_move()
        self.__allow = True

    def restore_move(self):
        self.show_next_move()
        self.__allow = True

    def get_neighbours(self, coord:tuple):
        '''
        Renvoie un tuple (neigh, coord) où neigh est de type Stone et coord
        le tuple de ses coordonnées.
        '''
        neigh = []
        for delta in [(-1,0), (0,-1), (0,1), (1,0)]:
            new_pos = np.array(coord) + np.array(delta)
            if new_pos[0] < self.__size and new_pos[1] < self.__size and new_pos[0] >= 0 and new_pos[1] >= 0:
                neigh.append((self.__board[tuple(new_pos)].get_stone(), tuple(new_pos)))
        return(neigh)

    def list_valid_moves(self): 
        color = self.__turn
        list = []
        for i in range(0, self.__size) : 
            for j in range(0, self.__size) : 
                if self.is_a_valid_move((i,j), color, False)[0] : 
                    list.append((i,j))
        return list
    
    
    def copy_board(self):
        new_board = Board(self.__size)   

        # Copie des pierres sur le plateau.
        for i in range(self.__size):
            for j in range(self.__size):
                if not (self.__board[i,j].get_stone() is None):
                    stone = self.__board[i,j].get_stone()
                    new_stone = Stone(stone.get_color(), stone.get_coord())
                    new_board.get_board()[i,j].set_stone(new_stone)

        # Copies des groupes.
        group_list = []
        for group in self.__groups:
            new_group = Group(group.get_color(), [])
            for stone in group.get_stones():
                new_board.get_board()[stone.get_coord()].get_stone().set_group(new_group)
                new_group.add_stone(new_board.get_board()[stone.get_coord()].get_stone())
            group_list.append(new_group)
        new_board.set_groups(group_list)

        new_board.update_board()

        return(new_board)


    def calculate_territories(self):
        '''
        Calcule les territoires pour chaque couleur après avoir supprimé les pierres supposées comme mortes.
        On réalisera pour cela un parcours en profondeur.
        '''
        def aux(current_pos, color, nb_territories):
            if current_pos in visited or current_pos in global_visited:
                return (0, color, [])

            if self.__board[current_pos].get_stone() is not None:
                if self.__board[current_pos].get_stone().get_color() != color and color != None:
                    color = -1 # On a croisé deux couleurs lors du parcours, on ne donne pas de couleur au territoire.
                elif color != -1:
                    color = self.__board[current_pos].get_stone().get_color()
                return (0, color, [])
            
            (y,x) = current_pos
            visited.append(current_pos)
            nb_territories += 1

            t_top = 0
            t_bottom = 0
            t_left = 0
            t_right = 0

            if y>0:
                if self.get_board()[(y-1, x)].get_stone() is not None:
                    if self.get_board()[(y-1, x)].get_stone().get_color() != color and color != None:
                        color = -1 # On a croisé deux couleurs lors du parcours, on ne donne pas de couleur au territoire.
                        has_a_color[0] = False
                    elif color != -1:
                        color = self.get_board()[(y-1, x)].get_stone().get_color()
                else:
                    (a,b,_) = aux((y-1, x), color, nb_territories)
                    t_top = a
                    if color is None:
                        color = b

            if y<self.__size-1:
                if self.get_board()[(y+1, x)].get_stone() is not None:
                    if self.get_board()[(y+1, x)].get_stone().get_color() != color and color != None:
                        color = -1 # On a croisé deux couleurs lors du parcours, on ne donne pas de couleur au territoire.
                        has_a_color[0] = False
                    elif color != -1:
                        color = self.get_board()[(y+1, x)].get_stone().get_color()
                else:
                    (a,b,_) = aux((y+1, x), color, nb_territories)
                    t_bottom = a
                    if color is None:
                        color = b

            if x>0:
                if self.get_board()[(y, x-1)].get_stone() is not None:
                    if self.get_board()[(y, x-1)].get_stone().get_color() != color and color != None:
                        color = -1 # On a croisé deux couleurs lors du parcours, on ne donne pas de couleur au territoire.
                        has_a_color[0] = False
                    elif color != -1:
                        color = aux((y, x-1), color, nb_territories)[1]
                else:
                    (a,b,_) = aux((y, x-1), color, nb_territories)
                    t_left = a
                    if color is None:
                        color = b

            if x<self.__size-1:
                if self.get_board()[(y, x+1)].get_stone() is not None:
                    if self.get_board()[(y, x+1)].get_stone().get_color() != color and color != None:
                        color = -1 # On a croisé deux couleurs lors du parcours, on ne donne pas de couleur au territoire.
                        has_a_color[0] = False
                    elif color != -1:
                        color = self.get_board()[(y, x+1)].get_stone().get_color()
                else:
                    (a,b,_) = aux((y, x+1), color, nb_territories)
                    t_right = a
                    if color is None:
                        color = b
            
            return (t_top + t_bottom + t_left + t_right, color, visited)
        
        black_territories_list = []
        white_territories_list = []
        global_visited = []
        for coord in self.get_empty_inter():
            visited = []
            has_a_color = [True] # On doit mettre une liste ici, car un simple bool est non mutable.
            if coord not in global_visited:
                (_, color, l) = aux(coord, None, 0)
                if color == 0 and has_a_color[0]:
                    black_territories_list.append(l)
                if color == 1 and has_a_color[0]:
                    white_territories_list.append(l)
                for coord in visited:
                    global_visited.append(coord)
        
        black_territories = 0
        white_territories = 0
        for terr in black_territories_list:
            black_territories += len(terr)
        for terr in white_territories_list:
            white_territories += len(terr)        
        return((black_territories, black_territories_list), (white_territories,white_territories_list))

    def end_game(self):
        '''
        Met fin à la partie en retirant les pierres mortes, ajoutant leur nombre au score de chaque joueur
        et calculant le territoire de chaque joueur.
        '''
        self.remove_dead_groups()
        (black, white) = self.calculate_territories()
        black_score = black[0] + len(self.__white_captured)
        white_score = white[0] + len(self.__black_captured)

        white_score += 7.5 # Ajout du komi (règles françaises)

        if white_score > black_score:
            print("VICTOIRE DE BLANC :")
            print("SCORE DE NOIR :", black_score)
            print("SCORE DE BLANC :", white_score)
        elif white_score < black_score:
            print("VICTOIRE DE NOIR")
            print("SCORE DE NOIR :", black_score)
            print("SCORE DE BLANC :", white_score)
        else:
            print("EGALITE")
            print("SCORE DE NOIR :", black_score)
            print("SCORE DE BLANC :", white_score)
        return(black_score, white_score)

    def get_empty_inter(self):
        '''
        Renvoie la liste des intersections vides du plateau.
        '''
        l = []
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__board[(i,j)].get_stone() is None:
                    l.append((i,j))
        return(l)


    def remove_dead_groups(self):
        '''
        Supprime toute les chaîne mortes du plateau et renvoie leur nombre pour Noir et Blanc.
        '''
        dead_stones = (0,0) # (Pierres noires mortes, Pierres blanches mortes)
        for g in self.__groups:
            if g.is_presumed_dead(self):
                for stone in g.get_stones():
                    self.__board[stone.get_coord()].set_stone(None)
                self.__groups.remove(g)
                self.update_board()
        return dead_stones

    def set_dead_stone(self, coord, v):
        self.__mat_dead_stones[coord] = v



    def list_presumed_dead_stones(self):
        '''
        Renvoie une matrice avec des 1 là où les pierres noires sont mortes, -1 où des pierres blanches sont mortes
        et 0 ailleurs.
        '''
        mat = self.__mat_dead_stones
        for g in self.__groups:
            if g.is_presumed_dead(self):
                for stone in g.get_stones():
                    if stone.get_color() == 0:
                        mat[stone.get_coord()] = 1
                    if stone.get_color() == 1:
                        mat[stone.get_coord()] = -1
        return(mat)
    
    def hash(self):
        # Générer une représentation unique du plateau
        board_state = tuple(tuple(intersection.get_stone().get_color() if intersection.get_stone() else -1
                                  for intersection in row) for row in self.__board)
        return hash(board_state)


    # Appels       
    #Appels aux différentes fonctions pour calculer le score final
    #dead_stones = detect_dead_stones()
    #territoires  = determine_territoires()
    #scores = assign_territoires(territoires, dead_stones)
    #return scores 