import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

from snake import Snake
from food import Food
from environment import draw_plane, draw_cube

# 初始化游戏
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 1.7, -28)
glRotatef(-45, 1, 0, 0)

# 主循环
snake = Snake()
food = Food()
clock = pygame.time.Clock()

def check_food_collision(snake_head, food_position):
    distance = math.sqrt(
        (snake_head[0] - food_position[0])**2 +
        (snake_head[1] - food_position[1])**2 +
        (snake_head[2] - food_position[2])**2
    )
    return distance < 1.0  # 当距离小于1时认为碰撞

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.speed += 0.01  # 增加速度
    if keys[pygame.K_DOWN]:
        snake.speed = max(0.01, snake.speed - 0.01)  # 减小速度，最低为0.01
    if keys[pygame.K_LEFT]:
        snake.change_angle(5)  # 逆时针旋转5度
    if keys[pygame.K_RIGHT]:
        snake.change_angle(-5)  # 顺时针旋转5度

    snake.move()

    if check_food_collision(snake.head_position(), food.position):
        snake.grow = True  # 设置增长标志
        food.respawn()

    if snake.check_collision():
        print("Game Over!")
        pygame.quit()
        quit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_plane()
    
    # 绘制蛇，增加间隔
    spacing_factor = 2.0  # 间隔系数
    adjusted_positions = [snake.positions[0]]  # 初始化调整后的位置列表，包含蛇头位置
    for i in range(1, len(snake.positions)):
        original_pos = snake.positions[i]
        prev_pos = adjusted_positions[i - 1]
        dir_x = original_pos[0] - snake.positions[i - 1][0]
        dir_y = original_pos[1] - snake.positions[i - 1][1]
        dir_z = original_pos[2] - snake.positions[i - 1][2]
        new_pos = (prev_pos[0] + dir_x * spacing_factor, prev_pos[1] + dir_y * spacing_factor, prev_pos[2] + dir_z * spacing_factor)
        adjusted_positions.append(new_pos)
    
    for pos in adjusted_positions:
        draw_cube(pos, (0, 1, 0))
    
    draw_cube(food.position, (1, 0, 0))
    pygame.display.flip()
    clock.tick(60)  # 调节帧率
