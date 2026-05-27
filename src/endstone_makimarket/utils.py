import asyncio
from endstone import Player, ColorFormat
from endstone.inventory import ItemStack

def process_buy_transaction(plugin, player: Player, item_id: str, amount: int, total_cost: float) -> None:
    async def _buy():
        api = plugin._economy_api
        uuid = str(player.unique_id)
        if not await api.has_balance(uuid, total_cost):
            player.play_sound(player.location, "mob.villager.no", volume=0.5, pitch=1.0)
            player.send_message(f"{ColorFormat.RED}Not enough money! Need ${total_cost:.2f}")
            return
        item = ItemStack(item_id, amount)
        leftover = player.inventory.add_item(item)
        if leftover:
            player.play_sound(player.location, "mob.villager.no", volume=0.5, pitch=1.0)
            player.send_message(f"{ColorFormat.RED}Not enough inventory space!")
            return
        await api.remove_balance(uuid, total_cost)
        item_name = item_id.replace('minecraft:', '').replace('_', ' ')
        player.play_sound(player.location, "random.orb", volume=0.5, pitch=1.0)
        player.send_message(f"{ColorFormat.GREEN}Bought {amount}x {item_name} for ${total_cost:.2f}")
    try:
        loop = asyncio.get_running_loop()
        asyncio.ensure_future(_buy())
    except RuntimeError:
        asyncio.run(_buy())

def process_sell_transaction(plugin, player: Player, sellable_items: dict, inventory) -> None:
    async def _sell():
        contents = inventory.contents
        sold_total = sum(
            sellable_items[item.type.id] * item.amount
            for item in contents
            if item and item.type.id in sellable_items
        )
        items_to_return = [
            item for item in contents
            if item and item.type.id not in sellable_items
        ]
        if items_to_return:
            inventory_full = False
            for item in items_to_return:
                if not inventory_full:
                    leftover = player.inventory.add_item(item)
                    if leftover:
                        inventory_full = True
                        for leftover_item in leftover:
                            player.world.drop_item(player.location, leftover_item)
                else:
                    player.world.drop_item(player.location, item)
        if sold_total > 0:
            api = plugin._economy_api
            uuid = str(player.unique_id)
            await api.add_balance(uuid, sold_total)
            player.play_sound(player.location, "random.orb", volume=0.5, pitch=1.0)
            player.send_message(f"{ColorFormat.GREEN}Items sold! Earned: ${sold_total:.2f}")
            if items_to_return:
                player.send_message(f"{ColorFormat.YELLOW}Some non-sellable items were returned to your inventory!")
        else:
            if items_to_return:
                player.play_sound(player.location, "mob.villager.no", volume=0.5, pitch=1.0)
                player.send_message(f"{ColorFormat.RED}No sellable items found! Non-sellable items returned.")
            else:
                player.send_message(f"{ColorFormat.YELLOW}No items found in the menu!")
    try:
        loop = asyncio.get_running_loop()
        asyncio.ensure_future(_sell())
    except RuntimeError:
        asyncio.run(_sell())