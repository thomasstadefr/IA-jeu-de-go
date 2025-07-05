import pygame

class Bouton:
    def __init__(self, w, h, x, y, screen, text):
        self.__width = w
        self.__height = h
        self.__x = x
        self.__y = y
        self.__im = pygame.image.load("Interface graphique/bouton.png").convert_alpha()
        self.__im = pygame.transform.scale(self.__im, (self.__width, self.__height))
        self.__screen = screen
        self.__text = text
        self.__textLength = 100
        self.__textColor = (0, 0, 0)
        self.__font = pygame.font.SysFont(None, self.__textLength)
        self.__blitText = self.__font.render(self.__text, True, self.__textColor)
        self.__size = self.__font.size(self.__text)
        
        while self.__size[0] > self.__width - 10 or self.__size[1] > self.__height - 10:
            self.__textLength -= 1
            self.__font = pygame.font.SysFont(None, self.__textLength)
            self.__blitText = self.__font.render(self.__text, True, (0, 0, 0))
            self.__size = self.__font.size(self.__text)

    def afficher(self):
        self.__screen.blit(self.__im, (self.__x, self.__y))
        self.__screen.blit(self.__blitText, (self.__x + self.__width/2 - self.__size[0]/2, self.__y + self.__height/2 - self.__size[1]/2))

    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def get_w(self):
        return self.__width
    
    def get_h(self):
        return self.__height
    
    def mouseOn(self):
        x,y = pygame.mouse.get_pos()
        return (x > self.__x and x < self.__x + self.__width and y > self.__y and y < self.__y + self.__height)
    
    def change_text_color(self, c):
        self.__textColor = c
        self.__blitText = self.__font.render(self.__text, True, self.__textColor)