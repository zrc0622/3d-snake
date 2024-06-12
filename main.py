import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from utils import check_food_collision, load_texture
from snake import Snake
from food import Food
from environment import draw_plane, draw_plane_with_texture, draw_cube, draw_cube_with_texture, init_lighting, draw_shadow

# 初始化游戏
pygame.init()
display = (1600, 1200)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 1.7, -28)
glRotatef(-45, 1, 0, 0)
light_position = [-2.0, -2.0, 10.0, 1.0]    # 光源位置
init_lighting(light_position)  # 初始化光源

# 材质
snake_texture = load_texture("texture/snake.png")   # 蛇的材质
plane_texture = load_texture("texture/grass.png")

# 主循环
snake = Snake()
food = Food()
clock = pygame.time.Clock()

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
    draw_plane_with_texture(plane_texture)
    
    # # 绘制影子
    # for pos in snake.positions:
    #     draw_shadow(pos, light_position)
    # draw_shadow(food.position, light_position)
    
    # 绘制蛇
    spacing_factor = 15.0  # 间隔系数，可以根据你的游戏设计调整，但在此逻辑中不再需要
    adjusted_positions = [snake.positions[0]]  # 初始化调整后的位置列表，包含蛇头位置

    # 更新每个身体部分的位置
    for i in range(1, len(snake.positions)):
        # 直接使用前一个部分的位置
        adjusted_positions.append(snake.positions[i - 1])

    # 绘制蛇的每个身体部分
    for pos in adjusted_positions:
        # 绘制每个蛇身节
        draw_cube_with_texture(pos, (1, 1, 1), snake_texture)

    # 绘制食物
    draw_cube(food.position, (1, 0, 0))
    
    pygame.display.flip()
    clock.tick(60)  # 调节帧率
