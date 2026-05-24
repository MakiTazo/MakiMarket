import asyncio
from endstone import Player, ColorFormat
from endstone.inventory import ItemStack

def process_buy_transaction(plugin, player: Player, item_id: str, amount: int, total_cost: float) -> None:
    async def _buy():
        api = plugin._economy_api
        uuid = str(player.unique_id)
        if not await api.has_balance(uuid, total_cost):
            player.send_message(f"{ColorFormat.RED}Not enough money! Need ${total_cost:.2f}")
            return
        item = ItemStack(item_id, amount)
        leftover = player.inventory.add_item(item)
        if leftover:
            player.send_message(f"{ColorFormat.RED}Not enough inventory space!")
            return
        await api.remove_balance(uuid, total_cost)
        item_name = item_id.replace('minecraft:', '').replace('_', ' ')
        player.send_message(f"{ColorFormat.GREEN}Bought {amount}x {item_name} for ${total_cost:.2f}")
    try:
        loop = asyncio.get_running_loop()
        asyncio.ensure_future(_buy())
    except RuntimeError:
        asyncio.run(_buy())

def process_sell_transaction(plugin, player: Player, sellable_items: dict, items_deposited: dict) -> None:
    async def _sell():
        sold_total = 0.0
        for item_id, amount in items_deposited.items():
            if item_id in sellable_items:
                sold_total += sellable_items[item_id] * amount

        if sold_total > 0:
            api = plugin._economy_api
            uuid = str(player.unique_id)
            await api.add_balance(uuid, sold_total)
            player.send_message(f"{ColorFormat.GREEN}Items sold! Earned: ${sold_total:.2f}")
        else:
            player.send_message(f"{ColorFormat.YELLOW}No items deposited for sale")

    try:
        loop = asyncio.get_running_loop()
        asyncio.ensure_future(_sell())
    except RuntimeError:
        asyncio.run(_sell())