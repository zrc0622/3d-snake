import random

class Food:
    def __init__(self):
        self.position = (random.uniform(-15, 15), random.uniform(-15, 15), 0)

    def respawn(self):
        self.position = (random.uniform(-15, 15), random.uniform(-15, 15), 0)
