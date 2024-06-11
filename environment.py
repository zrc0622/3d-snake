from OpenGL.GL import *

def draw_plane():
    """
    绘制平面
    """
    glBegin(GL_QUADS)
    glColor3fv((0.5, 0.5, 0.5))
    glVertex3fv((-10, -10, 0))
    glVertex3fv((10, -10, 0))
    glVertex3fv((10, 10, 0))
    glVertex3fv((-10, 10, 0))
    glEnd()

def draw_cube(position, color):
    """
    绘制立方体

    参数:
    - position: 立方体的位置
    - color: 立方体的颜色
    """
    glBegin(GL_QUADS)
    glColor3fv(color)
    x, y, z = position
    vertices = [
        (x - 0.5, y - 0.5, z - 0.5),
        (x + 0.5, y - 0.5, z - 0.5),
        (x + 0.5, y + 0.5, z - 0.5),
        (x - 0.5, y + 0.5, z - 0.5),
        (x - 0.5, y - 0.5, z + 0.5),
        (x + 0.5, y - 0.5, z + 0.5),
        (x + 0.5, y + 0.5, z + 0.5),
        (x - 0.5, y + 0.5, z + 0.5),
    ]
    faces = [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (2, 3, 7, 6),
        (0, 3, 7, 4),
        (1, 2, 6, 5),
    ]
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
