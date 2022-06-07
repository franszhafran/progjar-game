class Troop:
    def __init__(self):
        self.x = 0

    def move(self, steps: int):
        self.x += steps
    
    def discard(self):
        pass