import numpy as np

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
        self.__last_moves = [] # Liste de couples (coordonnnées du coup joué, liste des chaînes capturées)
        self.__black_captured = [] # Pierres noires capturées par Blanc.
        self.__white_captured = [] # Pierres blanches capturées par Noir.
        self.__groups = [] # Liste des chaînes du plateau.
        self.__last_groups = [] # Liste de listes de Group (historique des chaînes créées).
        self.__passed_moves = 0
        
    def get_board(self) -> np.array:
        '''
        Fournit le tableau de plateau

        Returns:
            Un tableaux NumPy représentant le tableau.
        '''
        return self.__board
    
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

    def __str__(self) -> str:
        '''
        Affiche le plateau de manière rudimentaire dans la console. 
        Il suffira de faire print(board) où board est une instance de la
        classe Board. 'O' pour Noir et 'X' pour Blanc.
        
        Returns:
            La chaîne de caractère correspondante.
        '''
        board_str = ""
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__board[i, j].get_stone() is None:
                    board_str += "| _ "
                elif self.__board[i, j].get_stone().get_color() == 0:
                    board_str += "| O "
                else:
                    board_str += "| X "
            board_str += "|\n"
        return board_str
    
    def is_a_valid_move(self, coord: tuple, color: int):
        '''
        Vérifie si un coup est possible. Va de paire avec la fonction play_move().
        Doit vérifier si les coordonnées sont dans le plateau, si la case est libre,
        éviter le ko, éviter le suicide de la pierre.

        Args:
            coord: Coordonnées du coup à jouer.
            color: Couleur du joueur (0 ou 1).

        Returns:
            True si le coup est valide, False sinon.
        '''
        # On vérifie que la pierre est dans le plateau
        if coord[0] >= self.__size or coord[1] >= self.__size or coord[0] < 0 or coord[1] < 0:
            print("Les coordonnées sont en dehors du plateau.")
            return False
        
        # On vérifie que l'intersection n'est pas occupée.
        if self.__board[coord].get_stone() is not None:
            print("L'emplacement est déjà occupé.")
            return False
        

        group_list = []
        for delta in [[-1,0], [0,-1], [1,0], [0,1]]:
            pos = np.array(coord) + delta
            if pos[0] < self.__size and pos[1] < self.__size and pos[0] >= 0 and pos[1] >= 0:
                if self.__board[tuple(pos)].get_stone() is not None and self.__board[tuple(pos)].get_stone().get_color() == color:
                    if self.__board[tuple(pos)].get_stone().get_group() not in group_list:
                        group_list.append(self.__board[tuple(pos)].get_stone().get_group())
        
       
        new_group = Group(color, [Stone(color, coord, self)], self)
        new_stone = None
        for group in group_list:
            new_group = Group.merge(new_group, group)
            self.__groups.remove(group)
            
        # Permet de retirer les doublons
        unique_stones = []
        for stone in new_group.get_stones():
            if stone not in unique_stones:
                unique_stones.append(stone)

        new_group.set_stones(unique_stones)
        for stone in new_group.get_stones():
            stone.set_group(new_group)
            if stone.get_coord() == coord:
                new_stone = stone

        
        self.__groups.append(new_group)
        new_group.update_liberties()

        print("new_group", new_group)
        self.__last_groups.append(group_list)
        for g in self.__groups:
            print("self.__groups :", g)
        for g in group_list:
            print("group_list", g)

        if new_group.get_liberties() == 0:
            print("Suicide non autorisé.")
            return (False, None)
        else:
            return (True, new_stone)
    
        '''
        # On calcule les libertés dans le cas où la pierre n'est connectée à aucune chaîne (il faudra modifier la fonction pour le cas général).
        liberties = 0
        for delta in [[-1,0], [0,-1], [1,0], [0,1]]:
            pos = np.array(coord) + delta
            if pos[0] < self.__size and pos[1] < self.__size and pos[0] >= 0 and pos[1] >= 0: 
                if self.__board[tuple(pos)].get_stone() is None:
                    liberties += 1
        
        # On vérifie que la pierre ne ne suicide pas.
        if liberties == 0:
            print("La pierre n'a aucun degré de liberté.")
            return(False)
        '''
    def play_move(self, coord: tuple, color: int) -> None:
        '''
        Joue un coup. Doit s'assurer que le coup est valide, puis
        mettre à jour les degrés de liberté, les chaînes, changer 
        self.__turn, etc.
        '''
