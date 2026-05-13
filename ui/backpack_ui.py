import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, MATERIAL_NAMES
from formula import EQUIPMENTS

class BackpackUI:
    def __init__(self, screen, font, material_manager, equipment_manager):
        self.screen = screen
        self.font = font
        self.material_mgr = material_manager
        self.equip_mgr = equipment_manager
        self.visible = False

    def toggle(self):
        self.visible = not self.visible

    def handle_events(self, events):
        if not self.visible:
            return
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:   # 按U关闭背包
                    self.toggle()
                # 未来可添加上下选择等

    def draw(self):
        if not self.visible:
            return
        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # 标题
        title = self.font.render("背包", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 60))
        self.screen.blit(title, title_rect)

        # 材料显示
        left_title = self.font.render("材料", True, (255, 255, 0))
        self.screen.blit(left_title, (50, 80))
        y = 120
        inventory = self.material_mgr.inventory
        if not inventory:
            empty_text = self.font.render("暂无材料", True, (200, 200, 200))
            self.screen.blit(empty_text, (50, y))
        else:
            for item_id, count in inventory.items():
                if count == 0:
                    continue
                name = MATERIAL_NAMES.get(item_id, item_id)
                text = self.font.render(f"{name}: {count}", True, (255, 255, 255))
                self.screen.blit(text, (70, y))
                y += 30

        # 装备显示
        right_title = self.font.render("已装备", True, (255, 255, 0))
        self.screen.blit(right_title, (SCREEN_WIDTH // 2 + 50, 80))
        equipped = self.equip_mgr.equipped_items if self.equip_mgr else []
        if not equipped:
            no_equip_text = self.font.render("无", True, (200, 200, 200))
            self.screen.blit(no_equip_text, (SCREEN_WIDTH // 2 + 70, 120))
        else:
            y = 120
            for item_id in equipped:
                item = EQUIPMENTS.get(item_id, {})
                name = item.get("name", item_id)
                effect = item.get("effect", {})
                effect_str = ", ".join([f"{stat}+{val}" for stat, val in effect.items()])
                text = self.font.render(f"{name}  ({effect_str})", True, (255, 255, 255))
                self.screen.blit(text, (SCREEN_WIDTH // 2 + 70, y))
                y += 30

        # 提示关闭
        hint = self.font.render("按 U 键关闭", True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)