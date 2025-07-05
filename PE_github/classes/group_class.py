import numpy as np

class Group():
    def __init__(self, color: int, stones: list) -> None:
        '''
        Initialise une instance de la classe Groupe.

        Args:
            color: Couleur du groupe (0 ou 1).
            stones: Liste des pierres de la chaîne.
            board: Plateau
        
        Returns:
            Instance de la classe Group.
        '''
        self.__stones = stones
        self.__color = color # 0 pour Noir, 1 pour Blanc.
        self.__atari = False # Est en atari.
        self.__liberties = 10 # Nombre de degrés de liberté.

    def get_color(self) -> int:
        '''
        Renvoie la couleur de la chaîne.

        Returns:
            0 pour la couleur Noire, 1 pour la couleur Blanche.
        '''
        return(self.__color)
    
    def get_stones(self) -> list:
        '''
        Renvoie les liste des pierres de la chaîne.

        Returns:
            La liste des pierres.
        '''
        return(self.__stones)
    
    def get_atari(self) -> bool:
        '''
        Indique si la chaîne est en atari.

        Returns:
            True si la pierre est en atari, False sinon.
        '''
        return(self.__atari)
    
    def get_liberties(self) -> int:
        '''
        Donne le nombre de degrés de liberté de la chaîne

        Returns:
            Un entier indiquant le nombre de degrés de liberté.
        '''
        return(self.__liberties)
    
    def set_liberties(self, lib) -> None:
        self.__liberties == lib
    
    def get_length(self):
        return len(self.__stones)
    
    def set_stones(self, stones):
        self.__stones = stones
        return 
    
    def add_stone(self, stone) -> None:
        '''
        Ajoute une pierre à la chaîne.

        Args:
            stone: Pierre à ajouter à la chaîne. 
        '''
        self.__stones.append(stone)
        return
    
    def remove_stone(self, stone):
        '''
        Supprime une pierre de la chaîne
        '''
        self.__stones.remove(stone)
    
    def update_liberties(self, board) -> None:
        '''
        Met à jour les degrés de liberté de la chaîne.

        Args:
            board: Le plateau
        '''
        liberties = 0
        inter_list = [] # Liste des coordonnées des intersections vides adjacentes à la chaîne.
        for stone in self.__stones:
            for delta in [[-1,0], [0,-1], [1,0], [0,1]]:
                pos = np.array(stone.get_coord()) + delta
                # La dernière condition permet de ne pas compter deux fois les mêmes intersections.
                if pos[0] < board.get_size() and pos[1] < board.get_size() and pos[0] >= 0 and pos[1] >= 0 and not tuple(pos) in inter_list: 
                    if board.get_board()[tuple(pos)].get_stone() is None:
                        liberties += 1
                        inter_list.append(tuple(pos))
        self.__liberties = liberties



    def update_liberties_new_stone(self, board) -> None:
        '''
        Cette fonction sert à calculer les libertés d'un groupe après avoir joué un coup. 
        En particulier lorsque l'on élimine une chaîne adverse qui privait de libertés.
        '''

        liberties = 0
        inter_list = [] # Liste des coordonnées des intersections vides adjacentes à la chaîne.
        for stone in self.__stones:
            for delta in [[-1,0], [0,-1], [1,0], [0,1]]:
                pos = np.array(stone.get_coord()) + delta
                # La dernière condition permet de ne pas compter deux fois les mêmes intersections.
                if pos[0] < board.get_size() and pos[1] < board.get_size() and pos[0] >= 0 and pos[1] >= 0 and not tuple(pos) in inter_list: 
                    if board.get_board()[tuple(pos)].get_stone() is None: 
                        liberties += 1
                        inter_list.append(tuple(pos))
                    elif board.get_board()[tuple(pos)].get_stone().get_color() != self.get_color(): 
                        g = board.get_board()[tuple(pos)].get_stone().get_group()
                        lib_g = g.get_liberties()
                        g.update_liberties(board)
                        if g.get_liberties() == 0:
                            liberties += 1
                            inter_list.append(tuple(pos))
                        g.set_liberties(lib_g)
        self.__liberties = liberties

    def __str__(self) -> str:
        '''
        Affiche la chaîne.

        Returns:
            La chaîne de caractère correspondante.
        '''
        board_str = "Chaîne: \n"
        for stone in self.__stones:
            board_str += "\t" + str(stone) + "\n"
        return board_str
        
    @staticmethod
    def merge(group1 : 'Group', group2 : 'Group') -> 'Group':
        new_group = Group(group1.get_color(), [])
        for stone in group1.get_stones():
            if not(stone in new_group.get_stones()):
                new_group.add_stone(stone)
            stone.set_group(new_group)
        for stone in group2.get_stones():
            if not(stone in new_group.get_stones()):
                new_group.add_stone(stone)
            stone.set_group(new_group)
        return new_group
    
    @staticmethod
    def dfs_group(s, board):
        '''
        Récupère le nouveau groupe auquel appartient la pierre s grâce à un parcours en profondeur
        '''
        c = s.get_color()
        g = Group(c, [])
        m = board.get_size()-1
        def aux(current_coord):
            current_s = board.get_board()[current_coord].get_stone()
            if current_s and current_s.get_color()==c and not(current_s in g.get_stones()):
                g.add_stone(current_s)
                g.sort_stones()
                y = current_coord[0]
                x = current_coord[1]
                if x>0:
                    aux((y, x-1))
                if x<m:
                    aux((y, x+1))
                if y>0:
                    aux((y-1, x))
                if y<m:
                    aux((y+1, x))
        aux(s.get_coord())
        return g

    def sort_stones(self):
        '''
        Trie les pierres du groupe dans l'ordre lexicographique de leurs coordonnées. Permet de
        repérer les groupes identiques (indépendamment de l'ordre des pierres dans la liste du groupe).
        '''
        sorted_stones = sorted(self.get_stones(), key=lambda stone: stone.get_coord())
        self.set_stones(sorted_stones)


    def split(self, s, board):
        '''
        Renvoie la liste des nouveaux groupes lorsqu'on a retiré une pierre au groupe.
        '''
        new_groups = []
        c = s.get_color()
        y = s.get_coord()[0]
        x = s.get_coord()[1]
        m = board.get_size()-1
        self.remove_stone(s)
        if x>0:
            left_s = board.get_board()[(y, x-1)].get_stone()
            if left_s and left_s.get_color() == c:
                left_g = self.dfs_group(left_s, board)
                new_groups.append(left_g)
        if x<m:
            right_s = board.get_board()[(y, x+1)].get_stone()
            if right_s and right_s.get_color() == c:
                rigth_g = self.dfs_group(right_s, board)
                if not(rigth_g in new_groups):
                    new_groups.append(rigth_g)
        if y>0:
            top_s = board.get_board()[(y-1, x)].get_stone()
            if top_s and top_s.get_color() == c:
                top_g = self.dfs_group(top_s, board)
                if not(top_g in new_groups):
                    new_groups.append(top_g)
        if y<m:
            bottom_s = board.get_board()[(y+1, x)].get_stone()
            if bottom_s and bottom_s.get_color() == c:
                bottom_g = self.dfs_group(bottom_s, board)
                if not(bottom_g in new_groups):
                    new_groups.append(bottom_g)
        return new_groups
    
    def is_presumed_dead(self, board):
        '''
        Renvoie si une chaîne est considérée morte à la fin de la partie.
        Une chaîne est considérée morte si elle ne compte qu'un seul degré de liberté ou si elle est isolée des pierres alliées.
        '''

        if self.__liberties == 1:
            return True
        
        # On va réaliser un parcours en profondeur pour savoir si la chaîne est isolée de ses alliés
        visited = []
        def aux(current_coord, visited_edges, size=board.get_size()):
            current_s = board.get_board()[current_coord].get_stone()
            if current_coord in visited or (current_s and current_s.get_color() != self.__color):
                return False
            
            visited.append(current_coord)
            if current_s and not(current_s.get_group() == self) and current_s.get_color() == self.__color:
                return True
            
            y = current_coord[0]
            x = current_coord[1]
            b_top = False
            b_bottom = False
            b_left = False
            b_right = False

            if y>0:
                b_top = aux((y-1, x), visited_edges)
            else:
                visited_edges[0] = True
            if y<size-1:
                b_bottom = aux((y+1, x), visited_edges)
            else:
                visited_edges[1] = True
            if x>0:
                b_left = aux ((y, x-1), visited_edges)
            else:
                visited_edges[2] = True
            if x<size-1:
                b_right = aux((y, x+1), visited_edges)
            else:
                visited_edges[3] = True

            return b_top or b_bottom or b_left or b_right or visited_edges.count(True) >= 3

            
        # La fonction auxiliaire aux renvoie si la chaîne n'est pas isolée
        return not(aux(self.__stones[0].get_coord(), [False, False, False, False]))

    def __eq__(self, group : 'Group') -> bool:
        return self.__color == group.get_color() and self.__stones == group.get_stones()