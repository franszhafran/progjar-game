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

    def draw():
        pass