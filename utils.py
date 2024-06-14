import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# 检测进食
def check_food_collision(snake_head, food_position):
    distance = math.sqrt( # 计算蛇头与食物之间的距离
        (snake_head[0] - food_position[0])**2 +
        (snake_head[1] - food_position[1])**2 +
        (snake_head[2] - food_position[2])**2
    )
    return distance < 1.0  # 当距离小于1时认为碰撞

# 加载纹理
def load_texture(image_path):
    texture_surface = pygame.image.load(image_path) # 加载图像
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1) # 将图像数据转换为字符串
    width = texture_surface.get_width() # 获取图像宽度
    height = texture_surface.get_height() # 获取图像高度

    texture = glGenTextures(1) # 生成一个纹理ID
    glBindTexture(GL_TEXTURE_2D, texture) # 绑定纹理
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)  # 指定纹理图像

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) # 设置纹理缩小过滤
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # 设置纹理放大过滤
    
    # 添加纹理重复和边缘处理参数
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # 设置S轴纹理重复
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) # 设置T轴纹理重复

    return texture

# 设置材料的镜面反射颜色和反射率
def set_material_specular(reflectivity, shininess): 
    specular_material = [reflectivity, reflectivity, reflectivity, 1.0] # 镜面反射颜色
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular_material)  # 设置材料的镜面反射颜色
    glMaterialf(GL_FRONT, GL_SHININESS, shininess) # 设置材料的光泽度

# 渲染文本
def render_text(text, display, font, color=(255, 255, 255)):
    text_surface = font.render(text, True, color) # 渲染文本为表面
    text_data = pygame.image.tostring(text_surface, "RGBA", True) # 将文本表面转换为字符串
    width, height = text_surface.get_width(), text_surface.get_height() # 获取文本表面的宽度和高度

    x = (display[0] - width) // 2 # 计算文本起始位置以使其居中
    y = (display[1] - height) // 2

    glMatrixMode(GL_PROJECTION) # 设置当前矩阵模式为投影矩阵
    glPushMatrix() # 保存当前矩阵
    glLoadIdentity() # 重置矩阵
    gluOrtho2D(0, display[0], 0, display[1]) # 设置正交投影矩阵
    
    glMatrixMode(GL_MODELVIEW) # 切换到模型视图矩阵
    glPushMatrix() # 保存当前矩阵
    glLoadIdentity() # 重置矩阵

    glDisable(GL_DEPTH_TEST) # 禁用深度测试
    glDisable(GL_TEXTURE_2D) # 禁用二维纹理

    glRasterPos2i(x, display[1] - y - height) # 设置文本的光栅位置
    
    glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data) # 渲染文本

    # 恢复之前的矩阵和状态
    glEnable(GL_DEPTH_TEST) # 启用深度测试
    glEnable(GL_TEXTURE_2D) # 启用二维纹理
    glMatrixMode(GL_PROJECTION) # 设置当前矩阵模式为投影矩阵
    glPopMatrix() # 恢复之前的矩阵
    glMatrixMode(GL_MODELVIEW) # 设置当前矩阵模式为模型视图矩阵
    glPopMatrix() # 恢复之前的矩阵

# 菜单提示
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
        choice = input("请输入您的选择：").lower() # 获取用户输入并转换为小写
        if choice in ['1', '2', '3']: # 如果输入为1, 2, 或3
            global speed # 声明全局变量speed
            speed_levels = {'1': 0.10, '2': 0.15, '3': 0.2} # 定义不同难度级别的速度
            speed = speed_levels[choice] # 根据用户选择设置速度
            print(f"\n您已选择 {'简单' if choice == '1' else '中等' if choice == '2' else '困难'} 难度。\n")
            return speed # 返回选择的速度
        else:
            print("\n无效输入，请重新输入！\n")
