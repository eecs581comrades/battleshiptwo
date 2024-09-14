from board import Board

#Dictionary can be used as a global var to map chars to ints
let_to_num={'A':0,'B':1, 'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}

def main():
    numShips = int(input("Enter the number of ships per player: "))
    board1 = Board(numShips)
    board2 = Board(numShips)
    board1.buildBoard()
    board2.buildBoard()
    board1.showBoard()
    print("\n")
    board1.ship_placement()
    board2.ship_placement()


if __name__ == "__main__":
    main()

