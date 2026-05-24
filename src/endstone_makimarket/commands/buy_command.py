from pathlib import Path
import yaml
from endstone import Player, ColorFormat
from endstone.command import CommandSender
from endstone_makimarket.utils import process_buy_transaction

command = {
    "buy": {
        "description": "Buys an item from the market",
        "usages": ["/buy <item> [amount]"],
        "permissions": ["endstone_makimarket.command.buy"],
    }
}

permissions = {
    "endstone_makimarket.command.buy": {
        "description": "Use /buy command",
        "default": "true",
    }
}


def load_all_items(market_path: Path) -> dict:
    all_items = {}
    for file in market_path.glob("*.yml"):
        with open(file, 'r') as f:
            data = yaml.safe_load(f) or {}
            if "items" in data:
                items = data["items"]
            else:
                items = data
            all_items.update(items)
    return all_items


def find_item(all_items: dict, search: str) -> str | None:
    search = search.lower().replace('minecraft:', '')
    for item_id in all_items:
        if item_id.lower().replace('minecraft:', '') == search:
            return item_id
    matches = []
    for item_id in all_items:
        if search in item_id.lower().replace('minecraft:', ''):
            matches.append(item_id)
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        return matches
    return None


def handler(plugin, sender: CommandSender, args: list[str]) -> bool:
    if not isinstance(sender, Player):
        sender.send_error_message("Only players can use /buy")
        return True

    if not args:
        sender.send_message(f"{ColorFormat.RED}Usage: /buy <item> [amount]")
        return True

    market_path = Path(plugin.data_folder) / "market"
    all_items = load_all_items(market_path)
    if not all_items:
        sender.send_message(f"{ColorFormat.RED}No items in market!")
        return True

    search = args[0]
    result = find_item(all_items, search)
    if not result:
        sender.send_message(f"{ColorFormat.RED}Item '{search}' not found in market")
        return True
    if isinstance(result, list):
        matches = [item.replace('minecraft:', '') for item in result[:10]]
        sender.send_message(f"{ColorFormat.YELLOW}Multiple matches: {', '.join(matches)}")
        sender.send_message(f"{ColorFormat.YELLOW}Be more specific!")
        return True

    item_id = result
    item_data = all_items[item_id]
    buy_price = item_data.get('buy_price', item_data.get('price', 0))
    amount = 1
    if len(args) >= 2:
        try:
            amount = int(args[1])
            if amount < 1 or amount > 64:
                sender.send_message(f"{ColorFormat.RED}Amount must be between 1 and 64")
                return True
        except ValueError:
            sender.send_message(f"{ColorFormat.RED}Invalid amount: {args[1]}")
            return True

    total_cost = buy_price * amount
    process_buy_transaction(plugin, sender, item_id, amount, total_cost)
    return True