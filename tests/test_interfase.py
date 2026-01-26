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
    Набор тестов для проверки базовых маршрутов API.
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
