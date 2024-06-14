import math

class Snake:
    def __init__(self, speed):
        self.positions = [(0, 0, 0)] # 蛇的初始位置，实际上是一个列表，列表中的每个位置代表每个身体块的位置
        self.angle = 0  # 初始角度为0度
        self.grow = False  # 蛇是否增长的标志
        self.speed = speed  # 初始速度
        self.growth_distance = 2.0  # 每次增长的距离
        self.waiting_num = 0 # 待增长的块的数量

    # 蛇移动
    def move(self):
        head_x, head_y, head_z = self.positions[0] # 获取蛇头位置
        dir_x = math.cos(math.radians(self.angle)) * self.speed # 计算x方向的移动距离
        dir_y = math.sin(math.radians(self.angle)) * self.speed # 计算y方向的移动距离
        new_head = (head_x + dir_x, head_y + dir_y, head_z) # 计算新的蛇头位置

        if self.grow:
            self.positions = [new_head] + self.positions  # 蛇增长，增加新的头部位置
            self.grow = False
        else:
            self.positions = [new_head] + self.positions[:-1]  # 蛇移动，不增长
    
    # 蛇角度改变
    def change_angle(self, delta_angle):
        self.angle = (self.angle + delta_angle) % 360 # 改变蛇的方向

    # 自身碰撞检测
    def check_collision(self, collision_threshold):
        head_x, head_y, head_z = self.positions[0]  # 获取蛇头位置
        for x, y, z in self.positions[5:]: # 检查蛇头与身体其余部分的碰撞
            distance = math.sqrt((head_x - x)**2 + (head_y - y)**2 + (head_z - z)**2) # 计算距离
            if distance < collision_threshold:
                return True
        return False
    
    # 边缘碰撞检测，与平台大小对应
    def check_boundary_collision(self, boundary=(-20, 20)):
        x, y, z = self.positions[0]  # 获取蛇头位置
        min_boundary, max_boundary = boundary # 边界值
        if (x < min_boundary or x > max_boundary or
            y < min_boundary or y > max_boundary or
            z < min_boundary or z > max_boundary):
            return True
        return False

    # 蛇身增长
    def grow_snake(self):
        if self.waiting_num > 0:
            tail_end = self.positions[-1] # 获取蛇尾位置
            if len(self.positions) > 1:
                tail_direction_x = self.positions[-1][0] - self.positions[-2][0] # 计算尾部方向
                tail_direction_y = self.positions[-1][1] - self.positions[-2][1]
            else:
                tail_direction_x = -math.cos(math.radians(self.angle))
                tail_direction_y = -math.sin(math.radians(self.angle))

            new_part_x = tail_end[0] - tail_direction_x * self.growth_distance # 计算新的蛇尾部分位置（实际没有用，最后渲染是用前一个方块的上一时刻的位置）
            new_part_y = tail_end[1] - tail_direction_y * self.growth_distance
            new_part_z = tail_end[2]

            new_part = (new_part_x, new_part_y, new_part_z)
            self.positions.append(new_part) # 增加新的蛇尾部分
            
            self.waiting_num -= 1 # 减少待增长的块数量

    # 获取蛇头位置
    def head_position(self):
        return self.positions[0] # 返回蛇头位置
