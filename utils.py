import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# 检测进食
def check_food_collision(snake_head, food_position):
    distance = math.sqrt(
        (snake_head[0] - food_position[0])**2 +
        (snake_head[1] - food_position[1])**2 +
        (snake_head[2] - food_position[2])**2
    )
    return distance < 1.0  # 当距离小于1时认为碰撞

# 加载纹理
def load_texture(image_path):
    texture_surface = pygame.image.load(image_path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
    width = texture_surface.get_width()
    height = texture_surface.get_height()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    # 添加纹理重复和边缘处理参数
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    return texture

def set_material_specular(reflectivity, shininess): # 对镜面光的反射程度和
    # 设置材料的镜面反射颜色和反射率
    specular_material = [reflectivity, reflectivity, reflectivity, 1.0]
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular_material)
    
    # 设置材料的光泽度
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)


def render_text(text, display, font, color=(255, 255, 255)):
    # 渲染文本为表面
    text_surface = font.render(text, True, color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_width(), text_surface.get_height()

    # 计算文本起始位置以使其居中
    x = (display[0] - width) // 2
    y = (display[1] - height) // 2

    # 切换到投影矩阵
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, display[0], 0, display[1])
    
    # 切换到模型视图矩阵
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # 禁用深度测试和纹理
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_TEXTURE_2D)

    # 设置文本位置
    glRasterPos2i(x, display[1] - y - height)
    
    # 渲染文本
    glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    # 恢复之前的矩阵和状态
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def menu():
    print("┌────────────────────────────────┐")
    print("│ 欢迎来到3D贪吃蛇               │")
    print("├────────────────────────────────┤")
    print("│ 操作提示                       │")
    print("│   [s]       开始游戏           │")
    print("│   [r]       重新游戏           │")
    print("│   [q]       退出游戏           │")
    print("│   [p]       暂停/继续游戏      │")
    print("│   [left]    逆时针旋转         │")
    print("│   [right]   顺时针旋转         │")
    print("├────────────────────────────────┤")
    print("│ 难度选择                       │")
    print("│   [1]       简单               │")
    print("│   [2]       中等               │")
    print("│   [3]       困难               │")
    print("└────────────────────────────────┘")

    while True:
        choice = input("请输入您的选择：").lower()
        if choice in ['1', '2', '3']:
            global speed
            speed_levels = {'1': 0.10, '2': 0.15, '3': 0.2}
            speed = speed_levels[choice]
            print(f"\n您已选择 {'简单' if choice == '1' else '中等' if choice == '2' else '困难'} 难度。\n")
            return speed
        else:
            print("\n无效输入，请重新输入！\n")
