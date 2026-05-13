import math
from utils.collision import circles_collide, circles_collide_xy

class CollisionManager:
    @staticmethod
    def handle_weapon_enemy_collisions(weapons, enemies):
        """武器攻击敌人，返回被消灭的敌人列表"""
        for weapon in weapons:
            wx, wy = weapon.get_position()
            for enemy in enemies[:]:
                if circles_collide_xy(wx, wy, weapon.radius, enemy.x, enemy.y, enemy.radius):
                    enemy.take_damage(weapon.damage)
                    # 击退
                    dx_knock = enemy.x - wx
                    dy_knock = enemy.y - wy
                    length = math.hypot(dx_knock, dy_knock)
                    if length != 0:
                        dx_knock /= length
                        dy_knock /= length
                    enemy.x += dx_knock * weapon.knockback
                    enemy.y += dy_knock * weapon.knockback
                    # if enemy.health <= 0:
                        # enemies.remove(enemy)
                    break

    @staticmethod
    def handle_player_enemy_collisions(player, enemies):
        """玩家与敌人碰撞，玩家受伤的话移除敌人"""
        for enemy in enemies[:]:
            if circles_collide(player, enemy):
                player.take_damage(1)
                enemies.remove(enemy)
                if player.health <= 0:
                    return True
        return False