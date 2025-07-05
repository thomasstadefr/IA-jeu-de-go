class Intersection:
    from classes.stone_class import Stone

    def __init__(self, coord: tuple) -> None:
        '''
        Initialise une instance de la classe Intersection.

        Args:
            coord: Coordonnées de l'intersection.
        '''
        self.__coord = coord
        self.__stone = None  # Pas de pierre sur l'intersection

    def get_coord(self):
        return self.__coord
    
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
        return

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