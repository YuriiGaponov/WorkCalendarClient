"""
Тесты миграций БД (`test_migrations.py`) для проекта WorkCalendarClient.

Цель: убедиться, что Alembic‑миграции корректно создают схему БД, особенно таблицу `calendarday`,
которая является ключевой для функционала календаря.

Контекст:
- Миграции применяются через `test_lifespan` при старте приложения (активируется HTTP‑запросом).
- Тестовая БД — SQLite в памяти (`sqlite:///:memory:`), изолирована для каждого запуска.
- Интроспекция схемы выполняется через SQLAlchemy `inspect()` для проверки наличия таблиц.

Используемые ресурсы:
- фикстура `test_client`: запускает приложение и `lifespan` (применяет миграции);
- фикстура `test_db_engine`: предоставляет доступ к тестовой БД для интроспекции.

Рекомендации:
- добавляйте тесты для других таблиц, если они появляются;
- проверяйте структуру столбцов через `inspector.get_columns('calendarday')`, если нужно.
"""

from sqlalchemy import inspect
from .conftest import test_client

class TestMigrations:
    """
    Тестовый класс для проверки миграций Alembic в WorkCalendarClient.

    Сценарий:
    1. Запускаем приложение через HTTP‑клиент → активируется `test_lifespan` → применяются миграции.
    2. Интроспектируем схему БД → проверяем наличие таблицы `calendarday`.

    Обеспечивает:
    - верификацию процесса миграции;
    - уверенность, что БД готова к работе до запуска бизнес‑логики.
    """

    def setup_class(self):
        """
        Подготавливает тестовый клиент для использования в тестах класса.

        Сохраняет глобальный `test_client` в атрибут экземпляра, чтобы тесты могли его использовать.
        """
        self.test_client = test_client

    def test_migrations_create_calendarday_table(self, test_client, test_db_engine):
        """
        Тест: миграции создают таблицу `calendarday` в тестовой БД.

        Пошагово:
        - отправляем GET‑запрос на `/` → запускаем приложение и `test_lifespan`;
        - через `inspect(test_db_engine)` получаем список таблиц;
        - проверяем, что `calendarday` есть среди них.

        Почему это важно:
        - таблица `calendarday` хранит данные календаря — без неё приложение неработоспособно;
        - тест гарантирует, что миграции не пропущены и схема актуальна.

        Args:
            test_client: фикстура HTTP‑клиента для активации приложения.
            test_db_engine: фикстура движка БД для интроспекции.

        Expected: таблица `calendarday` существует в БД после миграций.
        """
        response = test_client.get("/")
        assert response.status_code == 200, "Приложение не запустилось"

        inspector = inspect(test_db_engine)
        tables = inspector.get_table_names()
        assert "calendarday" in tables, "Таблица 'calendarday' не создана миграциями"
