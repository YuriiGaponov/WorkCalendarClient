"""
Модуль tests.test_interface.py — тесты для базового интерфейса API
WorkCalendarClient.


Содержит тестовые сценарии для проверки основных эндпоинтов приложения:
- доступность корневого маршрута;
- обработку несуществующих маршрутов (404);
- доступность маршрута /calendar.

Используемые компоненты:
- pytest — фреймворк для запуска тестов;
- TestClient из fastapi.testclient — имитация HTTP‑запросов к API.


Требования:
- запущенный экземпляр приложения (через conftest.py);
- установленный pytest и зависимости проекта.
"""

from .conftest import client


class TestInterface:
    """
    Набор тестов для проверки базовых маршрутов интерфейса.
    """

    def setup_class(self):
        """
        Инициализация тестового клиента перед запуском тестов класса.
        """
        self.client = client

    def test_root_endpoint_returns_200(self):
        """
        Проверяет, что корневой эндпоинт возвращает статус 200.
        """
        response = self.client.get("/")
        assert response.status_code == 200

    def test_404_on_unknown_endpoint(self):
        """
        Проверяет, что несуществующий маршрут возвращает статус 404.
        """
        response = self.client.get("/unknown")
        assert response.status_code == 404
    
    def test_root_endpoint_returns_200(self):
        """
        Проверяет, что эндпоинт получения календаря возвращает статус 200.
        """
        response = self.client.get("/calendar")
        assert response.status_code == 200
    
    def test_get_calendar_endpoint_available(self):
        """
        Тест проверки доступности эндпоинта /get-calendar (POST).
        Отправляет валидный запрос и проверяет:
        - статус-код 200;
        - наличие ожидаемых данных в ответе (пример).
        """
        form_data = {
            "source": "test_source",
            "year": 2025
        }
        response = client.post("/get-calendar", data=form_data)

        assert response.status_code == 200, (
            f"Ожидался статус 200, но получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

    def test_get_calendar_missing_field(self):
        """
        Тест на отсутствие обязательного поля (например, 'year')
        при обработке эндпоинта /get-calendar (POST).
        Проверяет, что сервис возвращает ошибку.
        """

        form_data_set = (
            dict(),  #  все поля пустые
            {"source": "test_source"},  # 'year' пропущен
            {"year": 2025}  # 'source' пропущен
        )
        for form_data in form_data_set:

            response = client.post("/get-calendar", data=form_data)

            assert response.status_code == 422, (
                f"Ожидался статус 422 (Unprocessable Entity), но получен {response.status_code}"
            )
