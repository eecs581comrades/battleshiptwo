#TODO create a way to enter ships for each board. Grid coordinates should be marked. Error checking 
#needs to be implemented for ship placement(Can't place a ship on top of another and a ship can't cross the game border)
class Board:
    def __init__(self, numShips):
        self.size = 10
        self.numShips = numShips
        self.col = []
        self.row = []
    #Build an empty board based on the size of the board
    def buildBoard(self):
        #Consider changing to a nested list with grid=[rows[cols]]
        for i in range(self.size):
            self.row.append(0)
            self.col.append(0)

    def showBoard(self):
        #TODO Create a prettier way of displaying the game board. 
        #Perhaps include a grid pattern or a small window application using pygame
        for i in range(len(self.row)):
            print("\n")
            for j in range(len(self.col)):
                print("0", end=' ')
