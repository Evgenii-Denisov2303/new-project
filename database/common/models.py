import datetime
import json
from sqlalchemy import Column, Integer, DateTime, Text
from sqlalchemy.orm import scoped_session
from database.db_setup import Base, SessionLocal


db_session = scoped_session(SessionLocal)


class CatFact(Base):
    """
    Модель для хранения фактов о котах.

    Attributes:
        id (int): Уникальный идентификатор записи.
        user_id (int): ID пользователя, которому принадлежит факт.
        facts (str): JSON-строка с фактами о котах.
        current_index (int): Текущий индекс факта.
        created_at (datetime): Дата создания записи.
    """

    __tablename__ = "cat_facts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    facts = Column(Text, default="[]")
    current_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


    @classmethod
    def get_or_create(cls, user_id: int):
        """
        Получает или создает запись для пользователя.

        Args:
            user_id (int): ID пользователя.

        Returns:
            CatFact: Экземпляр CatFact для указанного пользователя.
        """
        instance = db_session.query(cls).filter_by(user_id=user_id).first()
        if not instance:
            instance = cls(user_id=user_id)
            db_session.add(instance)
            db_session.commit()
        return instance


    def add_fact(self, fact_text: str):
        """
        Добавляет новый факт в коллекцию.

        Args:
            fact_text (str): Текст нового факта.

        Returns:
            bool: True, если факт добавлен успешно.
        """
        facts = json.loads(self.facts)
        facts.append({"text": fact_text})
        self.facts = json.dumps(facts)
        self.current_index = len(facts) - 1
        db_session.add(self)
        db_session.commit()
        return True


    @property
    def current_fact(self):
        """
        Возвращает текущий факт.

        Returns:
            str: Текст текущего факта или None, если фактов нет.
        """
        try:
            facts = json.loads(self.facts)
            return facts[self.current_index]["text"] if facts else None
        except (json.JSONDecodeError, IndexError):
            return None

    def save(self):
        """
        Сохраняет изменения в базе данных.

        Returns:
            bool: True, если сохранение прошло успешно.
        """
        db = SessionLocal()
        db.merge(self)  # Обновляем объект в текущей сессии
        db.commit()
        db.close()
        return True


    @classmethod
    def cleanup_old_facts(cls, max_facts=100):
        """
        Очищает старые записи из базы данных.

        Args:
            max_facts (int): Максимальное количество сохраняемых записей.

        Returns:
            int: Количество удаленных записей.
        """
        db = SessionLocal()
        subquery = db.query(cls.id).order_by(cls.created_at.desc()).limit(max_facts)
        result = db.query(cls).filter(cls.id.not_in(subquery)).delete()
        db.commit()
        db.close()
        return result
