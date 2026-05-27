from pathlib import Path
import yaml
from endstone import Player, ColorFormat
from endstone.inventory import ItemStack
from jwinventoryapi import Menu, MenuType
from endstone_makimarket.utils import process_buy_transaction

# Caché global
_cache = {}
_cache_time = {}
_player_menus = {}

def load_category_items(market_path: Path, category_name: str) -> dict:
    file_path = market_path / f"{category_name}.yml"
    if not file_path.exists():
        return {}
    mtime = file_path.stat().st_mtime
    cache_key = str(file_path)
    if cache_key in _cache and _cache_time.get(cache_key) == mtime:
        return _cache[cache_key]
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f) or {}
        if "items" in data:
            items = data["items"]
        else:
            items = data
    _cache[cache_key] = items
    _cache_time[cache_key] = mtime
    return items

def make_item(item_id: str, name: str = None, lore: list[str] = None) -> ItemStack:
    try:
        item = ItemStack(item_id)
    except RuntimeError:
        item = ItemStack("minecraft:barrier")
        if name:
            name = f"§c[ERROR] {name}"
    if name or lore:
        meta = item.item_meta
        if name:
            meta.display_name = name
        if lore:
            meta.lore = lore
        item.set_item_meta(meta)
    return item

def play_click_sound(player: Player):
    player.play_sound(player.location, "random.click", volume=0.5, pitch=1.0)

def open_shop_menu(plugin, player: Player) -> None:
    market_path = Path(plugin.data_folder) / "categories"
    categories = []
    for f in market_path.glob("*.yml"):
        with open(f, 'r') as file:
            data = yaml.safe_load(file) or {}
            cat_data = {
                "name": f.stem,
                "icon": data.get("icon", "minecraft:chest"),
                "slot": data.get("slot", 0),
                "file": f
            }
            categories.append(cat_data)
    categories.sort(key=lambda x: x["slot"])
    menu = Menu(MenuType.CHEST, "§lMaki Market - Categories")
    _player_menus[player.unique_id] = menu
    for cat in categories:
        slot = cat["slot"]
        if slot > 26:
            continue
        item = make_item(cat["icon"], f"§e{cat['name'].replace('_', ' ').title()}")
        menu.set_item(slot, item, on_click=make_category_callback(plugin, cat["name"]))
    close_item = make_item("minecraft:barrier", "§cClose")
    menu.set_item(26, close_item, on_click=make_close_callback())
    menu.send_to(player)

def make_category_callback(plugin, category_name: str):
    def callback(player: Player, slot: int, item: ItemStack, inventory):
        play_click_sound(player)
        current_menu = _player_menus.get(player.unique_id)
        if current_menu:
            current_menu.close(player)
        open_category_menu(plugin, player, category_name)
        return True
    return callback

def make_close_callback():
    def callback(player: Player, slot: int, item: ItemStack, inventory):
        play_click_sound(player)
        menu = _player_menus.pop(player.unique_id, None)
        if menu:
            menu.close(player)
        return True
    return callback


def get_category_icon(category: str) -> str:
    icons = {
        "blocks": "minecraft:grass_block",
        "ores": "minecraft:diamond",
        "food": "minecraft:golden_apple",
        "tools": "minecraft:diamond_pickaxe",
        "items": "minecraft:arrow"
    }
    return icons.get(category, "minecraft:chest")

def open_category_menu(plugin, player: Player, category_name: str) -> None:
    market_path = Path(plugin.data_folder) / "categories"
    items = load_category_items(market_path, category_name)
    if not items:
        player.send_message(f"{ColorFormat.RED}No items in {category_name}")
        return
    item_count = len(items)
    max_slots = 54 if item_count > 26 else 27
    menu_type = MenuType.DOUBLE_CHEST if item_count > 26 else MenuType.CHEST
    title = f"§l{category_name.replace('_', ' ').title()}"
    menu = Menu(menu_type, title)
    _player_menus[player.unique_id] = menu
    for i, (item_id, data) in enumerate(items.items()):
        if i >= max_slots - 1:
            break
        buy_price = data.get('buy_price', data.get('price', 0))
        item = make_item(
            item_id,
            f"§f{item_id.replace('minecraft:', '').replace('_', ' ').title()}",
            [f"§aBuy: ${buy_price:.2f}", "", "§7Click to purchase"]
        )
        menu.set_item(i, item, on_click=make_transaction_callback(plugin, item_id, data, category_name))
    back_item = make_item("minecraft:arrow", "§eBack to Categories")
    menu.set_item(max_slots - 1, back_item, on_click=make_back_callback(plugin))
    menu.send_to(player)

def make_transaction_callback(plugin, item_id: str, item_data: dict, category_name: str):
    def callback(player: Player, slot: int, item: ItemStack, inventory):
        play_click_sound(player)
        current_menu = _player_menus.get(player.unique_id)
        if current_menu:
            current_menu.close(player)
        open_transaction_menu(plugin, player, item_id, item_data, category_name)
        return True
    return callback

def make_back_callback(plugin):
    def callback(player: Player, slot: int, item: ItemStack, inventory):
        play_click_sound(player)
        current_menu = _player_menus.get(player.unique_id)
        if current_menu:
            current_menu.close(player)
        open_shop_menu(plugin, player)
        return True
    return callback

def open_transaction_menu(plugin, player: Player, item_id: str, item_data: dict, category_name: str) -> None:
    buy_price = item_data.get('buy_price', item_data.get('price', 0))
    item_name = item_id.replace('minecraft:', '').replace('_', ' ').title()
    menu = Menu(MenuType.HOPPER, f"§lBuy {item_name}")
    _player_menus[player.unique_id] = menu
    buy1 = make_item("minecraft:lime_concrete", "§aBuy 1", [f"§7Cost: ${buy_price:.2f}"])
    menu.set_item(0, buy1, on_click=make_buy_callback(plugin, item_id, 1, buy_price, item_data, category_name))
    buy16 = make_item("minecraft:green_concrete", "§aBuy 16", [f"§7Cost: ${buy_price * 16:.2f}"])
    menu.set_item(1, buy16, on_click=make_buy_callback(plugin, item_id, 16, buy_price * 16, item_data, category_name))
    buy32 = make_item("minecraft:cyan_concrete", "§aBuy 32", [f"§7Cost: ${buy_price * 32:.2f}"])
    menu.set_item(2, buy32, on_click=make_buy_callback(plugin, item_id, 32, buy_price * 32, item_data, category_name))
    buy64 = make_item("minecraft:blue_concrete", "§aBuy 64", [f"§7Cost: ${buy_price * 64:.2f}"])
    menu.set_item(3, buy64, on_click=make_buy_callback(plugin, item_id, 64, buy_price * 64, item_data, category_name))
    back = make_item("minecraft:arrow", "§eBack")
    menu.set_item(4, back, on_click=make_category_callback(plugin, category_name))
    menu.send_to(player)

def make_buy_callback(plugin, item_id: str, amount: int, total_cost: float, item_data: dict, category_name: str):
    def callback(player: Player, slot: int, item: ItemStack, inventory):
        process_buy_transaction(plugin, player, item_id, amount, total_cost)
        return True
    return callback