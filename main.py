from board import Board
from match import Match
from player import Player
from random import randint

def main():
    board = Board("abc", [])
    
    player_1 = Player("Zhafran", 0)
    player_2 = Player("Ubay", 1)

    board.add_player(player_1)
    board.add_player(player_2)

    n = 0
    while True:
        dice = randint(1, 6)

        print("Dice {}".format(dice))
        board.print_troops()
        print("Player {} got {} step".format(n, dice))

        if board.player_troops_at_base(n) == 4 and dice != 6:
            print("Skipping")
            continue
        
        i = input("Enter troop number to move:")
        i = int(i)
        
        if i == 5:
            board.player_troop_out(n)
        elif board.move_player_troop_possible(n, i, dice):
            board.move_player_troop(n, i, dice)
        else:
            print("Not possible")

        n += 1

        if n == 2:
            n = 0

main()
