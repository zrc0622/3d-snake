import math

class Snake:
    def __init__(self):
        self.positions = [(0, 0, 0)]
        self.angle = 0  # 初始角度为0度
        self.grow = False
        self.speed = 0.1  # 初始速度为0.1
        self.growth_distance = 2.0  # 每次增长的距离
        self.waiting_num = 0 # 待增长的块

    def move(self):
        head_x, head_y, head_z = self.positions[0]
        dir_x = math.cos(math.radians(self.angle)) * self.speed
        dir_y = math.sin(math.radians(self.angle)) * self.speed
        new_head = (head_x + dir_x, head_y + dir_y, head_z)

        if self.grow:
            self.positions = [new_head] + self.positions
            self.grow = False
        else:
            self.positions = [new_head] + self.positions[:-1]

    def change_angle(self, delta_angle):
        self.angle = (self.angle + delta_angle) % 360

    def check_collision(self):
        head = self.positions[0]
        return head in self.positions[1:]

    def grow_snake(self, segments=10):
        for _ in range(segments):  # 新增多个部分
            tail_end = self.positions[-1]
            if len(self.positions) > 1:
                tail_direction_x = self.positions[-1][0] - self.positions[-2][0]
                tail_direction_y = self.positions[-1][1] - self.positions[-2][1]
            else:
                tail_direction_x = -math.cos(math.radians(self.angle))
                tail_direction_y = -math.sin(math.radians(self.angle))

            new_part_x = tail_end[0] - tail_direction_x * self.growth_distance
            new_part_y = tail_end[1] - tail_direction_y * self.growth_distance
            new_part_z = tail_end[2]

            new_part = (new_part_x, new_part_y, new_part_z)
            self.positions.append(new_part)

    def head_position(self):
        return self.positions[0]
