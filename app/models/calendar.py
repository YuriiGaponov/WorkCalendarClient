"""
Модуль app.models.calendar — модель данных для хранения информации о днях календаря.

Определяет структуру таблицы `calendarday` в базе данных:
- дата;
- признак рабочего/нерабочего дня;
- название праздника (если есть).

Используемые компоненты:
- SQLAlchemy ORM — для описания модели и маппинга на таблицу БД;
- Base из app.core — базовая конфигурация моделей (автоимя таблицы, поле id).

Поля модели CalendarDay:
- date — дата (уникальная, индексированная, обязательная);
- is_working — флаг: True = рабочий день, False = выходной/праздник;
- holiday_name — опциональное название праздника (макс. 200 символов).

Преимущества:
- уникальность дат исключает дублирование записей;
- индекс по полю date ускоряет запросы по конкретной дате;
- поле holiday_name позволяет хранить контекст для нерабочих дней.

Пример использования:
    from app.models.calendar import CalendarDay
    day = CalendarDay(
        date=datetime.date(2025, 1, 1),
        is_working=False,
        holiday_name="Новый год"
    )

Требования:
- установленный SQLAlchemy;
- инициализированная БД с миграциями (например, через Alembic).
"""

from sqlalchemy import Column, Date, Boolean, String
from app.core import Base


class CalendarDay(Base):
    """
    Модель для хранения информации о статусе дня в календаре.

    Представляет запись о том, является ли конкретная дата рабочим днём,
    а также содержит название праздника для нерабочих дней.
    """

    date = Column(
        Date,
        unique=True,
        nullable=False,
        index=True
    )
    is_working = Column(Boolean, nullable=False)
    holiday_name = Column(String(200), nullable=True)
