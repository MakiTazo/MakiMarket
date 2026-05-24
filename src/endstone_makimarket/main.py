import inspect
import asyncio
from endstone.plugin import Plugin

from .config import config_loader
from .commands import preloaded_commands, preloaded_handlers, preloaded_perms

class Main(Plugin):

    api_version = "0.11"
    depend = ["jweconomy", "jwinventoryapi"]
    commands = preloaded_commands
    permissions = preloaded_perms

    def on_load(self) -> None:
        config_loader.load_defaults(str(self.data_folder))
        self.logger.info("MakiMarket its been loaded")

    def on_enable(self) -> None:
        eco_plugin = self.server.plugin_manager.get_plugin("jweconomy")
        if not eco_plugin or not eco_plugin.is_enabled:
            self.logger.error("JWEconomy not found or not enabled.")
            self.server.plugin_manager.disable_plugin(self)
            return
        self._economy_api = eco_plugin.get_api()
        self.logger.info("MakiMarket has been enabled successfully!")

    def on_disable(self) -> None:
        self.logger.info("Disabling MakiMarket")

    def on_command(self, sender, command, args) -> bool:
        handler = preloaded_handlers.get(command.name)
        if handler:
            if inspect.iscoroutinefunction(handler):
                asyncio.ensure_future(handler(self, sender, args))
                return True
            return handler(self, sender, args)
        return False