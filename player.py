from troop import Troop

# generate left to right
def glr(a: int, b: int) -> list:
    return list(range(a, b+1))

# generate move
def gm(a: int, move: str) -> list:
    x = []
    for i in range(a):
        x.append(move)
    return x

def gma(count: list, steps: list):
    res = []
    for i in range(len(count)):
        count_now = count[i]
        res.append(gm(count_now, steps[i]))
    return res

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

    player_tiles_move = [
        gm(4, "up") + ["upleft"] + 
        gm(5, "left") + gm(2, "up") + gm(5, "right") + ["upright"] + 
        gm(5, "up") + gm(2, "right") + gm(5, "down") + ["downright"] +
        gm(5, "right") + gm(2, "down") + gm(5, "left") + ["downleft"] +
        gm(5, "down") + gm(1, "left"),
        gma([4, 1,
        5, 2, 5, 1, 
        5, 2, 5, 1, 
        5, 2, 5, 1, 
        5, 1], [
            "right", + "upright", 
            "up", "right", "down", "downright",
            "right", "down", "left", "downleft",
            "down", "left", "up", "upleft",
            "left", "up"
        ])
    ]

    def __init__(self, name: str, player_number: int):
        self.name = name
        self.troops_on_base = list(range(0, 4))
        self.player_number = player_number
        self.troop_position = [-1, -1, -1, -1]
        self.last_steps = []
        self.player_tiles = Player.player_tiles[self.player_number]
        self.player_tiles_move = Player.player_tiles_move[self.player_number]

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
        self.last_steps_index = []
        if troop.state == "regular_zone":
            for i in range(troop.position, troop.position + steps + 1):
                self.last_steps.append(self.player_tiles[i])
                self.last_steps_index = [i]
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

        print(self.last_steps)

    def process_steps_to_movement(self, last_steps: list):
        move = []
        for i in last_steps:
            move.append(self.player_tiles_move[self.player_number][i])
        return move
                

    def troop_drown(self, troop_number: int):
        print("Player {} troop {} drowned".format(self.player_number, troop_number))
        self.troops[troop_number].discard()

