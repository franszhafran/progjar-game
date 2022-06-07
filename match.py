from player import Player
from typing import List

class Match:
    def __init__(self, match_id: str, players: List[Player]):
        self.match_id = match_id

        self.players = players

    def add_player(self, player: Player):
        self.players.append(player)

    def move_player_troop(self, player_number: int, troop_number: int, steps: int):
        self.players[player_number].move_troop(troop_number, steps)

        # check collision
        troop = self.players[player_number].troops[troop_number]
        for i in range(len(self.players)):
            if i == player_number:
                continue
            for j in range(len(self.players.troops)):
                troop_check = self.players[i].troops[j]
                if troop_check != "base":
                    if troop_check.x == troop.x:
                        troop.discard()
                    elif troop_check.x < troop.x and troop_check.x > troop.x-steps:
                        troop_check.discard()

    def move_player_troop_possible(self, player_number: int, troop_number: int, steps: int):
        troop = self.players[player_number].troops[troop_number]

        if troop.state == "base" and steps != 6:
            return False
        return True

    def draw():
        pass