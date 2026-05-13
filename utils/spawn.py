import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_RADIUS

def get_random_edge_position():
    """在屏幕外边缘随机生成一个坐标"""
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top':
        x = random.randint(0, SCREEN_WIDTH)
        y = -ENEMY_RADIUS
    elif side == 'bottom':
        x = random.randint(0, SCREEN_WIDTH)
        y = SCREEN_HEIGHT + ENEMY_RADIUS
    elif side == 'left':
        x = -ENEMY_RADIUS
        y = random.randint(0, SCREEN_HEIGHT)
    else:  # right
        x = SCREEN_WIDTH + ENEMY_RADIUS
        y = random.randint(0, SCREEN_HEIGHT)
    return x, y