from aiogram.types import BotCommand, MenuButtonCommands
from utils.i18n import SUPPORTED_LANGS


COMMANDS = {
    "ru": [
        ("start", "Запустить котика-ботика"),
        ("menu", "Открыть меню"),
        ("help", "Помощь по функциям"),
        ("survey", "Опрос"),
    ],
    "en": [
        ("start", "Start the cat bot"),
        ("menu", "Open menu"),
        ("help", "Help"),
        ("survey", "Survey"),
    ],
    "cs": [
        ("start", "Spustit kočičího bota"),
        ("menu", "Otevřít menu"),
        ("help", "Nápověda"),
        ("survey", "Průzkum"),
    ],
}


async def set_default_commands(bot):
    default_lang = "en"
    default_commands = [
        BotCommand(command=command, description=description)
        for command, description in COMMANDS[default_lang]
    ]
    await bot.set_my_commands(default_commands)
    for lang in SUPPORTED_LANGS:
        commands = [
            BotCommand(command=command, description=description)
            for command, description in COMMANDS[lang]
        ]
        await bot.set_my_commands(commands, language_code=lang)
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())
