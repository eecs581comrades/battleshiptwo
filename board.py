class Board:
    def __init__(self, numShips): #init changes to the way the grid is setup and the hits to calculate endgame.
        self.size = 10
        self.numShips = numShips
        self.grid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.hits = 0

    def buildBoard(self): #Not needed anymore
        pass
    
    def ship_placement(self, let_to_num): #New setup for ship placement to use horizontal or vertical. Also incorporates what was previously in buildBoard. Tried to make output look cleaner.
        ship_num = 1
        for i in range(self.numShips):
            print(f"**** Ship #{ship_num} (1 x {ship_num}) ****")
            while True:
                try:
                    row_num = int(input("Enter row number (1-10): ")) - 1 #Row and column
                    column_letter = input("Enter column letter (A-J): ").upper()
                    column_number = let_to_num.get(column_letter, -1)
                    if column_number == -1 or row_num < 0 or row_num >= self.size: #Validity checks
                        print("Invalid row/column. Try again.")
                        continue 
                    orientation = input("Enter orientation (H for Horizontal, V for Vertical): ").upper() #Direction
                    
                    if orientation == 'H': #Ship setup checks
                        if column_number + ship_num > self.size:
                            print("Ship does not fit horizontally. Try again.")
                            continue
                        if any(self.grid[row_num][column_number + j] != '.' for j in range(ship_num)):
                            print("Ships cannot overlap. Try again.")
                            continue

                        for j in range(ship_num): #Placement
                            self.grid[row_num][column_number + j] = 'S'

                    elif orientation == 'V': #Ship setup checks
                        if row_num + ship_num > self.size:
                            print("Ship does not fit vertically. Try again.")
                            continue
                        if any(self.grid[row_num + j][column_number] != '.' for j in range(ship_num)):
                            print("Ships cannot overlap. Try again.")
                            continue

                        for j in range(ship_num): #Placement
                            self.grid[row_num + j][column_number] = 'S'
                    else:
                        print("Invalid orientation. Please enter H or V.")
                        continue
                    
                    break

                except ValueError:
                    print("Invalid input. Please try again.")
            
            self.showBoard()  #Show the new board
            ship_num += 1

    def showBoard(self): #Small showBoard updates to make it look nicer
        print("\n**** Board ****")
        print("  A B C D E F G H I J")
        for idx, row in enumerate(self.grid):
            display_row = [str(cell) for cell in row]
            print(f"{idx + 1:2} " + " ".join(display_row))

    def take_shot(self, row, col): #Updates the board for hits and misses
        if self.grid[row][col] == 'S': #Ships
            print("Hit!")
            self.grid[row][col] = 'H' #Hits
            self.hits += 1
        elif self.grid[row][col] == '.': #Empty
            print("Miss!")
            self.grid[row][col] = 'M'  #Misses
        else:
            print("Already targeted this spot. Try again.")

    def has_lost(self): #Endgame check
        total_ship_cells = sum(range(1, self.numShips + 1))
        return self.hits == total_ship_cells