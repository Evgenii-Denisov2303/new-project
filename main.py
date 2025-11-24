from config_data.config import bot
from utils.set_bot_commands import set_default_commands
from database.db_setup import init_db
from handlers import register_all_handlers


if __name__ == "__main__":
    # Инициализация базы данных
    init_db()

    # Установка команд бота
    set_default_commands(bot)

    # Регистрация всех обработчиков
    register_all_handlers(bot)

    # Запуск бота
    bot.infinity_polling(none_stop=True, interval=0)
