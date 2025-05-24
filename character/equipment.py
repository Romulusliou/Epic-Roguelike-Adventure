# character/equipment.py
from ui.ui import add_floating_text

player_equipment = []  # 玩家裝備列表
equipment_icons = {
    "Flame Sword": "🔥🗡️",
    "Explosive Shotgun": "💣🔫",
    "Guardian Shield": "🛡️",
    "Wind Boots": "💨👟",
    "Energy Core": "⚛️"
}
equipment_descriptions = {
    "Flame Sword": "+10 ATK",
    "Explosive Shotgun": "Splash DMG",
    "Guardian Shield": "+20 DEF",
    "Wind Boots": "+2 SPD",
    "Energy Core": "CD -10%"
}


class Equipment:
    """裝備系統 - 管理所有裝備 & 其效果"""
    def __init__(self):
        self.equipped_items = {}

    def equip(self, item_name):
        """裝備道具"""
        self.equipped_items[item_name] = True

    def is_equipped(self, item_name):
        """檢查裝備是否啟用"""
        return self.equipped_items.get(item_name, False)

    def apply_effects(self, player, enemies):
        """套用裝備效果"""
        if self.is_equipped("Flame Sword"):
            player.sword_has_fire = True

        if self.is_equipped("Explosive Shotgun"):
            for enemy in enemies:
                if enemy.is_hit_by_bullet():
                    enemy.hp -= 10  # 額外範圍傷害
                    add_floating_text("💥 Explosion!", (enemy.x, enemy.y), 800)

        if self.is_equipped("Guardian Shield"):
            player.block_chance = 0.5  # 50% 擋傷害

        if self.is_equipped("Wind Boots"):
            player.speed *= 1.15  # 移動速度 +15%
            player.dodge_chance = 0.1  # 10% 閃避敵人攻擊

        if self.is_equipped("Energy Core"):
            from pygame.time import get_ticks
            if get_ticks() % 10000 < 100:  # 每 10 秒觸發
                for enemy in enemies:
                    if enemy.distance_to(player) < 150:
                        enemy.hp -= 50
                        add_floating_text("⚡ Electric Shock!", (enemy.x, enemy.y), 1000)

# 創建全域裝備管理器
player_equipment = Equipment()
