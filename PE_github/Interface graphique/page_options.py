import sys, pygame
import os
from pygame.locals import *
import variables 
from classeBouton import Bouton
from classeZoneTexte import ZoneDeTexte
from classePage import Page

chemin_dossier_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(chemin_dossier_parent)
from classes.board_class import Board

pygame.init()

class Options(Page):
    def __init__(self, p, fs):
        Page.__init__(self, fs)
        
        self.__p = p
        self.__fs = fs

        self.__boutonRetour = Bouton(self.get_width()/10, self.get_height()/20, self.get_width()/80, self.get_height()/80, self.get_screen(), "Retour")
        self.__boutonTaille1 = Bouton(self.get_width()/10, self.get_height()/20, 10*self.get_width()/40, 16*self.get_height()/40, self.get_screen(), "720x480")
        self.__boutonTaille2 = Bouton(self.get_width()/10, self.get_height()/20, 18*self.get_width()/40, 16*self.get_height()/40, self.get_screen(), "900x600")
        self.__boutonTaille3 = Bouton(self.get_width()/10, self.get_height()/20, 26*self.get_width()/40, 16*self.get_height()/40, self.get_screen(), "1080x720")
        self.__boutonFullScreen = Bouton(self.get_width()/10, self.get_height()/20, 18*self.get_width()/40, 20*self.get_height()/40, self.get_screen(), "Plein écran")
        
        self.set_boutons([self.__boutonRetour,
                          self.__boutonTaille1,
                          self.__boutonTaille2,
                          self.__boutonTaille3,
                          self.__boutonFullScreen])

        while self.get_b():
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.__boutonRetour.mouseOn():
                        if self.__p == 0:
                            self.set_b(0)
                            from page_plateau import Plateau
                            plateau = Plateau(Board(9), self.__fs, 0)
                        elif self.__p == 1:
                            self.set_b(0)
                            from page_menu import Menu
                            menu = Menu(self.__fs)
                        elif self.__p == 2:
                            self.set_b(0)
                            from page_tuto import Tuto
                            tuto = Tuto(self.__fs)
                        elif self.__p == 3:
                            self.set_b(0)
                            from page_plateau import Plateau
                            plateau = Plateau(Board(9), self.__fs, 1)
                    if self.__boutonTaille1.mouseOn():
                        variables.width = 720
                        variables.height = 480
                        self.set_b(0)
                        options = Options(self.__p, 0)
                    if self.__boutonTaille2.mouseOn():
                        variables.width = 900
                        variables.height = 600
                        self.set_b(0)
                        options = Options(self.__p, 0)
                    if self.__boutonTaille3.mouseOn():
                        variables.width = 1080
                        variables.height = 720
                        self.set_b(0)
                        options = Options(self.__p, 0)
                    if self.__boutonFullScreen.mouseOn():
                        variables.width = variables.fsw
                        variables.height = variables.fsh
                        self.set_b(0)
                        options = Options(self.__p, 1)

            self.styleBoutons()

            self.affiche_bg()
            self.affiche()

            pygame.display.update()

if __name__ == "__main__":
    options = Options(0, 0)