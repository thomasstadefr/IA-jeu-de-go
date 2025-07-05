import sys, pygame
import os
from pygame.locals import *
import variables
from classeBouton import Bouton
from classeZoneTexte import ZoneDeTexte
from classePage import Page
from classeChat import Chat
from pygame import gfxdraw

chemin_dossier_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(chemin_dossier_parent)
from classes.board_class import Board
from IA.search_tree import pvs, serialize_board

pygame.init()

class Plateau(Page):
    def __init__(self, board, fs, ia):
        Page.__init__(self, fs)
        self.__board = board
        self.__mat = self.__board.get_board()
        self.__n = len(self.__mat)
        self.__tailleGoban = min(self.get_width()/2, 3*self.get_height()/4)
        self.__caseTaille = self.__tailleGoban/11
        self.__xp = 3*self.get_width()/8 - 109*self.__tailleGoban/300
        self.__yp = 73*self.get_height()/480
        self.__ex = self.get_width()/60
        self.__ey = self.get_height()/60
        self.__couleurs = [[-1 for i in range(self.__n)] for i in range(self.__n)]
        self.__fs = fs
        self.__pass = 0
        self.__verif = 0
        self.__end = 0
        self.__abandon = 0
        self.__noirsCaptures = 0
        self.__blancsCaptures = 0
        self.__ia = ia
        self.__joueia = 0

        self.__pc1 = ["", "", "", ""]
        self.__pc2 = ["", "", "", ""]
        self.__ncoups1 = 0
        self.__ncoups2 = 0
        self.__k = 0

        self.__goban = pygame.image.load("Interface graphique/Goban 9x9.png").convert()
        self.__goban = pygame.transform.scale(self.__goban, (self.__tailleGoban, self.__tailleGoban))

        self.__pblanc = pygame.image.load("Interface graphique/pionBlanc.png").convert()
        self.__pblanc = pygame.transform.scale(self.__pblanc, (self.__caseTaille, self.__caseTaille))
        self.__pblanc.set_colorkey((0, 0, 0))

        self.__pnoir = pygame.image.load("Interface graphique/pionNoir.png").convert()
        self.__pnoir = pygame.transform.scale(self.__pnoir, (self.__caseTaille, self.__caseTaille))
        self.__pnoir.set_colorkey((255, 255, 255))

        self.__modif1 = 0
        self.__modif2 = 0

        self.__boutonMenu = Bouton(self.get_width()/10, self.get_height()/20, self.get_width()/80, self.get_height()/40, self.get_screen(), "Menu")
        self.__boutonOptions = Bouton(self.get_width()/20, self.get_height()/20, self.get_width()/80, 17*self.get_height()/200, self.get_screen(), "Options")
        self.__boutonQuitter = Bouton(self.get_width()/10, self.get_height()/20, self.get_width()/80, 37*self.get_height()/40, self.get_screen(), "Quitter")
        self.__boutonPasserAvant = Bouton(self.get_width()/10, 3*self.get_height()/40, 11*self.get_width()/80, 97*self.get_height()/120, self.get_screen(), "<<<")
        self.__boutonAvant = Bouton(self.get_width()/10, 3*self.get_height()/40, 21*self.get_width()/80, 97*self.get_height()/120, self.get_screen(), "<")
        self.__boutonApres = Bouton(self.get_width()/10, 3*self.get_height()/40, 31*self.get_width()/80, 97*self.get_height()/120, self.get_screen(), ">")
        self.__boutonPasserApres = Bouton(self.get_width()/10, 3*self.get_height()/40, 41*self.get_width()/80, 97*self.get_height()/120, self.get_screen(), ">>>")
        self.__boutonAnnuler = Bouton(self.get_width()/10, 3*self.get_height()/40, 11*self.get_width()/80, 108*self.get_height()/120, self.get_screen(), "Rejouer")
        self.__boutonPasser = Bouton(self.get_width()/10, 3*self.get_height()/40, 21*self.get_width()/80, 108*self.get_height()/120, self.get_screen(), "Passer")
        self.__boutonAbandon = Bouton(self.get_width()/10, 3*self.get_height()/40, 31*self.get_width()/80, 108*self.get_height()/120, self.get_screen(), "Abandon")
        #self.__boutonRetourBug = Bouton(self.get_width()/10, 3*self.get_height()/40, 41*self.get_width()/80, 108*self.get_height()/120, self.get_screen(), "...")
        self.__joueur1 = ZoneDeTexte(3*self.get_width()/20, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/8, self.get_screen(), ["Joueur 1", "Captures: " + str(self.__blancsCaptures)])
        self.__joueur2 = ZoneDeTexte(3*self.get_width()/20, 9*self.get_height()/40, 33*self.get_width()/40, self.get_height()/8, self.get_screen(), ["Joueur 2", "Captures: " + str(self.__noirsCaptures), "+7,5"])
        self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), [])
        #self.__chat = ZoneDeTexte(13*self.get_width()/40, 7*self.get_height()/20, 13*self.get_width()/20, 21*self.get_height()/40, self.get_screen(), ["Chat"])
        #self.__boiteTexte = Chat(13*self.get_width()/40, 3*self.get_height()/40, 13*self.get_width()/20, 35*self.get_height()/40)
        self.__demande_verif = ZoneDeTexte(self.__tailleGoban, 3*self.get_height()/40, 30*self.get_width()/80 - self.__tailleGoban/2, 97*self.get_height()/120, self.get_screen(), ["Acceptez-vous les pierres mortes ?"])
        self.__boutonOui = Bouton(self.get_width()/10, 3*self.get_height()/40, 21*self.get_width()/80, 108*self.get_height()/120, self.get_screen(), "Oui")
        self.__boutonNon = Bouton(self.get_width()/10, 3*self.get_height()/40, 31*self.get_width()/80, 108*self.get_height()/120, self.get_screen(), "Non")
        self.__boutonRecommencer = Bouton(2*self.get_width()/10, 3*self.get_height()/40, 22*self.get_width()/80, 108*self.get_height()/120, self.get_screen(), "Refaire une partie")

        self.__boutons1 = [self.__boutonMenu, 
                          self.__boutonOptions,
                          self.__boutonQuitter,
                          self.__boutonAnnuler,
                          self.__boutonApres,
                          self.__boutonPasserApres,
                          self.__boutonPasser,
                          self.__boutonAbandon,
                          #self.__boutonRetourBug
                          ]
        
        self.__boutons2 = [self.__boutonMenu, 
                          self.__boutonOptions,
                          self.__boutonQuitter,
                          self.__boutonPasserAvant,
                          self.__boutonAvant,
                          self.__boutonApres,
                          self.__boutonPasserApres,
                          self.__boutonPasser,
                          self.__boutonAbandon,
                          #self.__boutonRetourBug
                          ]
        
        self.__boutons = [self.__boutonMenu, 
                          self.__boutonOptions,
                          self.__boutonQuitter,
                          self.__boutonAnnuler,
                          self.__boutonPasserAvant,
                          self.__boutonAvant,
                          self.__boutonApres,
                          self.__boutonPasserApres,
                          self.__boutonPasser,
                          self.__boutonAbandon,
                          #self.__boutonRetourBug
                          ]
        
        while self.get_b():
            x, y = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.__end or self.__abandon:
                        if self.__boutonRecommencer.mouseOn():
                            self.set_b(0)
                            plateau = Plateau(Board(9), self.__fs, self.__ia) 
                    if self.__boutonMenu.mouseOn():
                                self.set_b(0)
                                self.__pass = 0
                                from page_menu import Menu
                                menu = Menu(self.__fs)
                    if self.__boutonQuitter.mouseOn():
                        sys.exit()
                    if self.__boutonOptions.mouseOn():
                        self.set_b(0)
                        self.__pass = 0
                        from page_options import Options
                        if self.__ia == 0:
                            options = Options(0, self.__fs)
                        else:
                            options = Options(3, self.__fs)
                    if self.__verif:
                        for i in range(self.__n):
                            for j in range(self.__n):
                                if (x > self.__xp - self.__ex + i*self.__caseTaille) and (x < self.__xp + self.__ex + i*self.__caseTaille) and (y > self.__yp - self.__ey + j*self.__caseTaille) and (y < self.__yp + self.__ey + j*self.__caseTaille):
                                    if self.__dead_stones[i][j] != 0:
                                        c = 0
                                        if self.__dead_stones[i][j] == -1:
                                            c = 1
                                        self.__board.play_move((i,j), c)
                                        self.__dead_stones[i][j] = 0    
                        if self.__boutonNon.mouseOn():
                            self.__verif = 0
                        if self.__boutonOui.mouseOn():
                            self.__end = 1
                            s1, s2 = self.__board.end_game()
                            if s1 > s2:
                                message = "Le joueur 1 gagne avec " + str(s1) + " points contre " + str(s2) + " points"
                            else:
                                message = "Le joueur 2 gagne avec " + str(s2) + " points contre " + str(s1) + " points"
                            self.__messageFin = ZoneDeTexte(self.__tailleGoban, 3*self.get_height()/40, 30*self.get_width()/80 - self.__tailleGoban/2, 97*self.get_height()/120, self.get_screen(), [message])
                    else: 
                        if self.__modif2 == 0:
                            if self.__boutonPasser.mouseOn():
                                if self.__ia == 1:
                                    self.__board.list_presumed_dead_stones()
                                    self.__dead_stones = self.__board.list_presumed_dead_stones()
                                    self.__verif = 1
                                else:
                                    self.__board.pass_move()
                                    self.__pass += 1
                                    if self.__pass == 2:
                                        self.__pass = 0
                                        self.__board.list_presumed_dead_stones()
                                        self.__dead_stones = self.__board.list_presumed_dead_stones()
                                        self.__verif = 1
                        if self.__boutonAnnuler.mouseOn():
                            if self.__ia == 1:
                                if self.__modif2 == 0:
                                    self.__modif1 = 1

                                    for i in range(2):
                                        self.__board.cancel_move()
                                        if self.__ncoups2 != 0:
                                            self.__ncoups2 -= 1
                                        self.__k = self.__ncoups2 // 6
                                        if self.__pc2[0] != "":
                                            if self.__pc2[self.__k] != "":
                                                self.__pc2[self.__k] = self.__pc2[self.__k][:-3]
                                            elif self.__pc2[self.__k] == 0 and self.__k != 0:
                                                self.__pc2[self.__k-1] = self.__pc2[self.__k-1][:-3]
                                            if self.__k > 2:
                                                self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), self.__pc2[self.__k-3:self.__k+1])
                                            else:
                                                self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), self.__pc2)

                                            self.__coupsJoues.set_size((int(117*self.get_width()/400), int(9*self.get_height()/200)))
                                            self.__coupsJoues.set_textLength(int(27*self.get_height()/400))
                            else:
                                if self.__board.get_last_moves() and self.__board.get_last_moves()[-1] != "passe":
                                    self.__k = self.__ncoups2 // 6
                                    if self.__pc2[0] != "":
                                        if self.__pc2[self.__k] != "":
                                            self.__pc2[self.__k] = self.__pc2[self.__k][:-3]
                                        elif self.__pc2[self.__k] == 0 and self.__k != 0:
                                            self.__pc2[self.__k-1] = self.__pc2[self.__k-1][:-3]
                                        if self.__k > 2:
                                            self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), self.__pc2[self.__k-3:self.__k+1])
                                        else:
                                            self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), self.__pc2)

                                        self.__coupsJoues.set_size((int(117*self.get_width()/400), int(9*self.get_height()/200)))
                                        self.__coupsJoues.set_textLength(int(27*self.get_height()/400))
                                if self.__pass != 0:
                                    self.__pass -= 1
                                if self.__modif2 == 0:
                                    self.__modif1 = 1
                                    self.__board.cancel_move()
                                    if self.__ncoups2 != 0:
                                        self.__ncoups2 -= 1
                        if self.__boutonAvant.mouseOn():
                            if self.__modif1 == 0:
                                self.__modif2 = 1
                                self.__board.show_last_move()
                        if self.__boutonApres.mouseOn():
                            if self.__modif2 == 1:
                                self.__board.show_next_move()
                            elif self.__modif1 == 1:
                                self.__board.restore_move()
                                self.__k = self.__ncoups2 // 6
                                if self.__pc2[self.__k] == "":
                                    self.__pc2[self.__k] = self.__pc1[self.__k][:2]
                                else:
                                    self.__pc2[self.__k] = self.__pc1[self.__k][:len(self.__pc2[self.__k])+3]
                                if self.__k > 3:
                                    self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), self.__pc2[self.__k-3:self.__k+1])
                                else:
                                    self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), self.__pc2)

                                self.__playedColors = [i[1] for i in self.__playedMoves]
                                self.__coupsJoues.set_size((int(117*self.get_width()/400), int(9*self.get_height()/200)))
                                self.__coupsJoues.set_textLength(int(27*self.get_height()/400))
                                self.__ncoups2 += 1

                                if self.__ia == 1:
                                    self.__board.restore_move()
                                    self.__k = self.__ncoups2 // 6
                                    if self.__pc2[self.__k] == "":
                                        self.__pc2[self.__k] = self.__pc1[self.__k][:2]
                                    else:
                                        self.__pc2[self.__k] = self.__pc1[self.__k][:len(self.__pc2[self.__k])+3]
                                    if self.__k > 3:
                                        self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), self.__pc2[self.__k-3:self.__k+1])
                                    else:
                                        self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), self.__pc2)

                                    self.__playedColors = [i[1] for i in self.__playedMoves]
                                    self.__coupsJoues.set_size((int(117*self.get_width()/400), int(9*self.get_height()/200)))
                                    self.__coupsJoues.set_textLength(int(27*self.get_height()/400))
                                    self.__ncoups2 += 1

                            if self.__board.get_live():
                                self.__modif1 = 0
                                self.__modif2 = 0
                        if self.__boutonPasserAvant.mouseOn():
                            if self.__modif1 == 0:
                                self.__modif2 = 1
                                self.__board.show_start_pos()
                        if self.__boutonPasserApres.mouseOn():
                            self.__board.show_live_pos()
                            self.__modif1 = 0
                            self.__modif2 = 0
                            self.__pc2 = self.__pc1.copy()
                            self.__ncoups2 = self.__ncoups1
                            self.__k = self.__ncoups2 // 6
                            if self.__k > 3:
                                self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), self.__pc2[self.__k-3:self.__k+1])
                            else:
                                self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), self.__pc2)

                            self.__playedColors = [i[1] for i in self.__playedMoves]
                            self.__coupsJoues.set_size((int(117*self.get_width()/400), int(9*self.get_height()/200)))
                            self.__coupsJoues.set_textLength(int(27*self.get_height()/400))
                        if self.__boutonAbandon.mouseOn():
                            self.__abandon = 1
                            tour = self.__board.get_turn()
                            if tour == 0:
                                tour = 2
                            else:
                                tour = 1
                            self.__messageAbandon = ZoneDeTexte(self.__tailleGoban, 3*self.get_height()/40, 30*self.get_width()/80 - self.__tailleGoban/2, 97*self.get_height()/120, self.get_screen(), ["Le joueur " + str(tour) + " gagne par abandon"])

                        #self.__boiteTexte.handle_event(event)
                if not (self.__verif or self.__abandon):
                    if event.type == pygame.MOUSEBUTTONUP:
                        for i in range(self.__n):
                            for j in range(self.__n):
                                if (x > self.__xp - self.__ex + i*self.__caseTaille) and (x < self.__xp + self.__ex + i*self.__caseTaille) and (y > self.__yp - self.__ey + j*self.__caseTaille) and (y < self.__yp + self.__ey + j*self.__caseTaille):
                                    if self.__board.is_a_valid_move((i,j), self.__board.get_turn(), 1)[0] and self.__modif2 == 0:
                                        self.__pass = 0
                                        self.__couleurs[i][j] = self.__board.get_turn()
                                        self.__board.play_move((i,j), self.__board.get_turn())
                                        self.__modif1 = 0   

                                        self.__k = self.__ncoups2 // 6
                                        if self.__k > 3:
                                            if self.__ncoups2 % 6 == 0:
                                                self.__pc2.append("")
                                        self.__playedMoves = self.__board.get_list_played_moves()
                                        self.__playedCoords = [(chr(65 + i[0][0]) + str(9-i[0][1])) for i in self.__playedMoves]
                                        if self.__pc2[self.__k] == "":
                                            self.__pc2[self.__k] = self.__playedCoords[-1]
                                        else:
                                            self.__pc2[self.__k] = self.__pc2[self.__k] + " " + self.__playedCoords[-1]
                                        if self.__k > 3:
                                            self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), self.__pc2[self.__k-3:self.__k+1])
                                        else:
                                            self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), self.__pc2)

                                        self.__playedColors = [i[1] for i in self.__playedMoves]
                                        self.__coupsJoues.set_size((int(117*self.get_width()/400), int(9*self.get_height()/200)))
                                        self.__coupsJoues.set_textLength(int(27*self.get_height()/400))
                                        self.__ncoups2 += 1
                                        self.__ncoups1 = self.__ncoups2
                                        self.__pc1 = self.__pc2.copy()

                                        if self.__ia == 1:
                                            self.__joueia = 1

            self.affiche_bg()
            self.get_screen().blit(self.__goban, (30*self.get_width()/80 - self.__tailleGoban/2,self.get_height()/20))

            if self.__board.get_len_white_captured() != self.__blancsCaptures:
                self.__blancsCaptures = self.__board.get_len_white_captured()
                self.__joueur1 = ZoneDeTexte(3*self.get_width()/20, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/8, self.get_screen(), ["Joueur 1", "Captures: " + str(self.__blancsCaptures)])
            if self.__board.get_len_black_captured() != self.__noirsCaptures:
                self.__noirsCaptures = self.__board.get_len_black_captured()
                self.__joueur2 = ZoneDeTexte(3*self.get_width()/20, 9*self.get_height()/40, 33*self.get_width()/40, self.get_height()/8, self.get_screen(), ["Joueur 2", "Captures: " + str(self.__noirsCaptures), "+7,5"])

            self.set_boutons(self.__boutons)
            
            if not (self.__verif or self.__abandon):
                for i in range(self.__n):
                    for j in range(self.__n):
                        if (x > self.__xp - self.__ex + i*self.__caseTaille) and (x < self.__xp + self.__ex + i*self.__caseTaille) and (y > self.__yp - self.__ey + j*self.__caseTaille) and (y < self.__yp + self.__ey + j*self.__caseTaille):
                            if self.__board.is_a_valid_move((i,j), self.__board.get_turn(), 0)[0] and self.__board.get_allow():
                                self.set_mouseClick(True)

            if self.__verif:
                for i in range(self.__n):
                    for j in range(self.__n):
                        if (x > self.__xp - self.__ex + i*self.__caseTaille) and (x < self.__xp + self.__ex + i*self.__caseTaille) and (y > self.__yp - self.__ey + j*self.__caseTaille) and (y < self.__yp + self.__ey + j*self.__caseTaille):
                            if self.__dead_stones[i][j] != 0:
                                self.set_mouseClick(True)
            
            if self.__modif1 == 1:
                self.set_boutons(self.__boutons1)
            elif self.__modif2 == 1:
                self.set_boutons(self.__boutons2)
            else:
                self.set_boutons(self.__boutons)

            self.set_zdt([self.__joueur1,
                      self.__joueur2,
                      self.__coupsJoues,
                      #self.__chat
                      ])
                
            for i in range(self.__n):
                for j in range(self.__n):
                    if not(self.__mat[i][j].get_stone() is None):
                        if self.__couleurs[i][j] == 0:
                            self.draw_circle(self.get_screen(), int(self.__xp + i*self.__caseTaille), int(self.__yp + j*self.__caseTaille), int(self.__caseTaille/2), (0,0,0))
                            #self.get_screen().blit(self.__pnoir,(self.__xp + i*self.__caseTaille - self.__caseTaille/2, self.__yp + j*self.__caseTaille - self.__caseTaille/2))
                        elif self.__couleurs[i][j] == 1:
                            self.draw_circle(self.get_screen(), int(self.__xp + i*self.__caseTaille), int(self.__yp + j*self.__caseTaille), int(self.__caseTaille/2), (255,255,255))
                            #self.get_screen().blit(self.__pblanc,(self.__xp + i*self.__caseTaille - self.__caseTaille/2, self.__yp + j*self.__caseTaille - self.__caseTaille/2))
                    if self.__verif:
                        if self.__dead_stones[i][j] == 1:
                            self.draw_circle(self.get_screen(), int(self.__xp + i*self.__caseTaille), int(self.__yp + j*self.__caseTaille), int(self.__caseTaille/2), (255,0,0))
                        elif self.__dead_stones[i][j] == -1:
                            self.draw_circle(self.get_screen(), int(self.__xp + i*self.__caseTaille), int(self.__yp + j*self.__caseTaille), int(self.__caseTaille/2), (0,255,0))

            #print(#self.__boiteTexte.font.size(#self.__boiteTexte.txt_surface))
                #self.__boiteTexte.draw(self.get_screen())

            if self.__abandon:
                self.set_boutons([self.__boutonMenu, 
                                  self.__boutonOptions,
                                  self.__boutonQuitter,
                                  self.__boutonRecommencer])
                
                self.set_zdt([self.__joueur1,
                              self.__joueur2,
                              self.__coupsJoues,
                              #self.__chat, 
                              self.__messageAbandon])

            if self.__verif: 
                self.set_boutons([self.__boutonMenu, 
                          self.__boutonOptions,
                          self.__boutonQuitter,
                          self.__boutonOui,
                          self.__boutonNon])
                self.set_zdt([self.__joueur1,
                      self.__joueur2,
                      self.__coupsJoues,
                      #self.__chat, 
                      self.__demande_verif])
                
            if self.__end:
                 self.set_boutons([self.__boutonMenu, 
                          self.__boutonOptions,
                          self.__boutonQuitter,
                          self.__boutonRecommencer])
                 self.set_zdt([self.__joueur1,
                      self.__joueur2,
                      self.__coupsJoues,
                      #self.__chat, 
                      self.__messageFin])


            """if self.__end:
                scores = self.__board.end_game()
                if scores[0] > scores[1]:
                    gagnant = "Joueur 1"
                    score = (scores[0], scores[1])
                else: 
                    gagnant = "Joueur 2"
                    score = (scores[1], scores[0])
                self.__findujeu = ZoneDeTexte(self.get_width()/2, self.get_height()/2, self.get_width()/4, self.get_height()/4, self.get_screen(), ["Le " + gagnant + " a gagné avec " + str(score[0]) + " points contre " + str(score[1])])
                self.__findujeu.afficher()"""
            
            self.styleBoutons()
            self.affiche()
            pygame.display.update()

            if self.__joueia:
                k,l = pvs(-float('inf'), float('inf'), 1, serialize_board(self.__board), 1, parallel=True)[1]
                self.__couleurs[k][l] = self.__board.get_turn()
                self.__board.play_move((k,l), self.__board.get_turn())
                self.__k = self.__ncoups2 // 6
                if self.__k > 3:
                    if self.__ncoups2 % 6 == 0:
                        self.__pc2.append("")
                self.__playedMoves = self.__board.get_list_played_moves()
                self.__playedCoords = [(chr(65 + i[0][0]) + str(9-i[0][1])) for i in self.__playedMoves]
                if self.__pc2[self.__k] == "":
                    self.__pc2[self.__k] = self.__playedCoords[-1]
                else:
                    self.__pc2[self.__k] = self.__pc2[self.__k] + " " + self.__playedCoords[-1]
                if self.__k > 3:
                    self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), self.__pc2[self.__k-3:self.__k+1])
                else:
                    self.__coupsJoues = ZoneDeTexte(13*self.get_width()/40, 9*self.get_height()/40, 13*self.get_width()/20, self.get_height()/2, self.get_screen(), self.__pc2)

                self.__playedColors = [i[1] for i in self.__playedMoves]
                self.__coupsJoues.set_size((int(117*self.get_width()/400), int(9*self.get_height()/200)))
                self.__coupsJoues.set_textLength(int(27*self.get_height()/400))
                self.__ncoups2 += 1
                self.__ncoups1 = self.__ncoups2
                self.__pc1 = self.__pc2.copy()
                self.__joueia = 0 
    
    def draw_circle(self, surface, x, y, radius, color):
        gfxdraw.aacircle(surface, x, y, radius, color)
        gfxdraw.filled_circle(surface, x, y, radius, color)

if __name__ == "__main__":
    plateau = Plateau(Board(9), 0, 0)