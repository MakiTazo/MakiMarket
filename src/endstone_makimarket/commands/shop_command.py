from endstone import Player
from endstone.command import CommandSender
from endstone_makimarket.forms.shop_menu import open_shop_menu

command = {
    "shop": {
        "description": "Opens the shop GUI",
        "usages": [
            "/shop"
        ],
        "permissions": ["endstone_makimarket.command.shop"],
    }
}

permissions = {
    "endstone_makimarket.command.shop": {
        "description": "Use /shop command",
        "default": "true",
    }
}

def handler(plugin, sender: CommandSender, args) -> bool:
    if not isinstance(sender, Player):
        sender.send_error_message("Only players can use /shop")
        return True
    open_shop_menu(plugin, sender)
    return True