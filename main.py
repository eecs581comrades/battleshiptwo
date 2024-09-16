#Battleship Main File
#This file contains the main functions and gameplay mechanics for the game battleship. This initializes the game and runs all interactions between players.
#No inputs or outputs
#Authors: Aiden Murphy, Jack Doughty, Jack Pigott, Vy Luu, Daniel Bobadilla
#Supplemental help from ChatGPT and StackOverflow
#Creation Date: 09-13-2024
#Newest Commit: 09-15-2024


from board import Board
#Dictionary can be used as a global var to map chars to ints
let_to_num = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}

#Get_Shot gets the coordinates from each player as a target for their shot
def get_shot():
    while True:
        try:
            #Gets user input for each required field
            row = int(input("Enter row number (1-10): ")) - 1 #Row input
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

#Main function of our program, handles the game setup, as well as the gameplay between each user
def main():

    #Sets up and initalizes game, creates board for each user by calling ship_placement
    numShips = int(input("Enter the number of ships per player (1 to 5): "))
    while numShips < 1 or numShips > 5: #Error checking on how many ships
        print("Invalid number of ships! Please choose between 1 and 5.")
        numShips = int(input("Enter the number of ships per player (1 to 5): "))
    board1 = Board(numShips) #Create board
    board2 = Board(numShips) #Create board
    print("Player 1's Board:")
    board1.showBoard() #Prints board
    print("\nPlayer 2's Board:")
    board2.showBoard() #Prints board
    print("\nPlayer 1, place your ships:")
    board1.ship_placement(let_to_num) #Initializes ship placement and places where according to user
    print("\nPlayer 2, place your ships:")
    board2.ship_placement(let_to_num) #Initializes ship placement and places where according to user

    player_turn = 1 #Gameplay setup in main. Changes to get target from each player then outputs the board they shot at. Endgame check if all spots are hit.
    while True:
        if player_turn == 1:
            print("\nPlayer 1, take your shot!")
            row, col = get_shot() #Gets the shot
            board2.take_shot(row, col) #Takes the shot
            board2.showBoard() #Shows board after result

            #Endgame check
            if board2.has_lost():
                print("Player 1 wins!")
                break

            player_turn = 2
        else:
            print("\nPlayer 2, take your shot!")
            row, col = get_shot() #Gets the shot
            board1.take_shot(row, col) #Takes the shot
            board1.showBoard() #Shows board after result

            #Endgame check
            if board1.has_lost():
                print("Player 2 wins!")
                break

            player_turn = 1

if __name__ == "__main__":
    main()
