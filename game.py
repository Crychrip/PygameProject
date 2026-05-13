# game.py
import pygame
import random
import math
from settings import (SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WEAPON_COUNT,
                      MATERIAL_DROP_VALUE, BUILDING_EFFECTS,
                      WORLD_WIDTH_TILES, WORLD_HEIGHT_TILES, TILE_SIZE,
                      PLAYER_SPEED)
from formula import EQUIPMENTS
from entities.player import Player
from entities.weapon import Weapon
from managers.input_manager import InputManager
from managers.enemy_spawner import EnemySpawner
from managers.collision_manager import CollisionManager
from managers.ui_manager import UIManager
from managers.experience_manager import ExperienceManager
from managers.upgrade_manager import UpgradeManager
from managers.material_manager import MaterialManager
from managers.equipment_manager import EquipmentManager
from managers.save_manager import SaveManager
from world.map_generator import MapGenerator, TerrainType
from world.camera import Camera
from world.minimap import MiniMap
from ui.backpack_ui import BackpackUI

class Game:
    def __init__(self, screen, font, return_to_camp_callback):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = font
        self.ui = UIManager(self.font)
        self.map_gen = MapGenerator(seed=random.randint(0, 10000))
        self.world_width = WORLD_WIDTH_TILES * TILE_SIZE
        self.world_height = WORLD_HEIGHT_TILES * TILE_SIZE
        self.decoration_objects = self.map_gen.decoration_objects
        self.camera = Camera(screen.get_width(), screen.get_height(),
                             self.world_width, self.world_height)
        self.minimap = None
        self.input_mgr = InputManager()
        self.spawner = EnemySpawner()
        self.collision_mgr = CollisionManager()
        self.exp_mgr = ExperienceManager()
        self.upgrade_mgr = UpgradeManager()
        self.material_mgr = MaterialManager()
        self.save_mgr = SaveManager()
        save_data = self.save_mgr.load()
        inventory = save_data.get("inventory", {})
        self.material_mgr.from_dict(inventory)
        self.equip_mgr = EquipmentManager(self.material_mgr)
        self.equip_mgr.from_dict(save_data)
        self.backpack_ui = BackpackUI(screen, font, self.material_mgr, self.equip_mgr)
        self.return_to_camp = return_to_camp_callback  # 回调函数，返回营地
        self.load_permanent_bonuses() # 加载永久属性加成
        self.load_equipment_bonuses()
        self.state = "playing"          # playing或者upgrading
        self.upgrade_options = []
        self.selected_upgrade = 0
        self.exit_to_camp = False
        self.reset()

    def load_permanent_bonuses(self):
        """从存档读取建筑等级计算加成"""
        save_data = self.save_mgr.load()
        buildings = save_data["buildings"]
        self.permanent_bonus = {
            "damage": 0,
            "max_health": 0,
            "attack_speed": 0,
            "speed": 0
        }
        for building, level in buildings.items():
            effect = BUILDING_EFFECTS[building]
            self.permanent_bonus[effect["stat"]] += effect["value"] * level
    
    def load_equipment_bonuses(self):
        """从存档读取装备等级计算加成"""
        save_data = self.save_mgr.load()
        equipped_items = save_data.get("equipped_items", [])
        self.equipment_bonus = {
            "damage": 0, 
            "max_health": 0, 
            "harvest_bonus": 0, 
            "speed": 0, 
            "attack_speed": 0
        }
        for item_id in equipped_items:
            item_info = EQUIPMENTS.get(item_id)
            if item_info and "effect" in item_info:
                for stat, value in item_info["effect"].items():
                    if stat in self.equipment_bonus:
                        self.equipment_bonus[stat] += value

    def reset(self):
        self.map_gen = MapGenerator(seed=random.randint(0, 10000))
        self.map_gen.generate_full_map()
        self.decoration_objects = self.map_gen.decoration_objects
        self.world_width = WORLD_WIDTH_TILES * TILE_SIZE
        self.world_height = WORLD_HEIGHT_TILES * TILE_SIZE
        # self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, self.world_width, self.world_height)
        start_x = self.world_width // 2
        start_y = self.world_height // 2
        self.player = Player(start_x, start_y)
        self.minimap = MiniMap(self.map_gen, self.camera, self.world_width, self.world_height)

        self.enemies = []
        self.weapons = []
        self.exp_mgr = ExperienceManager()
        # self.material_mgr = MaterialManager()

        self.player.damage = 1 + self.permanent_bonus["damage"] + self.equipment_bonus["damage"]
        self.player.max_health = 1 + self.permanent_bonus["max_health"] + self.equipment_bonus["max_health"]
        self.player.health = self.player.max_health
        self.player.base_speed = PLAYER_SPEED + self.permanent_bonus["speed"] + self.equipment_bonus["speed"]
        self.player.attack_speed = 5.0 + self.permanent_bonus["attack_speed"] + self.equipment_bonus["attack_speed"]
        self.harvest_bonus = self.equipment_bonus["harvest_bonus"]

        for i in range(WEAPON_COUNT):
            angle = (2 * math.pi / WEAPON_COUNT) * i
            self.weapons.append(Weapon(self.player, angle))
        
        self.camera.update(self.player.x, self.player.y)
        self.material_mgr.clear()
        self.game_over = False
        self.running = True
        self.spawner.last_spawn_time = pygame.time.get_ticks()  # 重置生成计时
        self.state = "playing"
        self.upgrade_options = []
        self.selected_upgrade = 0
    
    def get_material_value_for_biome(self, biome):
        mapping = {
            "rainforest": 5,
            "forest": 4,
            "grass": 3,
            "desert": 2,
            "tundra": 3,
            "ice": 4,
        }
        return mapping.get(biome, 3)
    
    def _get_nearest_interactable_deco(self, max_distance=50):
        """检测是否有可交互物"""
        nearest_dist_sq = max_distance * max_distance + 1
        nearest_deco = None
        px, py = self.player.x, self.player.y
        for deco in self.decoration_objects:
            dx = px - deco.x
            dy = py - deco.y
            dist_sq = dx*dx + dy*dy
            if dist_sq < nearest_dist_sq:
                nearest_dist_sq = dist_sq
                nearest_deco = deco
        if nearest_dist_sq <= max_distance * max_distance:
            return (nearest_dist_sq**0.5, nearest_deco)
        return (None, None)
    
    def _persist_materials(self):
        """将当前材料库存保存到全局存档"""
        save_data = self.save_mgr.load()
        current_inv = self.material_mgr.inventory
        global_inv = save_data.get("inventory", {})

        # 合并材料（本场获得 + 已有）
        for item_id, amount in current_inv.items():
            global_inv[item_id] = global_inv.get(item_id, 0) + amount

        save_data["inventory"] = global_inv
        save_data["materials"] = sum(global_inv.values())  # 可选，保留总价值字段
        self.save_mgr.save(save_data)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if self.backpack_ui.visible:
                self.backpack_ui.handle_events([event])
                return
            if self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:            
                save_data = self.save_mgr.load()
                old_inv = save_data.get("inventory", {})
                new_inv = self.material_mgr.get_inventory()
                old_inv.update(new_inv)
                save_data["inventory"] = old_inv
                self.save_mgr.save(save_data)

                self.exit_to_camp = True
                # self.reset()
            # 升级事件
            if self.state == "upgrading" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_upgrade = (self.selected_upgrade - 1) % len(self.upgrade_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_upgrade = (self.selected_upgrade + 1) % len(self.upgrade_options)
                elif event.key == pygame.K_RETURN:
                    upgrade = self.upgrade_options[self.selected_upgrade]
                    self.upgrade_mgr.apply_upgrade(self.player, self.weapons, upgrade)
                    self.state = "playing"
                    self.upgrade_options = []

            if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                self.backpack_ui.toggle()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                for deco in self.decoration_objects[:]:
                    dx = self.player.x - deco.x
                    dy = self.player.y - deco.y
                    if (dx**2 + dy**2)**0.5 < 50:
                        # material_value = self.get_material_value_for_biome(deco.biome)
                        # self.material_mgr.add_material(deco.x, deco.y, value=material_value)
                        self.material_mgr.add_material(deco.x, deco.y, deco.drop_item, deco.drop_amount)
                        self.decoration_objects.remove(deco)
                        break
            """
            # 营地事件
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b and self.state != "upgrading" and not self.game_over:
                save_data = self.save_mgr.load()
                save_data["materials"] += self.material_mgr.materials_value  # 累计材料
                self.save_mgr.save(save_data)
                self.return_to_camp()
            """
    
    def wants_to_exit_to_camp(self):
        return self.exit_to_camp

    def update(self):
        if self.game_over:
            return
        if self.state == "upgrading" or self.backpack_ui.visible:
            return

        # 移动玩家
        dx, dy = self.input_mgr.get_movement()
        self.player.move(dx, dy)

        # 移动视角
        self.camera.update(self.player.x, self.player.y)

        dt = self.clock.get_time() / 1000.0

        # 更新武器旋转
        for w in self.weapons:
            w.update(dt)

        # 生成敌人
        self.spawner.update(self.enemies, self.player.x, self.player.y, self.world_width, self.world_height)

        # 更新敌人位置
        for enemy in self.enemies[:]:
            enemy.update(self.player.x, self.player.y)
            if enemy.is_off_screen():
                self.enemies.remove(enemy)

        # 碰撞
        self.collision_mgr.handle_weapon_enemy_collisions(self.weapons, self.enemies)

        # 敌人死亡掉落经验球
        for enemy in self.enemies[:]:
            if enemy.dead:
                self.exp_mgr.add_orb(enemy.x, enemy.y, value=10)
                self.material_mgr.add_material(enemy.x, enemy.y, item_id="scrap", amount=MATERIAL_DROP_VALUE)
                self.enemies.remove(enemy)
                # print("敌人死亡，生成经验球")

        # 碰撞 玩家/敌人
        if self.collision_mgr.handle_player_enemy_collisions(self.player, self.enemies):
            # 死亡保存本局收集的材料到存档
            # save_data = self.save_mgr.load()
            # save_data["materials"] += self.material_mgr.materials_value
            # self.save_mgr.save(save_data)
            self._persist_materials()
            self.game_over = True
            return
        
        # 经验球吸引与拾取
        collected = self.exp_mgr.update_orbs(self.player.x, self.player.y, dt)
        if collected > 0:
            leveled = self.exp_mgr.add_experience(collected)
            if leveled:
                self.upgrade_options = self.upgrade_mgr.get_random_upgrades(3)
                self.selected_upgrade = 0
                self.state = "upgrading"
        
        # 材料拾取
        collected_material = self.material_mgr.update(self.player.x, self.player.y, dt)
        if collected_material:
            total_gained = sum(collected_material.values())
            if not hasattr(self.material_mgr, 'materials_value'):
                self.material_mgr.materials_value = 0
            self.material_mgr.materials_value += total_gained

        # 更新玩家无敌计时
        self.player.update()

    def draw(self):
        self.screen.fill(BLACK)
        if self.game_over:
            self.ui.draw_game_over(self.screen)

        elif self.state == "playing":
            # 绘制地形
            visible_rect = self.camera.get_visible_rect()
            start_tile_x = visible_rect.left // TILE_SIZE
            end_tile_x = (visible_rect.right + TILE_SIZE - 1) // TILE_SIZE
            start_tile_y = visible_rect.top // TILE_SIZE
            end_tile_y = (visible_rect.bottom + TILE_SIZE - 1) // TILE_SIZE
            for tile_y in range(start_tile_y, end_tile_y + 1):
                for tile_x in range(start_tile_x, end_tile_x + 1):
                    self.map_gen.draw_tile(self.screen, tile_x, tile_y, visible_rect)

            # 绘制交互物
            for deco in self.decoration_objects:
                deco.draw(self.screen, self.camera)

            # 绘制敌人
            for enemy in self.enemies:
                # enemy.draw(self.screen)
                screen_x, screen_y = self.camera.apply(enemy.x, enemy.y)
                enemy.draw(self.screen, screen_x, screen_y)

            # 绘制武器
            for weapon in self.weapons:
                # weapon.draw(self.screen)
                wx, wy = weapon.get_position()
                screen_x, screen_y = self.camera.apply(wx, wy)
                weapon.draw(self.screen, screen_x, screen_y)
            
            # 绘制角色
            # self.player.draw(self.screen)
            screen_x, screen_y = self.camera.apply(self.player.x, self.player.y)
            self.player.draw(self.screen, screen_x, screen_y)

            # 绘制经验
            for orb in self.exp_mgr.orbs:
                # orb.draw(self.screen)
                screen_x, screen_y = self.camera.apply(orb.x, orb.y)
                orb.draw(self.screen, screen_x, screen_y)
            
            # 绘制材料
            # self.material_mgr.draw(self.screen)
            self.material_mgr.draw(self.screen, self.camera)

            # 绘制ui
            self.ui.draw_game_ui(self.screen, self.player.health, len(self.enemies))
            
            """
            # 材料数量
            if hasattr(self.material_mgr, 'materials_value'):
                mat_text = self.font.render(f"材料: {self.material_mgr.materials_value}", True, (255,215,0))
                self.screen.blit(mat_text, (10, 90))
            
            wood_count = self.material_mgr.get_material("wood")
            stone_count = self.material_mgr.get_material("stone")
            wood_text = self.font.render(f"木材: {wood_count}", True, (255,255,255))
            self.screen.blit(wood_text, (SCREEN_WIDTH-150, 40))
            stone_text = self.font.render(f"石头: {stone_count}", True, (255,255,255))
            self.screen.blit(stone_text, (SCREEN_WIDTH-150, 80))
            """

            # 经验条
            exp, next_exp = self.exp_mgr.get_level_progress()
            if next_exp > 0:
                bar_width = 200
                fill = int(bar_width * exp / next_exp)
                pygame.draw.rect(self.screen, (100,100,100), (SCREEN_WIDTH-210, 10, bar_width, 20))
                pygame.draw.rect(self.screen, (0,255,0), (SCREEN_WIDTH-210, 10, fill, 20))
                level_text = self.font.render(f"Lv.{self.exp_mgr.level}", True, (255,255,255))
                self.screen.blit(level_text, (SCREEN_WIDTH-210, 35))
            
            # 绘制交互提示
            dist, deco = self._get_nearest_interactable_deco()
            if deco:
                hint_text = self.font.render("按 E 采集", True, (255, 255, 255))
                text_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
                bg_rect = text_rect.inflate(20, 10)
                pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)  # 注意：pygame.draw.rect不支持alpha，需用surface
                s = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
                s.fill((0, 0, 0, 180))
                self.screen.blit(s, bg_rect.topleft)
                self.screen.blit(hint_text, text_rect)

            # 小地图
            if self.minimap:
                current_time = pygame.time.get_ticks() / 1000.0
                self.minimap.draw(self.screen)

        elif self.state == "upgrading":
            # 升级界面
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0,0,0))
            self.screen.blit(overlay, (0,0))

            for enemy in self.enemies:
                screen_x, screen_y = self.camera.apply(enemy.x, enemy.y)
                enemy.draw(self.screen, screen_x, screen_y)

            for weapon in self.weapons:
                wx, wy = weapon.get_position()
                screen_x, screen_y = self.camera.apply(wx, wy)
                weapon.draw(self.screen, screen_x, screen_y)

            screen_x, screen_y = self.camera.apply(self.player.x, self.player.y)
            self.player.draw(self.screen, screen_x, screen_y)

            for orb in self.exp_mgr.orbs:
                screen_x, screen_y = self.camera.apply(orb.x, orb.y)
                orb.draw(self.screen, screen_x, screen_y)
            
            self.material_mgr.draw(self.screen, self.camera)
            self.ui.draw_game_ui(self.screen, self.player.health, len(self.enemies))
            self.ui.draw_upgrade_menu(self.screen, self.upgrade_options, self.selected_upgrade)
        
        self.backpack_ui.draw()
        pygame.display.flip()

    """
    def run(self):
        print("游戏主循环开始")
        while self.running:
            print("循环中...")
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
    """