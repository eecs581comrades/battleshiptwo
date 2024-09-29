#Battleship Main File
#This file contains the main functions and gameplay mechanics for the game battleship. This initializes the game and runs all interactions between players or computer opponent.
#No inputs or outputs
#Proj 1 Authors: Aiden Murphy, Jack Doughty, Jack Pigott, Vy Luu, Daniel Bobadilla
#Proj 2 Authors: Chase Curtis, Emily Tso, Katie Golder, Matthew Petillo, Wil Johnson
#Proj 1 Supplemental help from ChatGPT and StackOverflow
#Creation Date: 09-13-2024
#Project 2 Team Takeover: 09-18-2024

#Import needed libraries
from board import Board, clearScreen
from scripts import explode
import random #Needed for special shots

#Dictionary can be used as a global var to map chars to ints
let_to_num = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}

#Sets limits for firing each special shot 
special_shots_limits = {
    "nuke": 1, 
    "carpet_bomb": 3,
    "air_strike": 3,
    "scatter_shot" : 3
}

#Get_Shot gets the coordinates from each player as a target for their shot
def get_shot():
    while True:
        try:
            #Gets what type of shot the user wants to fire
            special_shot = input(" To use special shots (N for Nuke, C for Carpet Bomb, A for Air Strike, S for Scatter Shot, and any other keys for standard shot): ").upper()

            if special_shot == "N": #Nuke
                if special_shots_limits["nuke"] > 0:#Checks if all special shots have been used
                    special_shots_limits["nuke"] -= 1
                    return nuke()#call firing function
                else:
                    print("All shots used")
            elif special_shot == "C": #Carpet Bomb
                if special_shots_limits["carpet_bomb"] > 0:#Checks if all special shots have been used
                    special_shots_limits["carpet_bomb"] -= 1
                    return carpet_bomb()#call firing function
                else:
                    print("All shots used")
            elif special_shot == "A": #Air Strike
                if special_shots_limits["air_strike"] > 0:#Checks if all special shots have been used
                    special_shots_limits["air_strike"] -= 1
                    return air_strike()#call firing function
                else:
                    print("All shots used")
            elif special_shot == "S": #Air Strike
                if special_shots_limits["scatter_shot"] > 0:#Checks if all special shots have been used
                    special_shots_limits["scatter_shot"] -= 1
                    return scatter_shot()#call firing function
                else:
                    print("All shots used")
            
            #Gets user input for each required field
            row = int(input("Enter row number! (1-10): ")) - 1 #Row input
            col_letter = input("Enter column letter (A-J): ").upper() #Column input
            col = let_to_num.get(col_letter, -1) #Conversion
            #Error checking for validity in location
            if col == -1 or row < 0 or row >= 10:
                print("Invalid row/column. Try again.")
                continue

            return row, col
        #Error checking for validity for input
        except ValueError:
            print("Invalid input. Please try again.")

def nuke():#firing function for nuke
    print("Nuke activated")
    explode.main()#Calls file to activate nuke
    return None

def carpet_bomb():#firing function for carpet bomb
    print("Carpet Bomb activated")
    rowCol = input("Enter the column letter or row number to bomb: ") #gets user's desired shot row or column
    if rowCol.isdigit():#checks if user wants to shoot row 
        row = int(rowCol)-1 #Formats row input
        if row < 0 or row >= 10:#Checks if row is valid
            print("Invalid row/column. Try again.")
        else:
            return [row,row,row,row,row,row,row,row,row,row], [0,1,2,3,4,5,6,7,8,9]#Fires all shots in row

    else:#runs if user wants to shoot column 
        col = let_to_num.get(rowCol.upper(), -1)#Formats column input
        if col == -1:#Checks if column is valid
            print("Invalid row/column. Try again.")
        else:
            return [0,1,2,3,4,5,6,7,8,9], [col,col,col,col,col,col,col,col,col,col]#Fires all shots in column

