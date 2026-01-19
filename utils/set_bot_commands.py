from aiogram.types import BotCommand, MenuButtonCommands
from config_data.config import DEFAULT_COMMANDS


async def set_default_commands(bot):
    commands = [
        BotCommand(command=command, description=description)
        for command, description in DEFAULT_COMMANDS
    ]
    await bot.set_my_commands(commands)
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
