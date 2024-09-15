class Board:
    def __init__(self, numShips): #init changes to the way the grid is setup and the hits to calculate endgame.
        self.size = 10
        self.numShips = numShips
        self.grid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.hits = 0
        self.placements = {} # Stores user ship placements to track existing ships

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

            self.storeShipLocation(row_num, column_number, ship_num, orientation) # stores ship location for hitShip() function
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
            self.hitShip(row, col) # updates the health of the ship that was hit and if ship health is zero announces it
        elif self.grid[row][col] == '.': #Empty
            print("Miss!")
            self.grid[row][col] = 'M'  #Misses
        else:
            print("Already targeted this spot. Try again.")

    def has_lost(self): #Endgame check
        total_ship_cells = sum(range(1, self.numShips + 1))
        return self.hits == total_ship_cells

    # This function authored by Team Member: Daniel Bobadilla & ChatGPT
    def storeShipLocation(self, row, col, ship_num, orientation): # Stores the location of the ships
        # Stores the ship coordinates, ship health, and the orientation of the ship in a nested dictionary for hitShip checking
        self.placements[ship_num] = { # Key is dependent on which ship number it is (e.g., ship 1 is defined on canvas as a 1x1 and so on)
            'Ship Coordinates': (row, col),
            'Ship Length': ship_num,
            'Ship Health': ship_num,
            'Ship Orientation': orientation
        }

    # This function is authored by Team Member: Daniel Bobadilla & ChatGPT
    def hitShip(self, row, col): # Helper function that tracks ship health and whether it has sunk or not
        for ship_num, ship_data in self.placements.items(): # Iterates keys and items in class stored ship locations
            ship_coordinates = self.get_ship_coordinates(ship_num) # Stores a list of coordinates for a single ship
            if (row, col) in ship_coordinates: # checks if the shot from the opponent matches any of the coordinates from the ships coordinates
                ship_data['Ship Health'] -= 1 # If there is a match it reduces the ships health by 1
                if ship_data['Ship Health'] == 0: # If statement checks if the ship no longer has any health
                    print(f"Ship has sunk!") # If the ship has zero health announces that the ship has sunk
                return
    
    # This function is authored by Team Member: Daniel Bobadilla & ChatGPT
    def get_ship_coordinates(self, ship_num): # Helper function for hitShip() to provide full coordinates for a single ship
        ship = self.placements[ship_num] # Stores the specific ship information in variable "ship"
        start_row, start_col = ship['Ship Coordinates'] # Stores where the ship coordinates start
        length = ship['Ship Length'] # stores the length of the ship
        orientation = ship['Ship Orientation'] # stores the ships orientation

        coordinates = [] # Defines an empty list to hold ship coordinates

        # For loop with if else blocks is meant to iterate through a set of coordinates based on the start point of the ship, ship length, and ship orientation
        # Stores each coordinate in the "coordinates" list for hitShip() function to use
        for i in range(length):
            if orientation == 'H':
                coordinates.append((start_row, start_col + i))
            elif orientation == 'V':
                coordinates.append((start_row + i, start_col))
        return coordinates

