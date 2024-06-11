# 3D贪吃蛇

基于OpenGL的3D贪吃蛇小游戏，使用Python和Pygame开发。

## 文件结构

- `main.py`：主程序文件，负责游戏的初始化和主循环。
- `snake.py`：定义贪吃蛇类，包含贪吃蛇的移动、增长和碰撞检测等功能。
- `food.py`：定义食物类，包含食物的位置和重生功能。
- `environment.py`：包含绘制平面和立方体的函数，负责游戏环境的绘制。

## 依赖安装

在运行游戏之前，请确保已安装以下依赖：

```bash
pip install pygame PyOpenGL
```

## 运行游戏

使用以下命令行运行游戏

```bash
python main.py
```

## TODO
- [ ] 添加环境光照
- [ ] 添加边界