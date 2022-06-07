from match import Match
from player import Player
from random import randint
from kivy.app import App
from kivy.uix.widget import Widget

def main():
    match = Match("abc", [])
    
    player_1 = Player("Zhafran", 0)
    player_2 = Player("Ubay", 1)

    match.add_player(player_1)
    match.add_player(player_2)

    n = 0
    while True:
        dice = randint(1, 6)

        print(dice)
        
        print("Player {} got {} step".format(n, dice))
        i = input()

        if match.move_player_troop_possible(n, int(i), dice):
            match.move_player_troop(n, int(i), dice)
        else:
            print("Not possible")

        n += 1

        if n == 2:
            n = 0

main()
