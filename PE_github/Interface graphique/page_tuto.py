import sys, pygame
import os
from pygame.locals import *
import variables 
from classeBouton import Bouton
from classeZoneTexte import ZoneDeTexte
from classePage import Page
from pygame import gfxdraw

chemin_dossier_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(chemin_dossier_parent)
from classes.board_class import Board

pygame.init()

class Tuto(Page):
    def __init__(self, fs):
        Page.__init__(self, fs)
        self.__fs = fs

        self.__k = 0
        self.__titres = [["Règles du jeu"], ["Stratégies de base"]]
        self.__texte = [["1) Goban", "Le Go se joue sur un plateau de taille variable appelé Goban", "C’est un jeu à 2 joueurs au tour par tour"],
                        ["2) Pierres, intersections", "Lorsque c’est son tour de jouer, un joueur peut placer une pierre", "de sa couleur sur une intersection (croisement d’une ligne", "et d’une colonne) si une pierre ne s’y trouve pas déjà ou passer son tour"],
                        ["3) Chaînes", "Les pierres forment des chaînes : si deux pierres de même couleur", "sont placées côte à côte verticalement ou horizontalement alors", "elles font partie de la même chaîne"],
                        ["4) Degrés de liberté", "On appelle degré de liberté d’une chaîne le nombre de case du", "Goban où poser une pierre allongerait la chaîne"],
                        ["5) Capture", "Lorsqu’un joueur prive de degré de liberté une chaîne adverse", "cette chaîne est alors capturée et retirée du Goban"],
                        ["6) Suicide", "On appelle suicide le fait de jouer une pierre ne réalisant aucune", "capture et se faisant capturer. Ce coup est illégal"],
                        ["7) Répétition", "Il est interdit de répéter la même position deux fois dans la partie.", "Le cas le plus courant est celui du ko"],
                        ["8) Fin de partie et comptage des points", "Lorsque la partie se termine (les deux joueurs ont passé successivement),", "on retire les pierres mortes et on compte les pierres restantes en tenant compte", "du komi (compensation de points pour les blancs du fait que les noirs jouent en premier)"],
                        ["Connecter ses", "pierres pour", "avoir moins", "de chaînes", "à défendre"],
                        ["Créer des yeux"],
                        ["Attaquer l'adversaire"]]
        self.__n = len(self.__texte)

        self.__board = Board(9)
        self.__mat = self.__board.get_board()
        self.__m = len(self.__mat)
        self.__couleurs = [[-1 for i in range(self.__m)] for i in range(self.__m)]
        self.__modele = [[-1 for i in range(self.__m)] for i in range(self.__m)]
        self.__modif = 0
        self.__tailleGoban = min(self.get_width()/2, 3*self.get_height()/4)
        self.__xp = 3*self.get_width()/8 - 109*self.__tailleGoban/300
        self.__yp = 73*self.get_height()/480
        self.__caseTaille = self.__tailleGoban/11
        self.__ex = self.get_width()/60
        self.__ey = self.get_height()/60
        self.__goban = pygame.image.load("Interface graphique/Goban 9x9.png").convert()
        self.__goban = pygame.transform.scale(self.__goban, (self.__tailleGoban, self.__tailleGoban))
        self.__ajoue = 0

        self.__boutonMenu = Bouton(self.get_width()/10, self.get_height()/20, self.get_width()/80, self.get_height()/40, self.get_screen(), "Menu")
        self.__boutonOptions = Bouton(self.get_width()/20, self.get_height()/20, self.get_width()/80, 17*self.get_height()/200, self.get_screen(), "Options")
        self.__boutonPrecedent = Bouton(self.get_width()/4, self.get_height()/8, 3*self.get_width()/16, 23*self.get_height()/32, self.get_screen(), "<<<")
        self.__boutonSuivant = Bouton(self.get_width()/4, self.get_height()/8, 9*self.get_width()/16, 23*self.get_height()/32, self.get_screen(), ">>>")
        self.__titre = ZoneDeTexte(9*self.get_width()/20, self.get_height()/8, 11*self.get_width()/40, 3*self.get_height()/24, self.get_screen(), self.__titres[0])
        self.__bravo = ZoneDeTexte(self.__tailleGoban, self.get_height()/10, 30*self.get_width()/80 - self.__tailleGoban/2, 17*self.get_height()/20, self.get_screen(), ["Bravo !"])
        self.__essaieencore = ZoneDeTexte(self.__tailleGoban, self.get_height()/10, 30*self.get_width()/80 - self.__tailleGoban/2, 17*self.get_height()/20, self.get_screen(), ["Non, essaie encore !"])
        self.__boutonReessayer = Bouton(3*self.get_width()/20, 3*self.get_height()/40, 59*self.get_width()/80, 34*self.get_height()/40, self.get_screen(), "Réessayer")

        while self.get_b():
            x, y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.__boutonMenu.mouseOn():
                        self.set_b(0)
                        from page_menu import Menu
                        menu = Menu(self.__fs)
                    if self.__boutonOptions.mouseOn():
                        self.set_b(0)
                        from page_options import Options
                        options = Options(2, self.__fs)
                    if self.__boutonPrecedent.mouseOn():
                        self.__k -= 1
                        self.__board = Board(9)
                        self.__mat = self.__board.get_board()
                        self.__m = len(self.__mat)
                        self.__couleurs = [[-1 for i in range(self.__m)] for i in range(self.__m)]
                        self.__modif = 0
                        self.__ajoue = 0
                    if self.__boutonSuivant.mouseOn():
                        self.__k += 1
                        self.__board = Board(9)
                        self.__mat = self.__board.get_board()
                        self.__m = len(self.__mat)
                        self.__couleurs = [[-1 for i in range(self.__m)] for i in range(self.__m)]
                        self.__modif = 0
                        self.__ajoue = 0
                    if self.__boutonReessayer.mouseOn():
                        self.__modif = 0
                        self.__board = Board(9)
                        self.__mat = self.__board.get_board()
                        self.__couleurs = [[-1 for i in range(self.__m)] for i in range(self.__m)]
                        self.__ajoue = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.__k > 0:
                            self.__k -= 1
                            self.__board = Board(9)
                        self.__mat = self.__board.get_board()
                        self.__m = len(self.__mat)
                        self.__couleurs = [[-1 for i in range(self.__m)] for i in range(self.__m)]
                        self.__modif = 0
                        self.__ajoue = 0
                    if event.key == pygame.K_RIGHT:
                        if self.__k < self.__n-1:
                            self.__k += 1
                        self.__board = Board(9)
                        self.__mat = self.__board.get_board()
                        self.__m = len(self.__mat)
                        self.__couleurs = [[-1 for i in range(self.__m)] for i in range(self.__m)]
                        self.__modif = 0
                        self.__ajoue = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in range(self.__m):
                        for j in range(self.__m):
                            if (x > self.__xp - self.__ex + i*self.__caseTaille) and (x < self.__xp + self.__ex + i*self.__caseTaille) and (y > self.__yp - self.__ey + j*self.__caseTaille) and (y < self.__yp + self.__ey + j*self.__caseTaille) and not (self.__modif):
                                if self.__board.is_a_valid_move((i,j), self.__board.get_turn(), 1)[0]:
                                    self.__couleurs[i][j] = 0
                                    self.__board.play_move((i,j), 0)
                                    print((i,j))
                                    self.__modif = 1

            self.affiche_bg()

            if self.__k < 8:
                self.__boutonPrecedent = Bouton(self.get_width()/4, self.get_height()/8, 3*self.get_width()/16, 23*self.get_height()/32, self.get_screen(), "<<<")
                self.__boutonSuivant = Bouton(self.get_width()/4, self.get_height()/8, 9*self.get_width()/16, 23*self.get_height()/32, self.get_screen(), ">>>")
                self.__titre = ZoneDeTexte(9*self.get_width()/20, self.get_height()/8, 11*self.get_width()/40, 3*self.get_height()/24, self.get_screen(), self.__titres[self.__k//8])
                self.__tuto = ZoneDeTexte(18*self.get_width()/20, self.get_height()/3, self.get_width()/20, 7*self.get_height()/24, self.get_screen(), self.__texte[self.__k])
                self.set_zdt([self.__titre,
                              self.__tuto])
            else:
                self.get_screen().blit(self.__goban, (30*self.get_width()/80 - self.__tailleGoban/2,self.get_height()/20))
                self.__boutonPrecedent = Bouton(3*self.get_width()/20, 3*self.get_height()/40, 13*self.get_width()/20, 29*self.get_height()/40, self.get_screen(), "<<<")
                self.__boutonSuivant = Bouton(3*self.get_width()/20, 3*self.get_height()/40, 33*self.get_width()/40, 29*self.get_height()/40, self.get_screen(), ">>>")
                self.__titre = ZoneDeTexte(13*self.get_width()/40, self.get_height()/8, 26*self.get_width()/40, self.get_height()/20, self.get_screen(), self.__titres[self.__k//8])
                self.__tuto = ZoneDeTexte(13*self.get_width()/40, self.get_height()/2, 26*self.get_width()/40, 4*self.get_height()/20, self.get_screen(), self.__texte[self.__k])
                self.__question = ZoneDeTexte(self.__tailleGoban, 7*self.get_height()/50, 30*self.get_width()/80 - self.__tailleGoban/2, 83*self.get_height()/100, self.get_screen(), ["Aux noirs de jouer.", "Pose la pierre au bon endroit !"])
                self.set_zdt([self.__titre,
                              self.__tuto,
                              self.__question])
                for i in range(self.__m):
                    for j in range(self.__m):
                        if (x > self.__xp - self.__ex + i*self.__caseTaille) and (x < self.__xp + self.__ex + i*self.__caseTaille) and (y > self.__yp - self.__ey + j*self.__caseTaille) and (y < self.__yp + self.__ey + j*self.__caseTaille):
                            if self.__board.is_a_valid_move((i,j), self.__board.get_turn(), 0)[0] and self.__board.get_allow():
                                self.set_mouseClick(True)
                if self.__k == 8:
                    if self.__ajoue == 0:
                        self.__board.play_move((6, 2), 0)
                        self.__couleurs[6][2] = 0
                        self.__board.play_move((5, 2), 0)
                        self.__couleurs[5][2] = 0
                        self.__board.play_move((4, 2), 0)
                        self.__couleurs[4][2] = 0
                        self.__board.play_move((3, 3), 0)
                        self.__couleurs[3][3] = 0
                        self.__board.play_move((3, 4), 0)
                        self.__couleurs[3][4] = 0
                        self.__board.play_move((3, 2), 1)
                        self.__couleurs[3][2] = 1
                        self.__board.play_move((2, 3), 1)
                        self.__couleurs[2][3] = 1
                        self.__board.play_move((2, 4), 1)
                        self.__couleurs[2][4] = 1
                        self.__board.play_move((4, 4), 1)
                        self.__couleurs[4][4] = 1
                        self.__board.play_move((3, 5), 1)
                        self.__couleurs[3][5] = 1
                        for i in range(self.__m):
                            self.__modele[i] = self.__couleurs[i].copy()
                        self.__modele[4][3] = 0
                        self.__ajoue = 1
                if self.__k == 9:
                    if self.__ajoue == 0:
                        self.__board.play_move((8, 3), 1)
                        self.__couleurs[8][3] = 1
                        self.__board.play_move((7, 3), 1)
                        self.__couleurs[7][3] = 1
                        self.__board.play_move((6, 3), 1)
                        self.__couleurs[6][3] = 1
                        self.__board.play_move((5, 3), 1)
                        self.__couleurs[5][3] = 1
                        self.__board.play_move((4, 3), 1)
                        self.__couleurs[4][3] = 1
                        self.__board.play_move((3, 3), 1)
                        self.__couleurs[3][3] = 1
                        self.__board.play_move((2, 3), 1)
                        self.__couleurs[2][3] = 1
                        self.__board.play_move((8, 4), 1)
                        self.__couleurs[8][4] = 1
                        self.__board.play_move((8, 5), 1)
                        self.__couleurs[8][5] = 1
                        self.__board.play_move((8, 6), 1)
                        self.__couleurs[8][6] = 1
                        self.__board.play_move((8, 7), 1)
                        self.__couleurs[8][7] = 1
                        self.__board.play_move((7, 7), 1)
                        self.__couleurs[7][7] = 1
                        self.__board.play_move((6, 7), 1)
                        self.__couleurs[6][7] = 1
                        self.__board.play_move((5, 7), 1)
                        self.__couleurs[5][7] = 1
                        self.__board.play_move((4, 7), 1)
                        self.__couleurs[4][7] = 1
                        self.__board.play_move((3, 7), 1)
                        self.__couleurs[3][7] = 1
                        self.__board.play_move((2, 7), 1)
                        self.__couleurs[2][7] = 1
                        self.__board.play_move((2, 6), 1)
                        self.__couleurs[2][6] = 1
                        self.__board.play_move((2, 5), 1)
                        self.__couleurs[2][5] = 1
                        self.__board.play_move((2, 4), 1)
                        self.__couleurs[2][4] = 1
                        self.__board.play_move((7, 4), 0)
                        self.__couleurs[7][4] = 0
                        self.__board.play_move((7, 5), 0)
                        self.__couleurs[7][5] = 0
                        self.__board.play_move((7, 6), 0)
                        self.__couleurs[7][6] = 0
                        self.__board.play_move((6, 6), 0)
                        self.__couleurs[6][6] = 0
                        self.__board.play_move((5, 6), 0)
                        self.__couleurs[5][6] = 0
                        self.__board.play_move((4, 6), 0)
                        self.__couleurs[4][6] = 0
                        self.__board.play_move((3, 6), 0)
                        self.__couleurs[3][6] = 0
                        self.__board.play_move((3, 5), 0)
                        self.__couleurs[3][5] = 0
                        self.__board.play_move((3, 4), 0)
                        self.__couleurs[3][4] = 0
                        self.__board.play_move((4, 4), 0)
                        self.__couleurs[4][4] = 0
                        self.__board.play_move((5, 4), 0)
                        self.__couleurs[5][4] = 0
                        self.__board.play_move((6, 4), 0)
                        self.__couleurs[6][4] = 0
                        for i in range(self.__m):
                            self.__modele[i] = self.__couleurs[i].copy()
                        self.__modele[5][5] = 0
                        self.__ajoue = 1
                if self.__k == 10:
                    if self.__ajoue == 0:
                        self.__board.play_move((2, 2), 0)
                        self.__couleurs[2][2] = 0
                        self.__board.play_move((2, 3), 0)
                        self.__couleurs[2][3] = 0
                        self.__board.play_move((2, 4), 0)
                        self.__couleurs[2][4] = 0
                        self.__board.play_move((2, 5), 0)
                        self.__couleurs[2][5] = 0
                        self.__board.play_move((3, 3), 0)
                        self.__couleurs[3][3] = 0
                        self.__board.play_move((3, 6), 0)
                        self.__couleurs[3][6] = 0
                        self.__board.play_move((4, 1), 0)
                        self.__couleurs[4][1] = 0
                        self.__board.play_move((4, 6), 0)
                        self.__couleurs[4][6] = 0
                        self.__board.play_move((5, 4), 0)
                        self.__couleurs[5][4] = 0
                        self.__board.play_move((5, 5), 0)
                        self.__couleurs[5][5] = 0
                        self.__board.play_move((3, 1), 1)
                        self.__couleurs[3][1] = 1
                        self.__board.play_move((3, 2), 1)
                        self.__couleurs[3][2] = 1
                        self.__board.play_move((3, 4), 1)
                        self.__couleurs[3][4] = 1
                        self.__board.play_move((3, 5), 1)
                        self.__couleurs[3][5] = 1
                        self.__board.play_move((4, 3), 1)
                        self.__couleurs[4][3] = 1
                        self.__board.play_move((4, 4), 1)
                        self.__couleurs[4][4] = 1
                        self.__board.play_move((4, 5), 1)
                        self.__couleurs[4][5] = 1
                        self.__board.play_move((4, 2), 0)
                        self.__couleurs[4][2] = 0
                        self.__board.play_move((5, 3), 1)
                        self.__couleurs[5][3] = 1
                        self.__board.play_move((2, 1), 0)
                        self.__couleurs[2][1] = 0
                        self.__board.play_move((3, 0), 1)
                        self.__couleurs[3][0] = 1
                        self.__board.play_move((4, 0), 0)
                        self.__couleurs[4][0] = 0
                        self.__board.play_move((2, 0), 1)
                        self.__couleurs[2][0] = 1
                        for i in range(self.__m):
                            self.__modele[i] = self.__couleurs[i].copy()
                        self.__modele[1][0] = 0
                        self.__ajoue = 1


            
            if self.__k == 0:
                self.set_boutons([self.__boutonMenu,
                                  self.__boutonOptions,
                                  self.__boutonSuivant])
            elif self.__k == self.__n-1:
                self.set_boutons([self.__boutonMenu,
                                  self.__boutonOptions,
                                  self.__boutonPrecedent])
            else:
                self.set_boutons([self.__boutonMenu,
                                  self.__boutonOptions,
                                  self.__boutonPrecedent,
                                  self.__boutonSuivant])
            if self.__k > 7:
                if self.__couleurs == self.__modele:
                    self.set_zdt([self.__titre,
                              self.__tuto,
                              self.__bravo])
                elif self.__modif:
                    self.set_zdt([self.__titre,
                                  self.__tuto,
                                  self.__essaieencore])
                    if self.__k != 10:
                        self.set_boutons([self.__boutonMenu,
                                          self.__boutonOptions,
                                          self.__boutonPrecedent,
                                          self.__boutonSuivant, 
                                          self.__boutonReessayer])
                    else:
                        self.set_boutons([self.__boutonMenu,
                                          self.__boutonOptions,
                                          self.__boutonPrecedent,
                                          self.__boutonReessayer])



            self.styleBoutons()

            self.affiche()

            for i in range(self.__m):
                for j in range(self.__m):
                    if not(self.__mat[i][j].get_stone() is None):
                        if self.__couleurs[i][j] == 0:
                            self.draw_circle(self.get_screen(), int(self.__xp + i*self.__caseTaille), int(self.__yp + j*self.__caseTaille), int(self.__caseTaille/2), (0,0,0))
                        elif self.__couleurs[i][j] == 1:
                            self.draw_circle(self.get_screen(), int(self.__xp + i*self.__caseTaille), int(self.__yp + j*self.__caseTaille), int(self.__caseTaille/2), (255,255,255))

            pygame.display.update()

    def draw_circle(self, surface, x, y, radius, color):
        gfxdraw.aacircle(surface, x, y, radius, color)
        gfxdraw.filled_circle(surface, x, y, radius, color)

if __name__ == "__main__":
    tuto = Tuto(0)