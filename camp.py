import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, BUILDING_PRICES, BUILDING_EFFECTS, MATERIAL_NAMES
from world.camp_map import CampMap, BUILDINGS_POS, CAMP_WIDTH, CAMP_HEIGHT, WORKBENCH_POS
from managers.save_manager import SaveManager
from managers.input_manager import InputManager
from managers.material_manager import MaterialManager
from managers.equipment_manager import EquipmentManager
from world.camera import Camera
from entities.player import Player
from ui.crafting_ui import CraftingUI
from ui.equipment_ui import EquipmentUI

class Camp:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.save_data = SaveManager.load()
        
        self.inventory = self.save_data.get("inventory", {}) 
        # self.materials = self.save_data["materials"]
        self.materials = self.inventory.get("scrap", 0)
        self.buildings = self.save_data["buildings"]
        self.inv_mgr = MaterialManager()
        self.inv_mgr.from_dict(self.inventory)
        self.crafting_ui = CraftingUI(screen, font, self.inv_mgr)

        self.equip_mgr = EquipmentManager(self.inv_mgr)
        self.equip_mgr.from_dict(self.save_data)
        self.equipment_ui = EquipmentUI(screen, font, self.inv_mgr, self.equip_mgr)

        self.running = True
        self.quit_to_exit = False

        self.camp_map = CampMap()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, CAMP_WIDTH, CAMP_HEIGHT)
        self.player = Player(CAMP_WIDTH // 2, CAMP_HEIGHT // 2)
        self.player.base_speed = 8
        self.input_mgr = InputManager()
        self.workbench_pos = (CAMP_WIDTH - 150, CAMP_HEIGHT // 2)

        self.near_building = None
        self.near_workbench = False
        self.show_upgrade_ui = None
        self.selected_building_name = None
        

    def handle_events(self, events):
        # 处理合成
        if self.crafting_ui.visible:
            self.crafting_ui.handle_events(events)
            return
        
        # 处理装备
        if self.equipment_ui.visible:
            self.equipment_ui.handle_events(events)
            self.save_data.update(self.equip_mgr.to_dict())
            SaveManager.save(self.save_data)
            return
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                self.quit_to_exit = True
            """
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_building = (self.selected_building - 1) % len(BUILDING_PRICES)
                elif event.key == pygame.K_DOWN:
                    self.selected_building = (self.selected_building + 1) % len(BUILDING_PRICES)
                elif event.key == pygame.K_RETURN:
                    self.try_upgrade()
                elif event.key == pygame.K_b:  # 按B键返回战斗
                    self.running = False
            """
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and self.near_building:
                    # 升级面板
                    self.selected_building_name = self.near_building
                    self.show_upgrade_ui = True
                if self.show_upgrade_ui and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        pass
                    elif event.key == pygame.K_RETURN:
                        self.try_upgrade()
                        self.show_upgrade_ui = False
                    elif event.key == pygame.K_ESCAPE:
                        self.show_upgrade_ui = False
                if event.key == pygame.K_b and not self.show_upgrade_ui:
                    self.running = False
                if event.key == pygame.K_e and self.near_workbench:
                    # 合成界面
                    self.crafting_ui.toggle()
                if event.key == pygame.K_i:
                    # 装备界面
                    self.equipment_ui.toggle()


    def try_upgrade(self):
        if not self.selected_building_name:
            return
        building_name = self.selected_building_name
        current_level = self.buildings[building_name]
        if current_level >= len(BUILDING_PRICES[building_name]):
            # 满级处理
            return
        cost = BUILDING_PRICES[building_name][current_level]
        if self.materials >= cost:
            self.materials -= cost
            self.buildings[building_name] += 1
            # 保存数据
            # self.save_data["materials"] = self.materials
            self.inventory["scrap"] = self.materials
            self.save_data["buildings"] = self.buildings
            SaveManager.save(self.save_data)
    
    def update(self):
        if self.show_upgrade_ui or (self.crafting_ui and self.crafting_ui.visible):
            # 升级界面时暂停移动
            return

        # 移动玩家
        dx, dy = self.input_mgr.get_movement()
        self.player.move(dx, dy)
        # 相机跟随玩家
        self.camera.update(self.player.x, self.player.y)

        # 检测与建筑的接近程度
        self.near_building = None
        for name, pos in BUILDINGS_POS.items():
            # 计算玩家到建筑的距离
            dx = self.player.x - pos[0]
            dy = self.player.y - pos[1]
            dist = (dx**2 + dy**2)**0.5
            if dist < 50:  # 交互半径
                self.near_building = name
                break
        
        for name, pos in WORKBENCH_POS.items():
            wx, wy = pos[0], pos[1]
            dist_sq = (self.player.x - wx)**2 + (self.player.y - wy)**2
            self.near_workbench = (dist_sq < 60*60)

    def draw(self):
        self.screen.fill(BLACK)

        # 绘制地图（背景+建筑标记）
        self.camp_map.draw(self.screen, self.camera)
        # 绘制玩家
        screen_x, screen_y = self.camera.apply(self.player.x, self.player.y)
        self.player.draw(self.screen, screen_x, screen_y)

        # 绘制UI
        # 材料显示
        # mat_text = self.font.render(f"废旧零件(升级材料): {self.materials}", True, (255,215,0))
        # self.screen.blit(mat_text, (20, 20))
        panel_width = 220
        panel_height = len(self.inv_mgr.inventory) * 30 + 50
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surf.fill((0, 0, 0, 180))
        self.screen.blit(panel_surf, (SCREEN_WIDTH - panel_width - 10, 10))

        title = self.font.render("营地库存", True, (255,255,255))
        self.screen.blit(title, (SCREEN_WIDTH - panel_width, 20))

        y = 60
        for item_id, count in self.inv_mgr.inventory.items():
            if count == 0:
                continue
            name = MATERIAL_NAMES.get(item_id, item_id)
            text = self.font.render(f"{name}: {count}", True, (255,255,255))
            self.screen.blit(text, (SCREEN_WIDTH - panel_width + 10, y))
            y += 30

        # 提示信息
        if self.near_building and not self.show_upgrade_ui:
            hint = self.font.render(f"按 E 键升级 {self.near_building}", True, (255,255,255))
            self.screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT - 80))
            
        # 操作提示
        if not self.show_upgrade_ui:
            back_hint = self.font.render("按 B 键返回战斗", True, (200,200,200))
            self.screen.blit(back_hint, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 60))

        # 升级界面浮层
        if self.show_upgrade_ui and self.selected_building_name:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0,0,0))
            self.screen.blit(overlay, (0,0))
            # 显示升级信息
            building = self.selected_building_name
            current_level = self.buildings[building]
            from settings import BUILDING_PRICES, BUILDING_EFFECTS
            max_level = len(BUILDING_PRICES[building])
            if current_level < max_level:
                cost = BUILDING_PRICES[building][current_level]
                effect = BUILDING_EFFECTS[building]
                info = f"升级 {building} Lv.{current_level} -> Lv.{current_level+1}"
                cost_text = f"花费材料: {cost}"
                effect_text = f"效果: +{effect['value']} {effect['stat']}"
                confirm = "按回车确认升级，ESC取消"
                y = SCREEN_HEIGHT//2 - 60
                for line in [info, cost_text, effect_text, confirm]:
                    text_surf = self.font.render(line, True, (255,255,255))
                    self.screen.blit(text_surf, (SCREEN_WIDTH//2 - text_surf.get_width()//2, y))
                    y += 40
            else:
                text = self.font.render(f"{building} 已满级", True, (255,255,255))
                self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))

        #合成界面
        if self.near_workbench:
            hint = self.font.render("按 E 打开合成台", True, (255,255,0))
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 80))
            self.screen.blit(hint, hint_rect)
        if hasattr(self, 'crafting_ui') and self.crafting_ui.visible:
            self.crafting_ui.draw()
        
        # 装备界面
        if self.equipment_ui.visible:
            self.equipment_ui.draw()
        pygame.display.flip()