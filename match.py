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
        last_steps = self.players[player_number].last_steps
        troop = self.players[player_number].troops[troop_number]
        for i in range(len(self.players)):
            if i == player_number:
                continue
            for j in range(len(self.players[i].troops)):
                troop_check = self.players[i].troops[j]
                if troop_check != "base":
                    if troop_check.x in last_steps:
                        self.players[i].troop_drown(j)

    def move_player_troop_possible(self, player_number: int, troop_number: int, steps: int):
        troop = self.players[player_number].troops[troop_number]

        if troop.state == "base" and steps != 6:
            return False
        if troop.state == "finish":
            return False
        return True

    def player_troop_out(self, player_number: int):
        player = self.players[player_number]

        player.troop_out()

    def player_troops_at_base(self, player_number: int) -> int:
        return len(self.players[player_number].troops_on_base)

    def draw():
        pass