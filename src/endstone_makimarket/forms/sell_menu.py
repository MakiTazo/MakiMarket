from pathlib import Path
import yaml
from endstone import Player, ColorFormat
from jwinventoryapi import Menu, MenuType
from endstone_makimarket.utils import process_sell_transaction

def load_all_sellable_items(market_path: Path) -> dict:
    all_items = {}
    for file in market_path.glob("*.yml"):
        with open(file, 'r') as f:
            data = yaml.safe_load(f) or {}
            if "items" in data:
                items = data["items"]
            else:
                items = data
            for item_id, item_data in items.items():
                sell_price = item_data.get('sell_price', item_data.get('buy_price', 0) * 0.5)
                if sell_price > 0:
                    all_items[item_id] = sell_price
    return all_items

def open_sell_menu(plugin, player: Player) -> None:
    market_path = Path(plugin.data_folder) / "categories"
    sellable_items = load_all_sellable_items(market_path)
    if not sellable_items:
        player.send_message(f"{ColorFormat.RED}No sellable items configured in market!")
        return
    menu = Menu(MenuType.DOUBLE_CHEST, "§lSell Items")
    menu.set_editable(True)
    def on_close(pl: Player):
        process_sell_transaction(plugin, pl, sellable_items, menu.inventory)
    menu.set_close_listener(on_close)
    menu.send_to(player)