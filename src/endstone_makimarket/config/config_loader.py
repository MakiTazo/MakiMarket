import yaml
from pathlib import Path

DEFAULT_CATEGORIES = {
    "blocks.yml": {
        "icon": "minecraft:grass_block",
        "slot": 11,
        "items": {
            "minecraft:dirt": {"buy_price": 1.0, "sell_price": 0.5},
            "minecraft:stone": {"buy_price": 2.0, "sell_price": 1.0},
            "minecraft:oak_log": {"buy_price": 3.0, "sell_price": 1.5}
        }
    },
    "ores.yml": {
        "icon": "minecraft:diamond",
        "slot": 12,
        "items": {
            "minecraft:iron_ingot": {"buy_price": 10.0, "sell_price": 5.0},
            "minecraft:gold_ingot": {"buy_price": 20.0, "sell_price": 10.0},
            "minecraft:diamond": {"buy_price": 100.0, "sell_price": 50.0}
        }
    },
    "food.yml": {
        "icon": "minecraft:golden_apple",
        "slot": 13,
        "items": {
            "minecraft:apple": {"buy_price": 5.0, "sell_price": 2.5},
            "minecraft:bread": {"buy_price": 8.0, "sell_price": 4.0}
        }
    }
}

def load_defaults(plugin_data_folder: str) -> None:
    market_path = Path(plugin_data_folder) / "categories"
    market_path.mkdir(parents=True, exist_ok=True)

    for filename, items in DEFAULT_CATEGORIES.items():
        file_path = market_path / filename
        if not file_path.exists():
            with open(file_path, 'w') as f:
                yaml.dump(items, f, default_flow_style=False, allow_unicode=True)