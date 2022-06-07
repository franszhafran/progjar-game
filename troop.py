class Troop:
    def __init__(self):
        self.x = 0
        self.state = "base"

    def move(self, steps: int):
        self.x += steps
        print("Troop pos {}".format(self.x))

    def calculate_position(self, steps: int):
        return self.x + steps
    
    def discard(self):
        self.state = "base"
        self.x = 0
        pass