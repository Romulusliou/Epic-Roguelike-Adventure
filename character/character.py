# character/character.py

import random  # 導入 random 模組，用於生成隨機數，例如閃避、格擋機率

player_hp = 100
player_max_hp = 100
player_level = 1
player_exp = 0
player_speed = 5
player_atk_cd = 200
player_last_attack_time = 0


class Player:
    """玩家角色屬性與狀態管理"""
    
    def __init__(self):
        """初始化玩家角色的各項屬性"""
        self.x = 960    # 預設位置 (1920x1080 的中間)
        self.y = 540
        self.size = 40  # 角色大小
        self.hp = 100   # 初始生命值
        self.max_hp = 100 # 最大生命值
        self.level = 1   # 初始等級
        self.exp = 0    # 初始經驗值
        self.hp_regen = 0     # 生命回復速度
        self.crit_rate = 0.0   # 暴擊率 (0.0 ~ 1.0)
        self.dodge_rate = 0.0  # 閃避率 (0.0 ~ 1.0)
        self.speed = 5    # 移動速度
        self.equipment = []     # 玩家裝備列表
        self.weapons = {"sword": True, "bullet": False}   # 初始擁有劍，未解鎖槍械

    def take_damage(self, damage):
        """玩家受到傷害（包含閃避 & 格擋計算）"""
        blocked = False  # 預設為未格擋
        dodged = False   # 預設為未閃避

        # 裝備效果：格擋
        # 檢查玩家是否裝備了 "Guardian Shield"
        if any(e["name"] == "Guardian Shield" for e in self.equipment):
            if random.random() < 0.5:  # 50% 機率格擋
                blocked = True

        # 裝備效果：閃避
        # 檢查玩家是否裝備了 "Wind Boots"
        if any(e["name"] == "Wind Boots" for e in self.equipment):
            if random.random() < 0.1:  # 10% 機率閃避
                dodged = True

        if dodged:
            return "dodge"  # 返回 "dodge" 表示成功閃避
        elif blocked:
            self.hp -= damage // 2   # 格擋減少 50% 傷害
            return "blocked"  # 返回 "blocked" 表示成功格擋
        else:
            self.hp -= damage   # 受到正常傷害
            return "hit"  # 返回 "hit" 表示受到正常傷害

    def gain_exp(self, amount):
        """玩家獲取經驗值"""
        self.exp += amount  # 增加經驗值
        required_exp = 30 * (self.level ** 2)  # 計算升級所需經驗值
        
        if self.exp >= required_exp:  # 檢查是否達到升級條件
            self.exp = 0   # 重置經驗值
            self.level += 1   # 等級提升
            return True   # 返回 True 表示等級提升
        return False   # 返回 False 表示未升級

    def reset(self):
        """重置玩家狀態（當玩家死亡後重開）"""
        self.__init__()  # 重新初始化玩家屬性

# 創建全局玩家對象
player = Player()