import random

class Food:
    def __init__(self):
        self.position = (random.uniform(-10, 10), random.uniform(-10, 10), 0)

    def respawn(self):
        self.position = (random.uniform(-10, 10), random.uniform(-10, 10), 0)
