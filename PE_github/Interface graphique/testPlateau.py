import sys, pygame
from pygame.locals import *
pygame.init()

size = (480, 480)

screen = pygame.display.set_mode(size)

goban = pygame.image.load("Goban 9x9.png").convert() #quoicoubeh
goban = pygame.transform.scale(goban, size)

taillePion = 50
dimPion = (taillePion, taillePion)
pionB = pygame.image.load("pionBlanc.png").convert()
pionB = pygame.transform.scale(pionB, dimPion)
pionB.set_colorkey((0, 0, 0))
pionN = pygame.image.load("pionNoir.png").convert()
pionN = pygame.transform.scale(pionN, dimPion)
pionN.set_colorkey((255, 255, 255))

tour = 1

dim = (12, 9)
tailleCase = 57
plateau = [[(dim[0] + i*tailleCase, dim[0] + j*tailleCase)  for i in range(dim[1])] for j in range(dim[1])]
cases = [[0 for i in range(dim[1])] for i in range(dim[1])]
etats = [cases.copy()]

screen.blit(goban, (0,0))

while 1:

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for i in range(dim[1]):
                for j in range(dim[1]):
                    if pos[0] <= plateau[i][j][0] + taillePion//5 and pos[0] >= plateau[i][j][0] - taillePion//5 and pos[1] <= plateau[i][j][1] + taillePion//5 and pos[1] >= plateau[i][j][1] - taillePion//5:
                        if cases[i][j] == 0:
                            cases[i][j] = tour
                            etats.append(cases.copy())
                            if tour == 1:
                                screen.blit(pionN, (plateau[i][j][0] - taillePion//2, plateau[i][j][1] - taillePion//2))
                            else:
                                screen.blit(pionB, (plateau[i][j][0] - taillePion//2, plateau[i][j][1] - taillePion//2))
                            tour = -1*tour
                            
    pygame.display.update()