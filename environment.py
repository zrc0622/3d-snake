from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import pygame
from utils import *

def init_lighting(light_position):
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # 设置光源参数
    ambient_light = [0.5, 0.5, 0.5, 1.0]  # 环境光
    diffuse_light = [0.8, 0.8, 0.8, 1.0]  # 散射光
    specular_light = [1, 1, 1, 1.0]  # 镜面光

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # 设置光源的衰减参数
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)  # 常数衰减
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)  # 线性衰减
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.16)  # 平方衰减

    # 启用颜色追踪
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)



# 绘制平面
def draw_plane():
    glBegin(GL_QUADS)  # 开始绘制四边形
    glColor3fv((0.5, 0.5, 0.5))  # 设置颜色为灰色
    glVertex3fv((-20, -20, 0))  # 第一个顶点
    glVertex3fv((20, -20, 0))  # 第二个顶点
    glVertex3fv((20, 20, 0))  # 第三个顶点
    glVertex3fv((-20, 20, 0))  # 第四个顶点
    glEnd()  # 结束绘制

# 绘制具有纹理的平面
def draw_plane_with_texture(texture):
    glBindTexture(GL_TEXTURE_2D, texture)  # 绑定纹理
    glEnable(GL_TEXTURE_2D)  # 启用二维纹理

    # 启用颜色材料
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glColor3fv((1, 1, 1))  # 设置颜色为白色，不过通常镜面反射颜色不受此影响
    
    # 设置镜面反射属性
    set_material_specular(1, 128)

    glBegin(GL_QUADS)  # 开始绘制四边形
    glTexCoord2f(0.0, 0.0); glVertex3fv((-20, -20, 0))
    glTexCoord2f(1.0, 0.0); glVertex3fv((20, -20, 0))
    glTexCoord2f(1.0, 1.0); glVertex3fv((20, 20, 0))
    glTexCoord2f(0.0, 1.0); glVertex3fv((-20, 20, 0))
    glEnd()  # 结束绘制

    glDisable(GL_TEXTURE_2D)  # 禁用二维纹理
    glDisable(GL_COLOR_MATERIAL)  # 禁用颜色材料


# 绘制影子
def draw_shadow(position, light_position):
    x, y, z = position
    lx, ly, lz, lw = light_position

    # 影子投影矩阵
    shadow_matrix =  np.array([
        [lz, 0, -lx, 0],
        [0, lz, -ly, 0],
        [0, 0, 0, 0],
        [0, 0, -1, lz]
    ])

    glDisable(GL_LIGHTING)  # 禁用光照
    glColor3fv((0.1, 0.1, 0.1))  # 设置影子颜色为深灰色

    glPushMatrix()
    glMultMatrixf(shadow_matrix)
    draw_cube(position, (0.1, 0.1, 0.1))
    glPopMatrix()

    glEnable(GL_LIGHTING)  # 启用光照

# 绘制方块
def draw_cube(position, color):
    glBegin(GL_QUADS)
    glColor3fv(color)
    x, y, z = position

    vertices = [
        (x + 0.5, y - 0.5, z - 0.5),
        (x + 0.5, y + 0.5, z - 0.5),
        (x - 0.5, y + 0.5, z - 0.5),
        (x - 0.5, y - 0.5, z - 0.5),
        (x + 0.5, y - 0.5, z + 0.5),
        (x + 0.5, y + 0.5, z + 0.5),
        (x - 0.5, y - 0.5, z + 0.5),
        (x - 0.5, y + 0.5, z + 0.5),
    ]

    faces = [
        (0, 1, 2, 3),  # 前面
        (1, 5, 7, 2),  # 右面
        (3, 2, 7, 6),  # 后面
        (4, 5, 1, 0),  # 左面
        (6, 7, 5, 4),  # 顶面
        (4, 0, 3, 6),  # 底面 
    ]

    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

# 绘制带有纹理的方块
def draw_cube_with_texture(position, color, texture, head = False):
    glBindTexture(GL_TEXTURE_2D, texture)  # 绑定纹理
    glEnable(GL_TEXTURE_2D)  # 启用二维纹理

    x, y, z = position
    # 定义立方体的顶点
    vertices = [
        (x + 0.5, y - 0.5, z - 0.5),
        (x + 0.5, y + 0.5, z - 0.5),
        (x - 0.5, y + 0.5, z - 0.5),
        (x - 0.5, y - 0.5, z - 0.5),
        (x + 0.5, y - 0.5, z + 0.5),
        (x + 0.5, y + 0.5, z + 0.5),
        (x - 0.5, y - 0.5, z + 0.5),
        (x - 0.5, y + 0.5, z + 0.5),
    ]

    if head:
        vertices = [
        (x + 0.6, y - 0.6, z - 0.6),
        (x + 0.6, y + 0.6, z - 0.6),
        (x - 0.6, y + 0.6, z - 0.6),
        (x - 0.6, y - 0.6, z - 0.6),
        (x + 0.6, y - 0.6, z + 0.6),
        (x + 0.6, y + 0.6, z + 0.6),
        (x - 0.6, y - 0.6, z + 0.6),
        (x - 0.6, y + 0.6, z + 0.6),
    ]

    faces = [
        (0, 1, 2, 3),  # 前面
        (1, 5, 7, 2),  # 右面
        (3, 2, 7, 6),  # 后面
        (4, 5, 1, 0),  # 左面
        (6, 7, 5, 4),  # 顶面
        (4, 0, 3, 6),  # 底面 
    ]

    # 为每个面定义纹理坐标
    tex_coords_face = [
        (0, 0), (1, 0), (1, 1), (0, 1)  # 纹理坐标正确的顺序
    ]

    # 设置镜面反射属性
    set_material_specular(1, 100)
    # 渲染立方体的每个面
    for face in faces:
        glBegin(GL_QUADS)
        glColor3fv(color)  # 设置颜色
        for i, vertex in enumerate(face):
            glTexCoord2fv(tex_coords_face[i])  # 为每个顶点指定纹理坐标
            glVertex3fv(vertices[vertex])  # 定义顶点位置
        glEnd()

    glDisable(GL_TEXTURE_2D)  # 禁用二维纹理