<<<<<<< HEAD:board_classes.py
        # verifier si le coup est valide 
        if not self.is_valid_a_move(coord,color):
            #si le coup n'est valide
            print("coup invalide, le coup ne sera pas joué")
            return 
            # Créer une instance de la classe Stone pour représenter la pierre à jouer
        new_stone = Stone(color, coord, self)
        self.__board[coord].set_stone(new_stone)#placer une pierre
        new_stone.get_groupe().update_liberties
        
        # Inachevé, joue un coup sans vérifier qu'il soit valide.
        self.__board[coord].set_stone(Stone(color, coord, self))
        return
=======


        
        if self.is_a_valid_move(coord, color)[0]:
            new_stone = self.is_a_valid_move(coord, color)[1]
            print("newwwwwwww", new_stone)
            new_stone.get_group().update_liberties()#mettre à jour les degrés de libertés
            self.__board[coord].set_stone(new_stone)
        self.__turn = 1-self.__turn    #changer le tour
        print(self) #afficher le plateau après le coup 
               
    '''
    def __update_board(self, new_stone:'Stone') -> list:
        captured_groups = []
        self.__board[new_stone.get_coord()].set_stone(new_stone)
        for delta in [[-1, 0], [0, -1], [1, 0], [0, 1]]:
            pos = np.array(new_stone.get_coord()) + delta
            if pos[0] <self.__size and pos[1]<self.__size and pos[0]>=0 and pos[1]>=0:
               if self.__board[tuple(pos)].get_stone() iq None
                liberties += 1

        if liberties==0:
           print("La pierre n'a aucun degré de liberté.")
           return False
        else:
            return True
       '''                    
>>>>>>> 7c334204bc149811448e0ea2f2b50c9cc828e250:classes/(old_classes).py

    def pass_move(self):
        self.__turn = 1 - self.__turn
        self.__passed_moves += 1
        if self.__passed_moves == 2:
            return #fin de la partie lorsque les  deux joueurs passsent ler tour
    ''''        
    def cancel_move(self):
        last_moves = self.__last_moves
        if last_moves:
           coord, captured_groups = last_moves.pop()
           self.__turn = 1-self.__turn #Changer le tour
           #Annuler le coup en retirant la pierre du plateau
           self.__board[coord].set_stone(None)
        
        #Rétablir les pierres capturées 
        for group in captured_groups:
            for stone in group.get_stones():
                stone_coord = stone.get_coord()
                self.__board[stone_coord].set_stone(stone)
                stone.set_group(group)
                group.update_liberties()    
            
                
        self.passed_moves = self.passed_moves -1
        pass
    '''


class Intersection:
    def __init__(self, coord: tuple) -> None:
        '''
        Initialise une instance de la classe Intersection.

        Args:
            coord: Coordonnées de l'intersection.
        '''
        self.__coord = coord
        self.__stone = None  # Pas de pierre sur l'intersection
    
    def get_stone(self):
        '''
        Renvoie la pierre présente sur l'intersection
        '''
        return self.__stone

    def set_stone(self, stone: 'Stone') -> None:
        '''
        Place une pierre sur l'intersection.

        Args:
            stone: Pierre à placer.
        '''
        self.__stone = stone

    def is_empty(self) -> bool:
        '''
        Indique si l'intersection est vide

        Returns:
            True si l'intersection est vide, False sinon.
        '''
        return self.__stone is None

    def __str__(self):
        '''
        Affiche l'intersection

        Returns:
            La chaîne de caractère correspondante.
        
        '''
        return f"Intersection: coord = {self.__coord}, (Stone: {self.__stone})"


