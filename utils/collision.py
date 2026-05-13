import math

def distance(p1, p2):
    """计算两点距离"""
    dx = p1[0] - p2[0] if isinstance(p1, tuple) else p1.x - p2.x
    dy = p1[1] - p2[1] if isinstance(p1, tuple) else p1.y - p2.y
    return math.hypot(dx, dy)

def circles_collide(c1, c2):
    """检测两个圆形是否碰撞"""
    return distance(c1, c2) < c1.radius + c2.radius

def circles_collide_xy(x1, y1, r1, x2, y2, r2):
    return math.hypot(x1 - x2, y1 - y2) < r1 + r2