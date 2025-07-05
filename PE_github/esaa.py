class jeugo:
    a = int(input("la taille du plateau"))
    def __init__(self, size=a):
        self.size = size
        self.board = []
        for i in range(size):
            row = [0]*size
            self.board.append(row)
        print(self.board)
    def planche(self):
        for row in self.board:
            print(" ".join(map(str, row)))
    def place_pierre(self, row, col, player):
        self.board[row][col] = player

game = jeugo()

game.place_pierre(1,7,1)
game.planche()