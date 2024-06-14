import random

class Food:
    # 食物初始化
    def __init__(self):
        self.position = (random.uniform(-15, 15), random.uniform(-15, 15), 0) # 初始化食物位置，x和y在-15到15之间随机

    # 食物重生
    def respawn(self):
        self.position = (random.uniform(-15, 15), random.uniform(-15, 15), 0) # 重新生成食物位置，x和y在-15到15之间随机
