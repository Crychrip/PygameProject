import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from formula import EQUIPMENTS

class EquipmentUI:
    def __init__(self, screen, font, material_manager, equipment_manager):
        self.screen = screen
        self.font = font
        self.material_mgr = material_manager
        self.equip_mgr = equipment_manager
        self.visible = False
        self.selected_index = 0
        self.equippable_items = []   # 从库存中筛选出的可装备物品ID

    def refresh_items(self):
        """筛选库存中有的装备"""
        self.equippable_items = [
            item_id for item_id, count in self.material_mgr.inventory.items()
            if item_id in EQUIPMENTS and count > 0
        ]

    def toggle(self):
        self.visible = not self.visible
        if self.visible:
            self.refresh_items()
            self.selected_index = 0

    def handle_events(self, events):
        if not self.visible:
            return
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.toggle()
                elif event.key == pygame.K_UP:
                    if self.equippable_items:
                        self.selected_index = (self.selected_index - 1) % len(self.equippable_items)
                elif event.key == pygame.K_DOWN:
                    if self.equippable_items:
                        self.selected_index = (self.selected_index + 1) % len(self.equippable_items)
                elif event.key == pygame.K_e:
                    if self.equippable_items:
                        item_id = self.equippable_items[self.selected_index]
                        if item_id in self.equip_mgr.equipped_items:
                            self.equip_mgr.unequip(item_id)
                        else:
                            self.equip_mgr.equip(item_id)
                        self.refresh_items()
                elif event.key == pygame.K_RETURN:
                    self.toggle()

    def draw(self):
        if not self.visible:
            return
        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # 标题
        title = self.font.render("装备界面 (ESC关闭)", True, (255,255,255))
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 40))

        # 左侧：已装备物品
        left_title = self.font.render("已装备:", True, (255,255,0))
        self.screen.blit(left_title, (50, 100))
        y = 140
        for item_id in self.equip_mgr.equipped_items:
            name = EQUIPMENTS.get(item_id, {}).get("name", item_id)
            text = self.font.render(name, True, (200,200,200))
            self.screen.blit(text, (70, y))
            y += 30

        # 右侧：可装备物品列表
        right_title = self.font.render("可装备物品 (按E装备/卸下)", True, (255,255,255))
        self.screen.blit(right_title, (SCREEN_WIDTH//2, 100))
        y = 140
        for idx, item_id in enumerate(self.equippable_items):
            color = (255,255,0) if idx == self.selected_index else (255,255,255)
            item = EQUIPMENTS[item_id]
            name = item["name"]
            desc = item["description"]
            text = self.font.render(f"{name} - {desc}", True, color)
            self.screen.blit(text, (SCREEN_WIDTH//2, y))
            if item_id in self.equip_mgr.equipped_items:
                eq_text = self.font.render("[已装备]", True, (0,255,0))
                self.screen.blit(eq_text, (SCREEN_WIDTH//2 + 300, y))
            y += 40

        # 操作提示
        hint = self.font.render("↑/↓ 选择  E 装备/卸下  Enter/ESC 关闭", True, (200,200,200))
        self.screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT - 60))