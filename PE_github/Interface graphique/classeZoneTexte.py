import pygame

class ZoneDeTexte:
    def __init__(self, w, h, x, y, screen, texts):
        self.__width = w
        self.__height = h
        self.__x = x
        self.__y = y
        self.__tt = texts
        self.__n = len(self.__tt)
        self.__im = pygame.image.load("Interface graphique/bouton.png").convert_alpha()
        self.__im = pygame.transform.scale(self.__im, (self.__width, self.__height))
        self.__screen = screen
        self.__textLength = 100
        self.__font = pygame.font.SysFont(None, self.__textLength)
        self.__texts = [self.__font.render(i, True, (0, 0, 0)) for i in self.__tt]

        if texts != []:
            self.__size = max([self.__font.size(i) for i in texts])
        else:
            self.__size = (0,0)
        
        while self.__size[0] > self.__width - 10 or self.__size[1] > self.__height - 10:
            self.__textLength -= 1
            self.__font = pygame.font.SysFont(None, self.__textLength)
            self.__texts = [self.__font.render(k, True, (0, 0, 0)) for k in self.__tt]
            self.__size = max([self.__font.size(i) for i in texts])

    def afficher(self):
        self.__screen.blit(self.__im, (self.__x, self.__y))
        for i in range(self.__n):
            self.__screen.blit(self.__texts[i], (self.__x + self.__width/2 - self.__size[0]/2, self.__y + (i+1)*self.__height/(self.__n+1) - self.__size[1]/2))

    def get_size(self):
        return (self.__size, self.__textLength)
    
    def set_size(self, s):
        self.__size = s

    def set_textLength(self, len):
        self.__textLength = len
        self.__font = pygame.font.SysFont(None, self.__textLength)
        self.__texts = [self.__font.render(k, True, (0, 0, 0)) for k in self.__tt]