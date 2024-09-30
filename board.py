#Battleship Board File
#This file contains the board game initialization, hit mechanics, and board displays for the game battleship
#No inputs or outputs
#Proj 1 Authors: Aiden Murphy, Jack Doughty, Jack Pigott, Vy Luu, Daniel Bobadilla
#Proj 2 Authors: Chase Curtis, Emily Tso, Katie Golder, Matthew Petillo, Wil Johnson
#Proj 1 Supplemental help from ChatGPT and StackOverflow
#Creation Date: 09-13-2024
#Project 2 Team Takeover: 09-18-2024

from colorama import Fore, Back, Style, init
import os
import random

def clearScreen():#resets the terminal display
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
    return


class Board:
    def __init__(self, numShips):  #Sets up the grid, and stores hits. Also updates ship placements
        init(autoreset=True)
        self.size = 10
        self.numShips = numShips
        self.grid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.shotGrid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.hits = 0
        self.placements = {}  #Stores user ship placements to track existing ships\
        self.cpuNextShot = None #Stores the CPU's next shot
        self.cpuLastShot = None #Stores CPU's previous attempt(In case of a hit")
        self.cpuShotHit = None #Stores the hit from CPU
        self.cpuTry = 0 #Stores CPU's attempt at shooting after hit
        self.cpuHit = False #Stores if CPU hit player in previous shot

    def showBoard(self):
        """Prints the board with emojis and colored backgrounds for different states."""
        print(Style.BRIGHT + '    ' + '   '.join([Fore.YELLOW + chr(65 + i) for i in range(self.size)]))  # Column headers
        for idx, row in enumerate(self.grid):
            print(Fore.YELLOW + f"{idx+1:<2} ", end='')  # Row numbers with proper alignment
            for cell in row:
                if cell == 'S':  # Assuming 'S' represents a ship
                    print(Back.BLACK + '⬛', end='  ')  # BLACK emoji for ships
                elif cell == 'H':  # Assuming 'H' represents a hit
                    print(Back.YELLOW + '🟨', end='  ')  # Yellow emoji for hits
                elif cell == 'D':
                    print(Back.RED + '🟥', end='  ') # RED emoji for dead ship
                elif cell == '.':
                    print(Back.BLUE + '🟦', end='  ')  # BLUE emoji for water/empty
                else:
                    print(Back.WHITE + '⬜', end='  ')  # White square for misses
            print()  # Newline for the next row


    def showShotBoard(self):
        """Prints the shot board with emojis and colored backgrounds for different states."""
        print(Style.BRIGHT + '    ' + '   '.join([Fore.YELLOW + chr(65 + i) for i in range(self.size)]))  # Column headers
        for idx, row in enumerate(self.shotGrid):
            print(Fore.YELLOW + f"{idx+1:<2} ", end='')  # Row numbers with proper alignment
            for cell in row:
                if cell == 'H':  # Assuming 'H' represents a hit
                    print(Back.YELLOW + '🟨', end='  ')  # Red emoji for hits
                elif cell == 'D':
                    print(Back.RED + '🟥', end='  ')
                elif cell == '.':
                    print(Back.BLUE + '🟦', end='  ')  # BLUE emoji for water/empty
                else:
                    print(Back.WHITE + '⬜', end='  ')  # White square for misses
            print()  # Newline for the next row

    #Ship_Placement establishes the board and ship placement, while error checking for validity in placement
    def ship_placement(self, let_to_num):
        ship_num = 1
        for i in range(self.numShips): #Depending on how many ships
            print(f"**** Ship #{ship_num} (1 x {ship_num}) ****") #Output for each ship
            while True:
                try:
                    row_num = int(input("Enter row number (1-10): ")) - 1 #Row input from user 
                    column_letter = input("Enter column letter (A-J): ").upper() #Column input from user
                    column_number = let_to_num.get(column_letter, -1) #access the dictionary
                    if column_number == -1 or row_num < 0 or row_num >= self.size: #Validity checks
                        print("Invalid row/column. Try again.")
                        continue 
                    orientation = input("Enter orientation (H for Horizontal, V for Vertical): ").upper() #Direction for ship placement
                    
                    if orientation == 'H': #Ship setup checks
                        if column_number + ship_num > self.size: #Size Check
                            print("Ship does not fit horizontally. Try again.")
                            continue
                        if any(self.grid[row_num][column_number + j] != '.' for j in range(ship_num)): #Overlap check
                            print("Ships cannot overlap. Try again.") #Overlap check
                            continue

                        for j in range(ship_num): #Placement of the ship!
                            self.grid[row_num][column_number + j] = 'S'#Placement of the ship!

                    elif orientation == 'V': #Ship setup checks
                        if row_num + ship_num > self.size: #Size Check
                            print("Ship does not fit vertically. Try again.")
                            continue
                        if any(self.grid[row_num + j][column_number] != '.' for j in range(ship_num)): #Overlap check
                            print("Ships cannot overlap. Try again.") #Overlap check
                            continue

                        for j in range(ship_num): #Placement of the ship!
                            self.grid[row_num + j][column_number] = 'S' #Placement of the ship!
                    else:
                        print("Invalid orientation. Please enter H or V.") 
                        continue
                    
                    break

                except ValueError: #Invalid inputs
                    print("Invalid input. Please try again.")

            self.storeShipLocation(row_num, column_number, ship_num, orientation) #Stores ship location for hitShip() function
            clearScreen()
            self.showBoard()  #Show the new board
            ship_num += 1

    def autoPlaceShips(self):#Katie adapted from ship_placement
        # FOR CPU: AUTO PLACE SHIPS
        ship_num = 1
        for i in range(self.numShips): #Depending on how many ships
            #print(f"**** Ship #{ship_num} (1 x {ship_num}) ****") #Output for each ship
            while True:
                try:
                    row_num = random.randint(0,9)
                    #column_letter = input("Enter column letter (A-J): ").upper() #Column input from user
                    column_number = random.randint(0,9)
                    if column_number == -1 or row_num < 0 or row_num >= self.size: #Validity checks
                        print("Invalid row/column. Try again.")
                        continue 
                    #orientation = input("Enter orientation (H for Horizontal, V for Vertical): ").upper() #Direction for ship placement
                    orientation_choice = random.randint(0,1)
                    orientation = "H" if orientation_choice == 0 else "V"
                    
                    if orientation == "H": #Ship setup checks
                        print(row_num)
                        print(column_number)
                        if column_number + ship_num > self.size: #Size Check
                            print("Ship does not fit horizontally. Try again.")
                            continue
                        if any(self.grid[row_num][column_number + j] != '.' for j in range(ship_num)): #Overlap check
                            print("Ships cannot overlap. Try again.") #Overlap check
                            continue

                        for j in range(ship_num): #Placement of the ship!
                            self.grid[row_num][column_number + j] = 'S'#Placement of the ship!

                    elif orientation == "V": #Ship setup checks
                        print(row_num)
                        print(column_number)
                        if row_num + ship_num > self.size: #Size Check
                            print("Ship does not fit vertically. Try again.")
                            continue
                        if any(self.grid[row_num + j][column_number] != '.' for j in range(ship_num)): #Overlap check
                            print("Ships cannot overlap. Try again.") #Overlap check
                            continue

                        for j in range(ship_num): #Placement of the ship!
                            self.grid[row_num + j][column_number] = 'S' #Placement of the ship!
                    else:
                        print("Invalid orientation. Please enter H or V.") 
                        continue
                    
                    break

                except ValueError: #Invalid inputs
                    #print("Invalid input. Please try again.")
                    continue

            self.storeShipLocation(row_num, column_number, ship_num, orientation) #Stores ship location for hitShip() function
            clearScreen()
            self.showBoard()  #Show the new board
            ship_num += 1
        
    def take_shot(self, row, col): #Updates the board for hits and misses
        if self.grid[row][col] == 'S': #Ships
            print("Hit!")
            self.grid[row][col] = 'H' #Hits
            self.shotGrid[row][col] = 'H'
            self.hits += 1
            self.cpuHit = True #CPU hit a spot
            self.hitShip(row, col) #Updates the health of the ship that was hit and if ship health is zero announces it
            return True
        elif self.grid[row][col] == '.': #Empty
            print("Miss!")
            self.grid[row][col] = 'M'
            self.shotGrid[row][col] = 'M'  #Misses
            if self.cpuShotHit != None: #Checks if this was an attempt after a shot was hit by CPU
                self.cpuTry += 1 #Increments by 1 to try another spot by the hit spot
            return False
        else:
            print("Already targeted this spot. Try again.")

    # CPU shot function to collect a shot to be made by the CPU based on player specified difficulty
    def cpuTakeShot(self, dif):
        if (dif == 'easy'): #Easy mode shot for CPU
            while True:
                row = random.randint(0,9) #Takes random row number
                col = random.randint(0,9) #Takes random column number
                if self.shotGrid[row][col] == '.': #Checks if spot was previously shot at
                    return (row, col) #Shoot the shot
                else: #Try again for different shot
                    continue
        elif (dif == 'medium'): #Medium mode shot for CPU
            while True:
                if self.cpuNextShot == None and self.cpuHit == False: #No previous hit or shot
                    shotCheck = False #A temp shot check to check for hits not in a row
                    for i in range(0,9):
                        for j in range(0,9):
                            if self.shotGrid[i][j] == 'H': #checks if spot was hit
                                self.cpuLastShot = (i, j) #Spot was hit, so new spot to shoot around
                                self.cpuHit = True #Claim a shot was hit
                                shotCheck = True #Spot was hit
                    if shotCheck == False: #No previous spots hit that need to be checked
                        self.cpuLastShot = (random.randint(0,9), random.randint(0,9)) #generates random shot
                        if self.shotGrid[self.cpuLastShot[0]][self.cpuLastShot[1]] == '.': #checks if spot was already shot
                            return self.cpuLastShot #shoot the shot
                        else: #try again for a different shot
                            continue
                elif self.cpuNextShot == None and self.cpuHit == True: #the previous shot was a hit or there was a hit that needs checked
                    self.cpuShotHit = self.cpuLastShot #stores last shot attempted as spot that was hit
                    self.cpuHit = False #default the hit for next attempt
                    self.cpuNextShot = (self.cpuLastShot[0] + 1, self.cpuLastShot[1]) #Setup next shot
                    if self.shotGrid[self.cpuNextShot[0]][self.cpuNextShot[1]] == '.' and self.cpuNextShot[0] < 10: #checks if shot is on the board or shot already
                        return self.cpuNextShot #shoot the shot
                    else: #Shot is not on the board or was shot already
                        continue
                elif self.cpuNextShot != None and self.cpuHit == True: #A shot after a first hit on ship was hit
                    #Shot is incremented by 1 in direction of which the shot hit to continue to sink ship
                    if self.cpuTry == 0: 
                        self.cpuNextShot = (self.cpuNextShot[0] + 1, self.cpuNextShot[1])
                    elif self.cpuTry == 1:
                        self.cpuNextShot = (self.cpuNextShot[0] - 1, self.cpuNextShot[1])
                    elif self.cpuTry == 2:
                        self.cpuNextShot = (self.cpuNextShot[0], self.cpuNextShot[1] + 1)
                    else:
                        self.cpuNextShot = (self.cpuNextShot[0], self.cpuNextShot[1] - 1)
                    self.cpuHit = False #default the hit for next attempt
                    if self.shotGrid[self.cpuNextShot[0]][self.cpuNextShot[1]] != 'D' and self.shotGrid[self.cpuNextShot[0]][self.cpuNextShot[1]] != 'M' and self.cpuNextShot[0] < 10 and self.cpuNextShot[1] < 10 and self.cpuNextShot[0] >= 0 and self.cpuNextShot[1] >= 0: #check if shot was missed, sunk, or off the board
                        if self.shotGrid[self.cpuNextShot[0]][self.cpuNextShot[1]] == 'H': #checks if the next shot was a hit to skip over to the next spot available
                            continue
                        else: 
                            return self.cpuNextShot #shoot the shot
                    else: #shot was made or off the board. Increment the cpu.try to shoot a different spot and try again
                        self.cpuTry += 1
                        continue
                elif self.cpuNextShot != None and self.cpuHit == False:
                    if self.cpuTry == 0:
                        self.cpuNextShot = (self.cpuShotHit[0] + 1, self.cpuShotHit[1])
                    elif self.cpuTry == 1:
                        self.cpuNextShot = (self.cpuShotHit[0] - 1, self.cpuShotHit[1])
                    elif self.cpuTry == 2:
                        self.cpuNextShot = (self.cpuShotHit[0], self.cpuShotHit[1] + 1)
                    else:
                        self.cpuNextShot = (self.cpuShotHit[0], self.cpuShotHit[1] - 1)
                    if self.shotGrid[self.cpuNextShot[0]][self.cpuNextShot[1]] != 'D' and self.shotGrid[self.cpuNextShot[0]][self.cpuNextShot[1]] != 'M' and self.cpuNextShot[0] < 10 and self.cpuNextShot[1] < 10 and self.cpuNextShot[0] >= 0 and self.cpuNextShot[1] >= 0: #check if shot was missed, sunk, or off the board
                        if self.shotGrid[self.cpuNextShot[0]][self.cpuNextShot[1]] == 'H': #checks if the next shot was a hit to skip over to the next spot available
                            continue
                        else: 
                            return self.cpuNextShot #shoot the shot
                    else: #shot was made or off the board. Increment the cpu.try to shoot a different spot and try again
                        self.cpuTry += 1
                        continue
        else: #Hard mode shot for CPU
            for ship_num, ship_data in self.placements.items(): # Iterates keys and items in class stored ship locations
                ship_coordinates = self.get_ship_coordinates(ship_num) # Stores a list of coordinates for a single ship
                for (row, col) in ship_coordinates: # checks if the shot from the opponent matches any of the coordinates from the ships coordinates
                    if ship_data['Ship Health'] != 0: # If statement checks if the ship no longer has any health
                        if (self.shotGrid[row][col] == '.'):  
                            return ((row, col))
                        else:
                            print ("try next spot")
                    else:
                        print("error no ships found")
                    
    def has_lost(self): #Endgame check
        total_ship_cells = sum(range(1, self.numShips + 1)) #returns ship cell total
        return self.hits == total_ship_cells #Compares to see if game is over

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
                    for row, col in ship_coordinates:
                        self.grid[row][col] = 'D'
                        self.shotGrid[row][col] = 'D'
                    self.cpuNextShot = None #resets CPU's next shot to default
                    self.cpuLastShot = None #resets CPU's last shot to default
                    if self.cpuShotHit != None: #Checks if the shot hit is None(For the sinking of the 1x1 ship)
                        if self.shotGrid[self.cpuShotHit[0]][self.cpuShotHit[1]] == 'D': #Checks if the original shot that was hit is now sunk
                            self.cpuShotHit = None #Shot was is sunk, so back to default
                            self.cpuTry = 0 #shot attempts reset to default
                    self.cpuHit = False #default the hit for next attempt
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
    
