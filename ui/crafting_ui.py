import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, MATERIAL_NAMES
from formula import RECIPES, CATEGORY_NAMES, CATEGORY_ORDER
from managers.save_manager import SaveManager

class CraftingUI:
    def __init__(self, screen, font, inventory_manager):
        self.screen = screen
        self.font = font
        self.inv_mgr = inventory_manager
        self.save_data = SaveManager.load()
        self.visible = False

        # 类别
        self.categories = [cat for cat in CATEGORY_ORDER if any(
            r["category"] == cat for r in RECIPES.values())]
        self.selected_category_idx = 0
        self.selected_recipe_idx = 0

        # 类别下的配方
        self.current_recipes = []
        self._refresh_recipe_list()

    def _refresh_recipe_list(self):
        """根据当前选中的类别，更新配方列表"""
        current_category = self.categories[self.selected_category_idx]
        self.current_recipes = [
            (rid, rec) for rid, rec in RECIPES.items() if rec["category"] == current_category
        ]
        self.selected_recipe_idx = 0
        if not self.current_recipes:
            self.selected_recipe_idx = -1

    def toggle(self):
        self.visible = not self.visible
        if self.visible:
            self.selected_category_idx = 0
            self._refresh_recipe_list()
        else:
            pass

    def handle_events(self, events):
        if not self.visible:
            return
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.toggle()
                # 切换类别
                elif event.key == pygame.K_LEFT:
                    self.selected_category_idx = (self.selected_category_idx - 1) % len(self.categories)
                    self._refresh_recipe_list()
                elif event.key == pygame.K_RIGHT:
                    self.selected_category_idx = (self.selected_category_idx + 1) % len(self.categories)
                    self._refresh_recipe_list()
                # 选择配方
                elif event.key == pygame.K_UP:
                    if self.current_recipes:
                        self.selected_recipe_idx = (self.selected_recipe_idx - 1) % len(self.current_recipes)
                elif event.key == pygame.K_DOWN:
                    if self.current_recipes:
                        self.selected_recipe_idx = (self.selected_recipe_idx + 1) % len(self.current_recipes)
                # 合成
                elif event.key == pygame.K_RETURN:
                    self.craft()

    def craft(self):
        if self.selected_recipe_idx < 0 or not self.current_recipes:
            return
        recipe_id, recipe = self.current_recipes[self.selected_recipe_idx]
        materials = recipe["materials"]
        # 检查材料是否够
        for mat_id, need in materials.items():
            if self.inv_mgr.get_material(mat_id) < need:
                # 材料不足
                print(f"材料不足: {MATERIAL_NAMES.get(mat_id, mat_id)}")
                return
        # 扣除材料
        for mat_id, need in materials.items():
            self.inv_mgr.deduct_material(mat_id, need)
        # 添加产物
        result_amount = recipe["result_amount"]
        self.inv_mgr.add_material(None, None, recipe_id, result_amount)  # 直接加库存
        self.save_data["inventory"] = self.inv_mgr.inventory
        SaveManager.save(self.save_data)
        print(f"合成成功: {recipe['name']} x{result_amount}")

    def draw(self):
        if not self.visible:
            return
        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # 标题
        title = self.font.render("合成台 (ESC关闭)", True, (255,255,255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(title, title_rect)

        # 左侧：类别列表
        left_panel_rect = pygame.Rect(30, 80, 200, SCREEN_HEIGHT - 160)
        pygame.draw.rect(self.screen, (40,40,40), left_panel_rect)
        pygame.draw.rect(self.screen, (100,100,100), left_panel_rect, 2)

        y = left_panel_rect.y + 10
        for i, cat in enumerate(self.categories):
            color = (255,255,0) if i == self.selected_category_idx else (200,200,200)
            cat_name = CATEGORY_NAMES.get(cat, cat)
            text = self.font.render(cat_name, True, color)
            self.screen.blit(text, (left_panel_rect.x + 10, y))
            y += 40

        # 右侧：配方列表
        right_panel_rect = pygame.Rect(260, 80, 400, SCREEN_HEIGHT - 160)
        pygame.draw.rect(self.screen, (40,40,40), right_panel_rect)
        pygame.draw.rect(self.screen, (100,100,100), right_panel_rect, 2)

        # 显示类别名称
        current_cat = self.categories[self.selected_category_idx]
        cat_title = self.font.render(CATEGORY_NAMES.get(current_cat, current_cat), True, (255,255,255))
        self.screen.blit(cat_title, (right_panel_rect.x + 10, right_panel_rect.y + 5))

        # 显示配方列表
        y = right_panel_rect.y + 50
        for idx, (rid, recipe) in enumerate(self.current_recipes):
            color = (255,255,0) if idx == self.selected_recipe_idx else (255,255,255)
            name_text = self.font.render(recipe["name"], True, color)
            self.screen.blit(name_text, (right_panel_rect.x + 10, y))
            # 显示所需材料
            mats_text = ", ".join([f"{MATERIAL_NAMES.get(mid, mid)} x{num}" for mid, num in recipe["materials"].items()])
            small_font = pygame.font.SysFont('simhei', 16)
            mats_surf = small_font.render(mats_text, True, (150,150,150))
            self.screen.blit(mats_surf, (right_panel_rect.x + 150, y + 5))
            y += 40

        # 操作提示
        hint = self.font.render("←/→ 切类别  ↑/↓ 选配方  Enter 合成  ESC 关闭", True, (200,200,200))
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(hint, hint_rect)