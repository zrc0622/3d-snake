import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from utils import check_food_collision, load_texture, set_material_specular
from snake import Snake
from food import Food
from environment import draw_plane, draw_plane_with_texture, draw_cube, draw_cube_with_texture, init_lighting, draw_shadow, draw_cube_with_texture2

'''游戏初始化'''
# 场景初始化
pygame.init()
display = (1600, 1200)  # 窗口分辨率
pygame.display.set_mode(display, DOUBLEBUF | OPENGL) # 启动OpenGL渲染
gluPerspective(50, (display[0] / display[1]), 0.1, 100.0) # 摄像机视角: 视野角度（距离）、宽高比、近距离不裁剪、远距离不裁剪
glTranslatef(0, 5, -50) # 移动场景(x,y,z)
glRotatef(-40, 1, 0, 0) # 旋转场景

# 光源初始化
light_position = [20.0, -20.0, 15.0, 1.0]    # 光源位置
init_lighting(light_position)  # 初始化光源

# 难度设置
segments = 15 # 每吃一个食物增长的长度
speed = 0.10 # 初始速度
collision_threshold = 0.1 # 碰撞阈值

# 材质初始化
snake_texture = load_texture("texture/snake1.png")   # 蛇的材质
snake_head_texture = load_texture("texture/snake2.png")   # 蛇的材质
plane_texture = load_texture("texture/grass.png")   # 平台材质
food_texture = load_texture("texture/food.png")   # 平台材质

# 其它初始化
start_angle = -45
rotation_angle = start_angle # 初始食物旋转角度

# 主循环
snake = Snake(speed)
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
    snake.grow_snake()  # 增长标志

    if snake.check_collision(collision_threshold) or snake.check_boundary_collision():
        print("Game Over!")
        pygame.quit()
        quit()

    if check_food_collision(snake.head_position(), food.position):
        snake.waiting_num += segments
        food.respawn()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_plane_with_texture(plane_texture)
    # draw_plane()
    
    # # 绘制影子
    # for pos in snake.positions:
    #     draw_shadow(pos, light_position)
    # draw_shadow(food.position, light_position)
    
    """
    渲染部分
    """
    # 绘制蛇
    adjusted_positions = [snake.positions[0]]  # 初始化调整后的位置列表，包含蛇头位置

    # 更新每个身体部分的位置
    for i in range(1, len(snake.positions)):
        # 直接使用前一个部分的位置
        adjusted_positions.append(snake.positions[i - 1])

    # 绘制蛇的每个身体部分
    # 绘制蛇
    for index, pos in enumerate(snake.positions):
        if index % segments == 0:  # 检查索引是否是10的倍数
            if index == 0:
                draw_cube_with_texture(pos, (1, 1, 1), snake_head_texture, True)
            else:
                draw_cube_with_texture(pos, (1, 1, 1), snake_texture)
        else:
            continue

    # 绘制食物
    glPushMatrix()
    glTranslatef(*food.position)  # 将食物方块移动到其位置
    glRotatef(rotation_angle, 0, 0, 1)  # 绕Z轴旋转（中轴线）
    draw_cube_with_texture2((0, 0, 0), (1.0, 1.0, 1.0), food_texture)  # 以原点为中心绘制食物方块
    glPopMatrix()

    rotation_angle += 1  # 更新旋转角度
    if rotation_angle >= start_angle + 90:
        rotation_angle = start_angle  # 防止角度过大
    
    pygame.display.flip()
    clock.tick(90)  # 调节帧率