def air_strike():#firing function for air strike
    print("Air Strike requested")
    row = int(input("Enter the row number coordinate to bomb: "))-1#Gets user's desired shot and formats input
    col = let_to_num.get(input("Enter the column letter coordinate to bomb: ").upper(), -1)#Gets user's desired shot and formats input
    if col == -1 or row < 0 or row >= 10: #Checks valid input
        print("Invalid row/column. Try again.")
    else:
        #Creates and returns all coordinates for firing at 
        rows =[(row-1), row, (row+1)]
        cols = [(col-1), col, (col+1)]
        return [row, row, row, row+1, row-1], [col, col+1, col-1, col, col]

def scatter_shot():#firing function for scatter shot
    print("Fire the Scatter Shot")
    row = int(input("Enter the row number corrdinate to bomb: "))-1#Gets user's desired shot and formats input
    col = let_to_num.get(input("Enter the column letter coordinate to bomb: ").upper(), -1)#Gets user's desired shot and formats input
    if col == -1 or row < 0 or row >= 10:#Checks valid input
        print("Invalid row/column. Try again.")
    else:
        #Generates random numbers withing 3x3 range for rows and columns' coordinates
        ranR1 = random.randint(-1,1)
        ranR2 = random.randint(-1,1)
        ranR3 = random.randint(-1,1)
        ranC1 = random.randint(-1,1)
        ranC2 = random.randint(-1,1)
        ranC3 = random.randint(-1,1)

        #Check if the same coordinate was chosen and randomize values if so
        while ((ranR1,ranC1) == (ranR2,ranC2)) or ((ranR1,ranC1) == (ranR3,ranC3)) or ((ranR3,ranC3) == (ranR2,ranC2)):
            ranR2 = random.randint(-1,1)
            ranR3 = random.randint(-1,1)
            ranC2 = random.randint(-1,1)
            ranC3 = random.randint(-1,1)

        #Applies user's desired range to chosen random values for columns and rows
        cols = [col+ranC1, col+ranC2, col+ranC3]
        rows =[row+ranR1, row+ranR2, row+ranR3]
        return rows, cols

    
def printBoard(board, oppoboard): #Prints the player and oponents board by calling functions and formatting titles
            clearScreen()
            print("Opponent's Board")
            oppoboard.showShotBoard()
            print("------")
            print("Your Board")
            board.showBoard()
            print("Take your shot!")

def twoplayer():
        #Sets up and initalizes game, creates board for each user by calling ship_placement
        numShips = int(input("Enter the number of ships per player (1 to 5): "))
        while numShips < 1 or numShips > 5: #Error checking on how many ships
            print("Invalid number of ships! Please choose between 1 and 5.")
            numShips = int(input("Enter the number of ships per player (1 to 5): "))
        board1 = Board(numShips) #Create board
        board2 = Board(numShips) #Create board
        clearScreen()
        print("Player 1's Board:")
        board1.showBoard() #Prints board
        print("\nPlayer 1, place your ships:")
        board1.ship_placement(let_to_num) #Initializes ship placement and places where according to user
        clearScreen()
        print("\nPlayer 2's Board:")
        board2.showBoard() #Prints board
        print("\nPlayer 2, place your ships:")
        board2.ship_placement(let_to_num) #Initializes ship placement and places where according to user
        clearScreen()

        def checkEnd(hit):#Runs to check if the game should end when ship is hit
            if board1.has_lost():
                print("Player 1 wins!")
                return True #Ends game
            elif board2.has_lost():
                print("Player 2 wins!")
                return True#Ends game
            elif hit:
                print("Hit! Well done")
                return False#Continues game
            else:
                print("Miss! Boo!")
                return False#Continues game
        
        while (True):#players take their shots
            printBoard(board1, board2)
            
            row, col = get_shot() #Gets the shot
            clearScreen()
            
            if isinstance(row, list): #checks if list is given for special shots
                while (len(row) > 0):#Goes through shot coordinates
                    if (row[0] < 0 or row[0] >= 10 or col[0] < 0 or col[0] >= 10) == False: #Checks valid shot
                        hit = board2.take_shot(row[0], col[0]) #Fires shot
                        if (checkEnd(hit)):#Checks if won
                            break#ends game
                    #Takes fired coordinates off firing list
                    row.pop(0) 
                    col.pop(0)
                clearScreen()#removes all print statment from firing a line

            else:#Standard shot
                hit = board2.take_shot(row, col) #Fires user's shot
            if (checkEnd(hit)):#Checks if won
                break#ends game

            #Switches for next user
            _ = input("Click Enter when Player 2 has the computer!")
            printBoard(board2, board1)

            row, col = get_shot() #Gets the shot
            clearScreen()
            if isinstance(row, list): #checks if list for special shots
                while (len(row) > 0):#Goes through shot coordinates
                    if (row[0] < 0 or row[0] >= 10 or col[0] < 0 or col[0] >= 10) == False:#Checks valid shot
                        hit = board1.take_shot(row[0], col[0])#Fires shot
                        if (checkEnd(hit)):#Checks if won
                            break#ends game
                    #Takes fired coordinates off firing list
                    row.pop(0)
                    col.pop(0)  
                clearScreen()#removes all print statment from firing a line
            else:
                hit = board1.take_shot(row, col)#Fires shot
            if (checkEnd(hit)):#Checks if won
                break#ends game

            #Switches for next user
            _ = input("Click Enter when Player 1 has the computer!")

