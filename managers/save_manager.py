import json
import os

SAVE_FILE = "data/save_data.json"

class SaveManager:
    @staticmethod
    def load():
        if not os.path.exists(SAVE_FILE):
            default_data = {
                "materials": 0,
                "buildings": {
                    "铁匠铺": 0,
                    "训练场": 0,
                    "魔法塔": 0,
                    "仓库": 0
                },
                "inventory": {
                    "scrap": 0,
                }
            }
            SaveManager.save(default_data)
            return default_data
        with open(SAVE_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save(data):
        os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)