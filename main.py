from board import Board

#Dictionary can be used as a global var to map chars to ints
let_to_num = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}

def get_shot(): #Function to get shots from each player
    while True:
        try:
            row = int(input("Enter row number (1-10): ")) - 1
            col_letter = input("Enter column letter (A-J): ").upper()
            col = let_to_num.get(col_letter, -1)

            if col == -1 or row < 0 or row >= 10:
                print("Invalid row/column. Try again.")
                continue

            return row, col
        except ValueError:
            print("Invalid input. Please try again.")
def main():

    numShips = int(input("Enter the number of ships per player (1 to 5): "))

    while numShips < 1 or numShips > 5: #New check to make sure the number is valid
        print("Invalid number of ships! Please choose between 1 and 5.")
        numShips = int(input("Enter the number of ships per player (1 to 5): "))
    board1 = Board(numShips)
    board2 = Board(numShips)

    print("Player 1's Board:")
    board1.showBoard()
    print("\nPlayer 2's Board:")
    board2.showBoard()
    
    print("\nPlayer 1, place your ships:")
    board1.ship_placement(let_to_num) #New function to make setting up the boards easier
    print("\nPlayer 2, place your ships:")
    board2.ship_placement(let_to_num)

    player_turn = 1 #Gameplay setup in main. Changes to get target from each player then outputs the board they shot at. Endgame check if all spots are hit.
    while True:
        if player_turn == 1:
            print("\nPlayer 1, take your shot!")
            row, col = get_shot()
            board2.take_shot(row, col)
            board2.showBoard()

            if board2.has_lost():
                print("Player 1 wins!")
                break

            player_turn = 2
        else:
            print("\nPlayer 2, take your shot!")
            row, col = get_shot()
            board1.take_shot(row, col)
            board1.showBoard()

            if board1.has_lost():
                print("Player 2 wins!")
                break

            player_turn = 1

if __name__ == "__main__":
    main()
