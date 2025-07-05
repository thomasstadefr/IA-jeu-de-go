import numpy as np
from classes.group_class import Group

class Stone():
    def __init__(self, color: int, coord: tuple) -> None:
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
        self.__coord = coord # Coordonnées de la pierre.
        self.__group = Group(self.__color, [self]) # Chaîne à laquelle appartient la pierre.
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
    
    def update_liberties(self, board) -> None:
        '''
        Met à jour les degrés de libertés de la pierre.
        '''
        liberties = 0
        for delta in [[-1,0], [0,-1], [1,0], [0,1]]:
            pos = np.array(self.__coord) + delta
            if pos[0] < board.get_size() and pos[1] < board.get_size() and pos[0] >= 0 and pos[1] >= 0: 
                if board.get_board()[tuple(pos)].get_stone() is None:
                    liberties += 1
        self.__liberties = liberties
    
    def __str__(self) -> str:
        s = ""
        for stone in self.get_group().get_stones():
            s += str(stone.get_coord())
        return f"Pierre : couleur = {self.__color}, coord = {self.__coord}, group="+s

    def __eq__(self, stone : 'Stone'):
        return self.__color == stone.get_color() and self.__coord == stone.get_coord()