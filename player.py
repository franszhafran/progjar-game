from troop import Troop

class Player:
    def __init__(self, name: str):
        self.name = name

        self.generate_troop()

    def generate_troop(self):
        self.troops = []

        for i in range(4):
            self.troops.append(Troop())

    def move_troop(self, troop_number: int, steps: int):
        self.troops[troop_number].move(steps)
        pass