import math
import pygame
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

def set_material_specular(reflectivity, shininess): # 对镜面光的反射程度和材料光泽度
    # 设置材料的镜面反射颜色和反射率
    specular_material = [reflectivity, reflectivity, reflectivity, 1.0]
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular_material)
    
    # 设置材料的光泽度
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)

