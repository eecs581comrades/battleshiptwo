class Board:
    def __init__(self, numShips):
        self.size = 10
        self.numShips = numShips
        self.grid = list()
        for i in range(self.size):
            self.grid.append(list())

    def buildBoard(self):
        for row in self.grid:
            for i in range(self.size):
                row.append(0)
    
    def ship_placement(self):
        ship_num = 1
        for i in range(self.numShips):
            print("****Ship #", ship_num, " ( 1 x", ship_num, ")****")
            print("\n")
            if ship_num >= 2:
                print("Must enter adjacent tiles for each ship. Do not repeat tiles.")
            row_num = int(input("Enter row number for ship:"))
            column_letter = input("Enter a column letter:")
            print("\n")
            column_letter = column_letter.upper()


            if column_letter == 'A':
                column_letter = 1
            elif column_letter == 'B':
                column_letter = 2
            elif column_letter == 'C':
                column_letter = 3
            elif column_letter == 'D':
                column_letter = 4
            elif column_letter == 'E':
                column_letter = 5
            elif column_letter == 'F':
                column_letter = 6
            elif column_letter == 'G':
                column_letter = 7
            elif column_letter == 'H':
                column_letter = 8
            elif column_letter == 'I':
                column_letter = 9
            elif column_letter == 'J':
                column_letter = 10


            row_num -= 1
            column_letter -= 1
            self.grid[row_num][column_letter] = 1
            ship_num += 1



    def showBoard(self):
        print("\n")
        print("****Board****")
        for row in self.grid:
            print(row)

