from pathlib import Path
from endstone import ColorFormat
from endstone.command import CommandSender
from endstone_makimarket.forms.shop_menu import _cache, _cache_time

command = {
    "shopreload": {
        "description": "Reloads all market configurations",
        "usages": ["/shopreload"],
        "permissions": ["endstone_makimarket.command.reload"],
    }
}

permissions = {
    "endstone_makimarket.command.reload": {
        "description": "Use /shopreload command",
        "default": "op",
    }
}

def handler(plugin, sender: CommandSender, args: list[str]) -> bool:
    if not sender.has_permission("endstone_makimarket.command.reload"):
        sender.send_message(f"{ColorFormat.RED}You don't have permission to reload the market!")
        return True
    _cache.clear()
    _cache_time.clear()
    market_path = Path(plugin.data_folder) / "categories"
    if market_path.exists():
        sender.send_message(f"{ColorFormat.GREEN}Market reloaded successfully!")
        plugin.logger.info(f"Market reloaded by {sender.name}")
    else:
        sender.send_message(f"{ColorFormat.YELLOW}Market folder not found, but cache cleared.")
    return True