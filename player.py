from troop import Troop

class Player:
    player_number_start = ["1", "14", "27", "40"]
    player_number_safezone_start = ["52", "58", "64", "70"]
    player_number_finish = ["57", "63", "69", "75"]
    player_limit_end = ["51", "12", "25", "38"]

    def __init__(self, name: str, player_number: int):
        self.name = name
        self.troops_on_base = list(range(0, 4))
        self.generate_troop()
        self.player_number = player_number

    def generate_troop(self):
        self.troops = []

        for i in range(4):
            self.troops.append(Troop())

    def troop_out(self):
        troop_number = self.troops_on_base.pop()

        self.move_troop(troop_number, Player.player_number_start[self.player_number])
    
    def troop_out_possible(self):
        return len(self.troops_on_base) > 0

    def move_troop(self, troop_number: int, steps: int):
        end_position = self.troops[troop_number].calculate_position(steps)
        if end_position > Player.player_limit_end[self.player_number]:
            print("Safe Zone")

        self.troops[troop_number].move(steps)
    
    def move_troop_safezone(self, troop_number: int, steps: int):
        troop = self.troops[troop_number]
        if troop.x != Player.player_limit_end[self.player_number]:
            raise Exception("Error, wrong safezone calculation")
        
        # call function to move safezone

