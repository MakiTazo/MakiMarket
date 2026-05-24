# MakiMarket
A fully customizable Minecraft marketplace plugin for Endstone servers, featuring a graphical shop interface, buy/sell commands, and economy integration.

## Features
- **Graphical Shop Interface** - Browse items by category using an intuitive chest GUI
- **Buy & Sell System** - Purchase items from the market or sell items from your inventory
- **Economy Integration** - Works with JWEconomy for balance management
- **Category-based Organization** - Items organized into YAML files by category
- **Customizable Pricing** - Configure buy and sell prices per item (sell price = 5% of buy price by design)
- **Permission Support** - Granular control over who can use each command
- **Hot Reload** - Reload configuration without restarting the server

## Commands
| Command | Description | Permission |
|---------|-------------|------------|
| `/shop` | Opens the graphical shop menu | `endstone_makimarket.command.shop` |
| `/buy <item> [amount]` | Buys an item directly by name | `endstone_makimarket.command.buy` |
| `/sell` | Opens the sell interface | `endstone_makimarket.command.sell` |
| `/marketreload` | Reloads all market configurations | `endstone_makimarket.command.reload` |

## Installation
1. Ensure you have the following dependencies already installed in your server:
   - [JWEconomy](https://github.com/junggamyeon/JWEconomy)
   - [JWInventoryAPI](https://github.com/junggamyeon/JWInventoryAPI)
2. Place the WHL plugin in your `plugins/` folder
3. Restart your server or load the plugin using Endstone's plugin manager

## Configuration
### Category Files
Categories are defined as YAML files in the `market/` folder inside your plugin data directory. Each category file follows this structure:

```yaml
icon: "minecraft:grass_block"
slot: 11
items:
  "minecraft:dirt":
    buy_price: 0.50
    sell_price: 0.025
  "minecraft:stone":
    buy_price: 0.80
    sell_price: 0.04
```

### Parameters

- **icon** - The item ID used as the category icon in the shop menu
- **slot** - Inventory slot where the category icon appears (0-26 for chest, 0-53 for double chest)
- **items** - List of items in this category
  - **buy_price** - Price players pay to purchase this item
  - **sell_price** - Price players receive when selling this item

### Default Categories

The plugin generates default categories on first run:

- `blocks.yml` - Building blocks and materials
- `ores.yml` - Ores, ingots, and minerals
- `food.yml` - Food items
- `items.yml` - Miscellaneous items, drops, and farmable materials

## Permissions

| Permission | Default | Description |
|------------|---------|-------------|
| `endstone_makimarket.command.shop` | true | Allows using /shop command |
| `endstone_makimarket.command.buy` | true | Allows using /buy command |
| `endstone_makimarket.command.sell` | true | Allows using /sell command |
| `endstone_makimarket.command.reload` | op | Allows using /marketreload command |

## Building from Source
1. Clone the repository:
```bash
git clone https://github.com/your-repo/endstone-makimarket.git
cd endstone-makimarket
```

2. Install dependencies:
```bash
pip install -e .
```

3. Build the distribution:
```bash
python -m build
```

## File Structure

```
endstone-makimarket/
├── endstone_makimarket/
│   ├── __init__.py
│   ├── main.py
│   ├── config_loader.py
│   ├── utils.py
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── shop_command.py
│   │   ├── buy_command.py
│   │   ├── sell_command.py
│   │   └── reload_command.py
│   └── forms/
│       ├── shop_menu.py
│       └── sell_menu.py
├── pyproject.toml
└── README.md
```

## Dependencies

- **Endstone** >= 0.11
- **JWEconomy** - Economy provider
- **JWInventoryAPI** - GUI menu system

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.