def oneplayer():#Players plays against computer
    #Asks user which difficulty they would like to play against
    diff = ''
    while True:
        difficulty = input("What difficulty would you like to play on? (e[asy], m[edium], h[ard]\n")
        if difficulty.lower() == 'easy' or difficulty.lower() == 'e':
            diff = 'easy'; break
        elif difficulty.lower() == 'medium' or difficulty.lower() == 'm':
            diff = 'medium'; break
        elif difficulty.lower() == 'hard' or difficulty.lower() == 'h':
            diff = 'hard'; break
        else:
            print("Bad input!")

    #Asks user how many ships they would like to play with
    numShips = int(input("Enter the number of ships (1 to 5): "))
    while numShips < 1 or numShips > 5: #Error checking on how many ships
        print("Invalid number of ships! Please choose between 1 and 5.")
        numShips = int(input("Enter the number of ships (1 to 5): "))

    playerBoard = Board(numShips) #Create board
    cpuBoard = Board(numShips) #Create board
    playerBoard.showBoard() #Prints board
    print("\nPlace your ships!:")
    playerBoard.ship_placement(let_to_num) #Initializes ship placement and places where according to user
    clearScreen()
    cpuBoard.autoPlaceShips()

    
    while True:#runs game
        printBoard(playerBoard, cpuBoard)#Shows boards to begin game
        row, col = get_shot() #Gets the shot
        if isinstance(row, list): #checks if list for special shots
            while (len(row) > 0):#Goes through shot coordinates
                if (row[0] < 0 or row[0] >= 10 or col[0] < 0 or col[0] >= 10) == False:#Checks valid shot
                    hit = cpuBoard.take_shot(row[0], col[0])#Fires shot
                #Takes fired coordinates off firing list
                row.pop(0)
                col.pop(0)
        else:
            hit = cpuBoard.take_shot(row, col)#Fires shot
            
        clearScreen()#resets screen view

        #Gives player feedback and checks if game should end or continue
        if cpuBoard.has_lost():
            print("You win!")
            return#ends game
        elif hit:
            print("Hit! Well done")
        else:
            print("Miss! Boo!")
            
        cpuFire = playerBoard.cpuTakeShot(diff)#Gets shot for cpu
        hit = playerBoard.take_shot(cpuFire[0],cpuFire[1])#Fires shot
        if playerBoard.has_lost():#Checks if game should end or continue
            clearScreen()
            print("CPU wins! Womp Womp....")
            return


#Main function of our program, handles the game setup, as well as the gameplay between each user
def main():
    while True:
        players = input("1 or 2 Players?: ")#Asks user if they want a 1 or 2 player game
        if players.lower() == "1" or players.lower() == "one":
            oneplayer()#starts one player game
            break
        elif players.lower() == "2" or players.lower() == "two":
            twoplayer()#starts two player game
            break
        else:
            print("Bad Input!")
    

if __name__ == "__main__":
    main()
