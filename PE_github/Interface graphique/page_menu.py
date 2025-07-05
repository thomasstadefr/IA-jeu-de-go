import sys, pygame
import webbrowser
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

## Titre de l'interface
pygame.display.set_caption("Jeu de Go")

# Charger le logo
logo = pygame.image.load("logo_go.png")
pygame.display.set_icon(logo)

class Menu(Page):
    def __init__(self, fs):
        w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
        variables.fsw = w
        variables.fsh = h
        variables.width = variables.fsw
        variables.height = variables.fsh
        self.__fs = fs

        Page.__init__(self, fs)

        self.__boutonOptions = Bouton(self.get_width()/10, self.get_height()/20, self.get_width()/80, self.get_height()/40, self.get_screen(), "Options")
        self.__boutonQuitter = Bouton(self.get_width()/10, self.get_height()/20, self.get_width()/80, 37*self.get_height()/40, self.get_screen(), "Quitter")
        #self.__boutonRetourBug = Bouton(self.get_width()/10, self.get_height()/20, 71*self.get_width()/80, 37*self.get_height()/40, self.get_screen(), "...")
        self.__boutonJouerIA = Bouton(4*self.get_width()/10, self.get_height()/8, 3*self.get_width()/10, 7*self.get_height()/64, self.get_screen(), "Jouer contre l'IA")
        self.__boutonJouerLocal = Bouton(4*self.get_width()/10, self.get_height()/8, 3*self.get_width()/10, 21*self.get_height()/64, self.get_screen(), "Jouer en local")
        #self.__boutonJouerLigne = Bouton(4*self.get_width()/10, self.get_height()/10, 3*self.get_width()/10, 18*self.get_height()/40, self.get_screen(), "Jouer en ligne")
        self.__boutonTutoriel = Bouton(4*self.get_width()/10, self.get_height()/8, 3*self.get_width()/10, 35*self.get_height()/64, self.get_screen(), "Tutoriel")
        self.__boutonRU = Bouton(4*self.get_width()/10, self.get_height()/8, 3*self.get_width()/10, 49*self.get_height()/64, self.get_screen(), "Faire un retour")
        
        self.set_boutons([self.__boutonQuitter,
                          self.__boutonOptions,
                          #self.__boutonRetourBug,
                          self.__boutonJouerIA,
                          self.__boutonJouerLocal,
                          #self.__boutonJouerLigne,
                          self.__boutonTutoriel,
                          self.__boutonRU])

        while self.get_b():
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.__boutonQuitter.mouseOn():
                        self.set_b(0)
                        sys.exit()
                    if self.__boutonJouerLocal.mouseOn():
                        from page_plateau import Plateau
                        self.set_b(0)
                        plateau = Plateau(Board(9), self.__fs, 0)
                    if self.__boutonJouerIA.mouseOn():
                        from page_plateau import Plateau
                        self.set_b(0)
                        plateau = Plateau(Board(9), self.__fs, 1)
                    if self.__boutonOptions.mouseOn():
                        from page_options import Options
                        self.set_b(0)
                        options = Options(1, self.__fs)
                    if self.__boutonTutoriel.mouseOn():
                        from page_tuto import Tuto
                        self.set_b(0)
                        tuto = Tuto(self.__fs)
                    if self.__boutonRU.mouseOn():
                        webbrowser.open("https://docs.google.com/forms/d/e/1FAIpQLScbkMAINJsww12QgaOFccIogSuPxdzf7jc-bJ4OYLHujB59-w/viewform?usp=sf_link")

            self.styleBoutons()

            self.affiche_bg()
            self.affiche()

            pygame.display.update()

# Position pour apprendre à lier ses chaînes
def tutorial_pos_1():
    b = Board(9)
    b.play_move((6, 2), 1)
    b.play_move((5, 2), 1)
    b.play_move((4, 2), 1)
    b.play_move((3, 3), 1)
    b.play_move((3, 4), 1)
    b.play_move((3, 2), 0)
    b.play_move((2, 3), 0)
    b.play_move((2, 4), 0)
    b.play_move((4, 4), 0)
    b.play_move((3, 5), 0)


# Position pour apprendre à créer des yeux
def tutorial_pos_2():
    b = Board(9)
    b.play_move((8, 3), 1)
    b.play_move((7, 3), 1)
    b.play_move((6, 3), 1)
    b.play_move((5, 3), 1)
    b.play_move((4, 3), 1)
    b.play_move((3, 3), 1)
    b.play_move((2, 3), 1)
    b.play_move((8, 4), 1)
    b.play_move((8, 5), 1)
    b.play_move((8, 6), 1)
    b.play_move((8, 7), 1)
    b.play_move((7, 7), 1)
    b.play_move((6, 7), 1)
    b.play_move((8, 7), 1)
    b.play_move((5, 7), 1)
    b.play_move((4, 7), 1)
    b.play_move((3, 7), 1)
    b.play_move((2, 7), 1)
    b.play_move((2, 6), 1)
    b.play_move((2, 5), 1)
    b.play_move((2, 4), 1)
    b.play_move((7, 4), 0)
    b.play_move((7, 5), 0)
    b.play_move((7, 6), 0)
    b.play_move((6, 6), 0)
    b.play_move((5, 6), 0)
    b.play_move((4, 6), 0)
    b.play_move((3, 6), 0)
    b.play_move((3, 5), 0)
    b.play_move((3, 4), 0)
    b.play_move((4, 4), 0)
    b.play_move((5, 4), 0)
    b.play_move((6, 4), 0)

# Position pour apprendre à utiliser l'initiative et créer des menaces
def tutorial_pos_3():
    b = Board(9)
    b.play_move((2, 2), 0)
    b.play_move((2, 3), 0)
    b.play_move((2, 4), 0)
    b.play_move((2, 5), 0)
    b.play_move((3, 3), 0)
    b.play_move((3, 6), 0)
    b.play_move((4, 1), 0)
    b.play_move((4, 6), 0)
    b.play_move((5, 4), 0)
    b.play_move((5, 5), 0)
    b.play_move((3, 1), 1)
    b.play_move((3, 2), 1)
    b.play_move((3, 4), 1)
    b.play_move((3, 5), 1)
    b.play_move((4, 3), 1)
    b.play_move((4, 4), 1)
    b.play_move((4, 5), 1)
    # Solution du problème
    b.play_move((4, 2), 0)
    b.play_move((5, 3), 1)
    b.play_move((2, 1), 0)
    b.play_move((3, 0), 1)
    b.play_move((4, 0), 0)   # Le dernier et avant-dernier coup blanc peuvent être interchangés
    b.play_move((2, 0), 1)
    b.play_move((1, 0), 0)

if __name__ == "__main__":
    menu=Menu(1)

