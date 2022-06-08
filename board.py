from typing import List

from match import Match
from player import Player
from troop import Troop

class Board(Match):
    player_number_start = [1, 14, 27, 40]
    player_number_safezone_start = [52, 58, 64, 70]
    player_number_finish = [57, 63, 69, 75]
    player_limit_end = [51, 12, 25, 38]

    def __init__(self, match_id: str, players: List[Player]):
        super().__init__(match_id, players)

    def generate_tile_animation_list(self, player_number: int, troop_number: int, steps: int):
        troop: Troop = self.players[player_number].troops[troop_number]
        limit = Board.player_limit_end[player_number]

        if troop.calculate_position(steps) > limit:
            print(list(range(troop.x, limit)))
            print(list(range(Board.player_number_safezone_start[player_number], (limit-troop.calculate_position(steps)-1))))
            return list(range(troop.x, limit)) + list(range(Board.player_number_safezone_start[player_number], limit-troop.calculate_position(steps)-1))
        else:
            return list(range(troop.x, troop.calculate_position(steps)+1))

    def print_troops(self):
        for i in range(len(self.players)):
            for j in range(len(self.players[i].troops)):
                troop_check = self.players[i].troops[j]
                if troop_check.state != "base":
                    print("Player {} troop {} at pos {}".format(i, j, troop_check.x))