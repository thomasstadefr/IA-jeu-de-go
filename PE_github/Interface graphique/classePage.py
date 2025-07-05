import sys, pygame
from pygame.locals import *
import variables

class Page:
    def __init__(self, fs):
        self.__width = variables.width
        self.__height = variables.height
        self.__size = (self.__width, self.__height)
        self.__mouseClick = False
        self.__b = 1   
        self.__screen = None 
        if fs == 0:
            self.__screen = pygame.display.set_mode(self.__size)
        elif fs == 1:
            self.__screen = pygame.display.set_mode(self.__size, FULLSCREEN)
            

        self.__bg = pygame.image.load("Interface graphique/fond.png").convert()
        self.__bg = pygame.transform.scale(self.__bg, (self.__width, self.__height))

        self.__boutons = []
        self.__zonesDeTexte = []

    def get_width(self):
        return self.__width 

    def get_height(self):
        return self.__height
    
    def set_mouseClick(self, m):
        self.__mouseClick = m

    def get_b(self):
        return self.__b
    
    def set_b(self, b):
        self.__b = b

    def get_screen(self):
        return self.__screen
    
    def affiche_bg(self):
        self.__screen.blit(self.__bg, (0, 0))  

    def set_boutons(self, b):
        self.__boutons = b

    def affiche(self):
        for i in self.__boutons:
            i.afficher()
        for i in self.__zonesDeTexte:
            i.afficher()
    
    def set_zdt(self, zdt):
        self.__zonesDeTexte = zdt

    def styleBoutons(self):
        for i in self.__boutons:
            if i.mouseOn():
                self.__mouseClick = True
                i.change_text_color((255, 255, 255))

        if self.__mouseClick == True:
            pygame.mouse.set_cursor(pygame.cursors.pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.cursors.pygame.SYSTEM_CURSOR_ARROW)
            for i in self.__boutons:
                i.change_text_color((0, 0, 0))

        self.__mouseClick = False