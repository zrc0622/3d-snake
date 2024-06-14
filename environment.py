from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from utils import *

# 设置光源
def init_lighting(light_position):
    glEnable(GL_LIGHTING) # 启用光照
    glEnable(GL_LIGHT0) # 启用光源0

    # 设置光源参数
    ambient_light = [0.5, 0.5, 0.5, 1.0]  # 环境光
    diffuse_light = [0.8, 0.8, 0.8, 1.0]  # 散射光
    specular_light = [1, 1, 1, 1.0]  # 镜面光

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)  # 设置光源0的环境光
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)  # 设置光源0的散射光
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)  # 设置光源0的镜面光
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)  # 设置光源0的位置

    # 设置光源的衰减参数
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)  # 常数衰减
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)  # 线性衰减
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.16)  # 平方衰减

    # 启用颜色追踪
    glEnable(GL_COLOR_MATERIAL) # 启用颜色材料
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE) # 设置材料属性为前面材质的环境光和散射光

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

    glEnable(GL_COLOR_MATERIAL) # 启用颜色材料
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE) # 设置材料属性为前面材质的环境光和散射光
    glColor3fv((1, 1, 1))  # 设置颜色为白色，不过通常镜面反射颜色不受此影响
    
    set_material_specular(1, 128) # 设置镜面反射属性

    glBegin(GL_QUADS)  # 开始绘制四边形
    glTexCoord2f(0.0, 0.0); glVertex3fv((-20, -20, 0)) # 设置纹理坐标和顶点位置
    glTexCoord2f(1.0, 0.0); glVertex3fv((20, -20, 0))
    glTexCoord2f(1.0, 1.0); glVertex3fv((20, 20, 0))
    glTexCoord2f(0.0, 1.0); glVertex3fv((-20, 20, 0))
    glEnd()  # 结束绘制

    glDisable(GL_TEXTURE_2D)  # 禁用二维纹理
    glDisable(GL_COLOR_MATERIAL)  # 禁用颜色材料


# 绘制影子
def draw_shadow(position, light_position):
    lx, ly, lz, lw = light_position # 获取光源位置

    shadow_matrix =  np.array([ # 影子投影矩阵
        [lz, 0, -lx, 0],
        [0, lz, -ly, 0],
        [0, 0, 0, 0],
        [0, 0, -1, lz]
    ])

    glDisable(GL_LIGHTING)  # 禁用光照
    glColor3fv((0.1, 0.1, 0.1))  # 设置影子颜色为深灰色

    glPushMatrix() # 保存当前矩阵
    glMultMatrixf(shadow_matrix) # 乘以影子投影矩阵
    draw_cube(position, (0.1, 0.1, 0.1)) # 绘制影子
    glPopMatrix() # 恢复之前的矩阵

    glEnable(GL_LIGHTING)  # 启用光照

# 绘制方块
def draw_cube(position, color):
    glBegin(GL_QUADS) # 开始绘制四边形
    glColor3fv(color) # 设置颜色
    x, y, z = position # 获取方块位置

    vertices = [ # 定义方块的顶点
        (x + 0.5, y - 0.5, z - 0.5),
        (x + 0.5, y + 0.5, z - 0.5),
        (x - 0.5, y + 0.5, z - 0.5),
        (x - 0.5, y - 0.5, z - 0.5),
        (x + 0.5, y - 0.5, z + 0.5),
        (x + 0.5, y + 0.5, z + 0.5),
        (x - 0.5, y - 0.5, z + 0.5),
        (x - 0.5, y + 0.5, z + 0.5),
    ]

    faces = [ # 定义方块的各个面
        (0, 1, 2, 3),  # 前面
        (1, 5, 7, 2),  # 右面
        (3, 2, 7, 6),  # 后面
        (4, 5, 1, 0),  # 左面
        (6, 7, 5, 4),  # 顶面
        (4, 0, 3, 6),  # 底面 
    ]

    for face in faces: # 遍历每个面
        for vertex in face: # 遍历每个顶点
            glVertex3fv(vertices[vertex]) # 绘制顶点
    glEnd() # 结束绘制

# 绘制带有纹理的方块
def draw_cube_with_texture(position, color, texture, head = False):
    glBindTexture(GL_TEXTURE_2D, texture)  # 绑定纹理
    glEnable(GL_TEXTURE_2D)  # 启用二维纹理

    x, y, z = position # 获取方块位置
    vertices = [ # 定义方块的顶点
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
        vertices = [ # 蛇头定义较大的顶点
        (x + 0.6, y - 0.6, z - 0.6),
        (x + 0.6, y + 0.6, z - 0.6),
        (x - 0.6, y + 0.6, z - 0.6),
        (x - 0.6, y - 0.6, z - 0.6),
        (x + 0.6, y - 0.6, z + 0.6),
        (x + 0.6, y + 0.6, z + 0.6),
        (x - 0.6, y - 0.6, z + 0.6),
        (x - 0.6, y + 0.6, z + 0.6),
    ]

    faces = [ # 定义方块的各个面
        (0, 1, 2, 3),  # 前面
        (1, 5, 7, 2),  # 右面
        (3, 2, 7, 6),  # 后面
        (4, 5, 1, 0),  # 左面
        (6, 7, 5, 4),  # 顶面
        (4, 0, 3, 6),  # 底面 
    ]

    tex_coords_face = [ # 定义纹理坐标
        (0, 0), (1, 0), (1, 1), (0, 1)  # 纹理坐标
    ]

    set_material_specular(1, 100) # 设置镜面反射属性
    for face in faces:  # 遍历每个面
        glBegin(GL_QUADS)  # 开始绘制四边形
        glColor3fv(color)  # 设置颜色
        for i, vertex in enumerate(face):  # 遍历每个顶点
            glTexCoord2fv(tex_coords_face[i])  # 为每个顶点指定纹理坐标
            glVertex3fv(vertices[vertex])  # 定义顶点位置
        glEnd()  # 结束绘制

    glDisable(GL_TEXTURE_2D)  # 禁用二维纹理