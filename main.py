import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from utils import check_food_collision, load_texture, menu
from snake import Snake
from food import Food
from environment import draw_plane, draw_plane_with_texture, draw_cube, draw_cube_with_texture, init_lighting

speed = menu()  # 显示菜单并获取游戏难度

'''游戏初始化'''
# 游戏状态
START = 0
RUNNING = 1
PAUSED = 2
GAME_OVER = 3
QUIT = 4
game_state = START # 游戏初始化为开始状态

# 场景初始化
pygame.init()
display = (1600, 1200)  # 窗口分辨率

# 视角（摄像机）控制
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL) # 启动OpenGL渲染
gluPerspective(50, (display[0] / display[1]), 0.1, 100.0) # 摄像机视角: 视野角度（距离）、宽高比、近距离不裁剪、远距离不裁剪
glTranslatef(0, 5, -50) # 移动场景(x,y,z)
glRotatef(-40, 1, 0, 0) # 旋转场景

# 光源初始化
light_position = [20.0, -20.0, 15.0, 1.0] # 光源位置
init_lighting(light_position) # 初始化光源

# 材质初始化
snake_texture = load_texture("texture/snake1.png")   # 蛇的材质
snake_head_texture = load_texture("texture/snake2.png")   # 蛇头的材质
plane_texture = load_texture("texture/grass.png")   # 平台材质
food_texture = load_texture("texture/food.png")   # 食物材质

# 标题初始化
pygame.display.set_caption('3D Snake') # 设置游戏标题

# 其它初始化
start_angle = -45
rotation_angle = start_angle # 初始食物旋转角度

"""游戏设置"""
# 难度设置
segments = 15 # 每吃一个食物增长的长度
collision_threshold = 0.1 # 碰撞阈值

# 游戏设置
snake = Snake(speed) # 初始化蛇
food = Food() # 初始化食物
clock = pygame.time.Clock() # 初始化时钟
score = 0 # 初始化分数

# 重新开始函数
def reset_game():
    global snake, food, game_state, score
    snake = Snake(speed)  # 重新初始化蛇
    food = Food()  # 重新初始化食物
    game_state = START  # 游戏状态设为开始
    score = 0  # 分数清零

# 主循环
while True:
    """控制部分"""
    # 处理开始、暂停等
    for event in pygame.event.get(): # 获取所有事件
        if event.type == pygame.QUIT:
            pygame.quit() # 退出pygame
            quit() # 退出程序
        elif event.type == pygame.KEYDOWN: # 如果按下键盘
            if event.key == pygame.K_p: # 按下'p'键
                if game_state == RUNNING:
                    game_state = PAUSED # 切换为暂停状态
                elif game_state == PAUSED:
                    game_state = RUNNING # 切换为运行状态
            elif event.key == pygame.K_r: # 按下'r'键
                reset_game() # 重新开始游戏
            elif event.key == pygame.K_s: # 按下's'键
                if game_state == START:
                    game_state = RUNNING # 切换为运行状态
            elif event.key == pygame.K_q: # 按下'q'键
                print("\n欢迎下次游玩!")
                pygame.quit() # 退出pygame
                quit() # 退出程序

    # 处理蛇的控制等
    keys = pygame.key.get_pressed()  # 获取当前按键状态
    if game_state == RUNNING: # 如果游戏正在运行
        if keys[pygame.K_UP]:
            snake.speed += 0.01  # 增加速度
        if keys[pygame.K_DOWN]:
            snake.speed = max(0.01, snake.speed - 0.01)  # 减小速度，最低为0.01
        if keys[pygame.K_LEFT]:
            snake.change_angle(5)  # 逆时针旋转5度
        if keys[pygame.K_RIGHT]:
            snake.change_angle(-5)  # 顺时针旋转5度

        snake.move() # 移动蛇
        snake.grow_snake()  # 增长蛇身

        if snake.check_collision(collision_threshold) or snake.check_boundary_collision():
            game_state = GAME_OVER # 如果碰撞，游戏结束
            print(f"游戏结束, 你的成绩是{score}分!")

        if check_food_collision(snake.head_position(), food.position):
            snake.waiting_num += segments # 增加等待增长的块数
            score += 1 # 增加分数
            food.respawn() # 重新生成食物

    """渲染部分"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # 清空颜色和深度缓冲
    draw_plane_with_texture(plane_texture) # 绘制带有纹理的平面
    
    if game_state in [RUNNING, PAUSED, GAME_OVER]:
        # 绘制蛇
        adjusted_positions = [snake.positions[0]]  # 初始化调整后的位置列表（重新计算蛇的各部分位置）

        # 更新每个身体部分的位置
        for i in range(1, len(snake.positions)):
            adjusted_positions.append(snake.positions[i - 1]) # 直接使用前一个部分的位置

        # 绘制蛇的每个身体部分
        for index, pos in enumerate(snake.positions):
            if index % segments == 0:  # 检查索引是否是segments的倍数
                if index == 0:
                    draw_cube_with_texture(pos, (1, 1, 1), snake_head_texture, True) # 绘制蛇头
                else:
                    draw_cube_with_texture(pos, (1, 1, 1), snake_texture) # 绘制蛇身体
            else:
                continue

        # 绘制食物
        glPushMatrix()
        glTranslatef(*food.position)  # 将食物方块移动到其位置
        glRotatef(rotation_angle, 0, 0, 1)  # 绕Z轴旋转（中轴线）
        draw_cube_with_texture((0, 0, 0), (1.0, 1.0, 1.0), food_texture)  # 以原点为中心绘制食物方块
        glPopMatrix()

        rotation_angle += 1  # 更新旋转角度
        if rotation_angle >= start_angle + 90:
            rotation_angle = start_angle  # 防止角度过大


    pygame.display.flip() # 刷新屏幕
    clock.tick(90)  # 调节帧率

    if game_state == GAME_OVER:
        reset_game()  # 重新游戏