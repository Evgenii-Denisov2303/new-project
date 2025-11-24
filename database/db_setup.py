import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Определяем путь к базе данных
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "cat_bot.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Создаем движок базы данных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    """
    Инициализирует базу данных и создает таблицы.

    Создает необходимые таблицы в базе данных, используя метаданные из моделей.
    """

    from database.common.models import CatFact

    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    print(f"База данных успешно инициализирована")
