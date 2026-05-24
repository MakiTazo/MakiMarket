from endstone import Player, ColorFormat
from endstone.command import CommandSender
from endstone_makimarket.forms.sell_menu import open_sell_menu

command = {
    "sell": {
        "description": "Opens the sell menu to deposit items",
        "usages": ["/sell"],
        "permissions": ["endstone_makimarket.command.sell"],
    }
}

permissions = {
    "endstone_makimarket.command.sell": {
        "description": "Use /sell command",
        "default": "true",
    }
}


def handler(plugin, sender: CommandSender, args: list[str]) -> bool:
    if not isinstance(sender, Player):
        sender.send_error_message("Only players can use /sell")
        return True

    open_sell_menu(plugin, sender)
    return True