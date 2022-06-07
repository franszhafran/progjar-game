from match import Match
from player import Player
from random import randint
def main():
    match = Match("abc", [])
    
    player_1 = Player("Zhafran")
    player_2 = Player("Ubay")

    match.add_player(player_1)
    match.add_player(player_2)

    while True:
        dice = randint(1, 6)
        
        print(dice)
        i = input()

main()
