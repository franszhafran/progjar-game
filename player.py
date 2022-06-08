from troop import Troop

def glr(a: int, b: int) -> list:
    return list(range(a, b+1))
class Player:
    player_number_start = [1, 14, 27, 40]
    player_number_safezone_start = [52, 58, 64, 70]
    player_number_finish = [57, 63, 69, 75]
    player_limit_end = [51, 12, 25, 38]

    player_tiles = [
        glr(1, 57),
        glr(14, 51) + glr(0, 12) + glr(58, 63),
        glr(27, 51) + glr(0, 25) + glr(64, 69),
        glr(40, 51) + glr(0, 38) + glr(70, 75)
    ]

    def __init__(self, name: str, player_number: int):
        self.name = name
        self.troops_on_base = list(range(0, 4))
        self.player_number = player_number
        self.troop_position = [-1, -1, -1, -1]
        self.last_steps = []
        self.player_tiles = Player.player_tiles[self.player_number]

        self.generate_troop()

    def generate_troop(self):
        self.troops = []

        for i in range(4):
            self.troops.append(Troop(Player.player_limit_end[self.player_number], Player.player_number_safezone_start[self.player_number]))

    def troop_out(self):
        troop_number = self.troops_on_base.pop()
        
        self.troops[troop_number].state = "regular_zone"
        self.troops[troop_number].position = 0
        self.troops[troop_number].x = self.player_tiles[0]
    
    def troop_out_possible(self):
        return len(self.troops_on_base) > 0
    
    def move_troop(self, troop_number: int, steps: int):
        troop = self.troops[troop_number]
        self.last_steps = []
        if troop.state == "regular_zone":
            for i in range(troop.position, troop.position + steps + 1):
                self.last_steps.append(self.player_tiles[i])
            troop.position += steps
            troop.x = self.player_tiles[troop.position]
            if troop.x >= Player.player_number_safezone_start[self.player_number]:
                troop.state = "safe_zone"
        else:
            if troop.position + steps == len(self.player_tiles)-1:
                for i in range(troop.position, troop.position + steps + 1):
                    self.last_steps.append(self.player_tiles[i])
                troop.state = "finish"
                troop.position += steps
                troop.x = self.player_tiles[troop.position]
            elif troop.position + steps > len(self.player_tiles)-1:
                step_forward = len(self.player_tiles)-troop.position-1
                step_backward = steps-step_forward
                for i in range(troop.position, troop.position+step_forward):
                    self.last_steps.append(self.player_tiles[i])

                for i in range(troop.position+step_forward, len(self.player_tiles)-1-step_backward-1, -1):
                    self.last_steps.append(self.player_tiles[i])
                troop.position = len(self.player_tiles)-1-step_backward
                troop.x = self.player_tiles[troop.position]
            else:
                for i in range(troop.position, troop.position + steps + 1):
                    self.last_steps.append(self.player_tiles[i])
                troop.position += steps
                troop.x = self.player_tiles[troop.position]
                

    def troop_drown(self, troop_number: int):
        print("Player {} troop {} drowned".format(self.player_number, troop_number))
        self.troops[troop_number].discard()

