import schedule
import time
import threading
from database.common.models import CatFact
from services.cat_fact_api import get_cat_fact
from services.translate_api import translate_text


def create_translation():
    """
    Получает факт о котах, переводит его на русский язык и сохраняет в базу данных.

    Returns:
        str: Переведенный текст или сообщение об ошибке.
    """
    fact = get_cat_fact()
    if not fact:
        return "Не удалось получить факт о котиках."

    translation = translate_text(fact, target_language="ru")
    CatFact.create_with_fact(fact_text=fact, translation=translation)
    return translation


def cleanup_database():
    """
    Очищает старые записи из базы данных, оставляя только определенное количество последних фактов.

    Attributes:
        MAX_FACTS (int): Максимальное количество хранимых фактов.
    """
    MAX_FACTS = 100  # Максимальное количество хранимых фактов
    CatFact.cleanup_old_facts(max_facts=MAX_FACTS)


def setup_scheduler():
    """
    Настраивает планировщик для периодических задач.

    Задачи:
        - Получение нового факта о котах каждый день в 09:00.
        - Очистка базы данных каждую неделю в 03:00.
    """
    schedule.every().day.at("09:00").do(create_translation)
    schedule.every().monday.at("03:00").do(cleanup_database)

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()


def run_scheduler():
    """
    Запускает планировщик в бесконечном цикле.

    Выполняет запланированные задачи и ожидает новых событий.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)


class CRUDInterface:
    """
    Интерфейс для работы с CRUD операциями.

    Attributes:
        create_translation (method): Создает перевод факта о котах.
        cleanup (method): Очищает базу данных.
    """


    @staticmethod
    def create_translation():
        """
        Создает перевод нового факта о котах.

        Returns:
            str: Переведенный текст или сообщение об ошибке.
        """
        return create_translation()


    @staticmethod
    def cleanup():
        """
        Очищает старые записи из базы данных.

        Returns:
            None
        """
        return cleanup_database()