# Classe des pierres
class Stone():
    def __init__(self, color: int, coord: tuple, board: 'Board') -> None:
        '''
        Initialise une instance de la classe Stone.

        Args:
            color: Couleur de la pierre (0 ou 1).
            coord: Coordonnées de la pierre.
            board: Plateau.
        
        Returns:
            Instance de la classe Pierre.
        '''
        self.__color = color # 0 pour Noir, 1 pour Blanc.
        self.__board = board # Plateau
        self.__coord = coord # Coordonnées de la pierre.
        self.__group = Group(self.__color, [self], self.__board) # Chaîne à laquelle appartient la pierre.
        self.__atari = False # Est en atari.
        self.__liberties = 4 # Nombre de degrés de liberté

    def get_color(self) -> int:
        '''
        Renvoie la couleur de la pierre.

        Returns:
            0 pour la couleur Noire, 1 pour la couleur Blanche.
        '''
        return(self.__color)
    
    def get_coord(self) -> tuple:
        '''
        Renvoie les coordonnées de la pierre.

        Returns:
            Le tuple des coordonnées
        '''
        return(self.__coord)
    
    def get_group(self) -> 'Group':
        '''
        Renvoie un objet de la classe Group() correspondant à la chaîne
        à laquelle appartient la pierre. 

        Returns:
            Instance de la classe Group().
        '''
        return self.__group
    
    def get_atari(self) -> bool:
        '''
        Indique si la pierre est en atari (on appelera la fonction
        Group.get_atari() , dans la mise à jour de self.__atari 
        dans la fonction Board.jouer_coup() pur rester général).

        Returns:
            True si la pierre est en atari, False sinon.
        '''
        return(self.__atari)
    
    def get_liberties(self) -> int:
        '''
        Donne le nombre de degrés de liberté de la pierre

        Returns:
            Un entier indiquant le nombre de degrés de liberté.
        '''
        return(self.__liberties)
    
    def set_atari(self)-> None:
        '''
        Change l'état de la pierre selon qu'elle soit en
        atari ou non.
        '''
        self.__atari = self.__liberties == 1
        return

    def set_group(self, group: 'Group') -> None:
        '''
        Définit la chaîne à laquelle appartient la pierre.

        Args:
            group: Chaîne à laquelle appartient la pierre.
        '''
        self.__group = group
        return
    
    def set_liberties(self, liberties: int) -> None:
        '''
        Change le degré de liberté de la pierre

        Args:
            liberties: Nouvelle valeur du nombre de degrés de libertés
        '''
        self.__liberties = liberties
        return
    
    def __str__(self) -> str:
        s = ""
        for stone in self.get_group().get_stones():
            s += str(stone.get_coord())
        return f"Pierre : couleur = {self.__color}, coord = {self.__coord}, group="+s

    def __eq__(self, stone : 'Stone'):
        return self.__color == stone.get_color() and self.__coord == stone.get_coord()


# Classe des chaînes
class Group():
    def __init__(self, color: int, stones: list, board: 'Board') -> None:
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
        self.__board = board # Plateau.

    def get_board(self):
        return self.__board

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
    
    def set_stones(self, stones):
        self.__stones = stones
        return 
    
    def add_stone(self, stone: 'Stone') -> None:
        '''
        Ajoute une pierre à la chaîne.

        Args:
            stone: Pierre à ajouter à la chaîne. 
        '''
        self.__stones.append(stone)
        return
    
    def update_liberties(self) -> None:
        '''
        Met à jour les degrés de liberté de la chaîne.
        '''
        liberties = 0
        inter_list = [] # Liste des coordonnées des intersections vides adjacentes à la chaîne.
        for stone in self.__stones:
            for delta in [[-1,0], [0,-1], [1,0], [0,1]]:
                pos = np.array(stone.get_coord()) + delta
                # La dernière condition permet de ne pas compter deux fois les mêmes intersections.
                if pos[0] < self.__board.get_size() and pos[1] < self.__board.get_size() and pos[0] >= 0 and pos[1] >= 0 and not tuple(pos) in inter_list: 
                    if self.__board.get_board()[tuple(pos)].get_stone() is None:
                        liberties += 1
                        inter_list.append(tuple(pos))
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
        new_group = Group(group1.get_color(), [], group1.get_board())
        for stone in group1.get_stones():
            new_group.add_stone(stone)
            stone.set_group(new_group)
        for stone in group2.get_stones():
            new_group.add_stone(stone)
            stone.set_group(new_group)
        return new_group
    
    def __eq__(self, group : 'Group') -> bool:
        return self.__color == group.get_color() and self.__stones == group.get_stones()
        
    

# Tests
if __name__ == "__main__":
    board = Board(9)
    print(board,"\n\n")
    board.play_move((0,1), 0)
    print(board,"\n\n")
    board.play_move((0,0), 1)
    print(board,"\n\n")
    board.play_move((1,0), 1)
    print(board, "\n\n")
    print("hhhh", board.get_board()[(1,0)].get_stone().get_group())
    board.play_move((1,1), 1)
    print(board,"\n\n")
    '''
    board.play_move((8,8), 1)
    board.play_move((4,4), 0)
    board.play_move((5,5), 0)
    board.play_move((4,6), 0)
    board.play_move((3,5), 0)

    print(board)
    board.play_move((5,6), 1)
    print(board)
    for group in board.get_groups():   
        print(group)

    print(board.get_board()[0,0])

    board.is_a_valid_move((4,5), 0)

    ch = Group(1, [Stone(1, (0,0), board), Stone(1, (1,0), board), Stone(1, (1,1), board)], board)
    print(ch)
    ch.update_liberties()
    print("Degrés de liberté de la chaîne :", ch.get_liberties())
    '''