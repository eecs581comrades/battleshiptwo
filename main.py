#Battleship Main File
#This file contains the main functions and gameplay mechanics for the game battleship. This initializes the game and runs all interactions between players.
#No inputs or outputs
#Authors: Aiden Murphy, Jack Doughty, Jack Pigott, Vy Luu, Daniel Bobadilla
#Supplemental help from ChatGPT and StackOverflow
#Creation Date: 09-13-2024
#Newest Commit: 09-15-2024


from board import Board, clearScreen
from scripts import explode

#Dictionary can be used as a global var to map chars to ints
let_to_num = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}

#Get_Shot gets the coordinates from each player as a target for their shot
def get_shot():
    while True:
        try:
            #Gets user input for each required field
            row = int(input("Enter row number! (1-10): ")) - 1 #Row input
            col_letter = input("Enter column letter (A-J): ").upper() #Column input
            col = let_to_num.get(col_letter, -1) #Conversion

            if col_letter == "N":
                explode.main()
            
            #Error checking for validity in location
            if col == -1 or row < 0 or row >= 10:
                print("Invalid row/column. Try again.")
                continue

            return row, col
        #Error checking for validity for input
        except ValueError:
            print("Invalid input. Please try again.")
            
def printBoard(board, oppoboard):
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

        def checkEnd(hit):
            if board1.has_lost():
                print("Player 1 wins!")
                return True
            elif board2.has_lost():
                print("Player 2 wins!")
                return True
            elif hit:
                print("Hit! Well done")
                return False
            else:
                print("Miss! Boo!")
                return False
        
        while (True):
            printBoard(board1, board2)
            row, col = get_shot() #Gets the shot
            hit = board2.take_shot(row, col) #Takes the shot
            clearScreen()
            if (checkEnd(hit)):
                break
            _ = input("Click Enter when Player 2 has the computer!")
            printBoard(board2, board1)
            row, col = get_shot() #Gets the shot
            hit = board1.take_shot(row, col) #Takes the shot
            clearScreen()
            if (checkEnd(hit)):
                break
            _ = input("Click Enter when Player 1 has the computer!")
            clearScreen()

def oneplayer():
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

    while True:
        printBoard(playerBoard, cpuBoard)
        row, col = get_shot() #Gets the shot
        hit = cpuBoard.take_shot(row, col)
        clearScreen()
        if cpuBoard.has_lost():
            print("You win!")
        elif hit:
            print("Hit! Well done")
            return False
        else:
            print("Miss! Boo!")
            return False
        playerBoard.cpuTakeShot(diff)
        if playerBoard.has_lost():
            clearScreen()
            print("CPU wins! Womp Womp....")


#Main function of our program, handles the game setup, as well as the gameplay between each user
def main():
    while True:
        players = input("1 or 2 Players?")
        if players.lower() == "1" or players.lower() == "one":
            oneplayer()
            break
        elif players.lower() == "2" or players.lower() == "two":
            twoplayer()
            break
        else:
            print("Bad Input!")
    

if __name__ == "__main__":
    main()
