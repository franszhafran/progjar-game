class Troop:
    def __init__(self, end_position: int, safe_zone_position: int):
        self.x = -1 #tile number
        self.position = 0 #tile index on list
        self.state = "base"
        self.end_position = end_position
        self.safe_zone_position = safe_zone_position

    def move(self, steps: int):
        self.x += steps

    def set(self, pos: int):
        self.x = pos

    def calculate_position(self, steps: int):
        return self.x + steps
    
    def discard(self):
        self.state = "base"
        self.x = 0
        pass