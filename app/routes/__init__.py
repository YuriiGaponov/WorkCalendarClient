"""
Модуль app.routes.__init__.py — сборка роутеров API для WorkCalendarClient.


Модуль объединяет роутеры из подмодулей в единый экземпляр APIRouter.
Это позволяет подключить все маршруты к основному приложению одной операцией.


Функциональность:
- Импорт роутеров из подмодулей (например, interfaces).
- Объединение маршрутов в единый роутер.
- Упрощение подключения всех API‑маршрутов к основному приложению.


Используемые компоненты:
- FastAPI.APIRouter — инструмент группировки маршрутов.


Экспортируемые объекты:
- router — экземпляр APIRouter со всеми включёнными маршрутами.
  Для подключения: app.include_router(router).


Пример импорта в main.py:
    from app.routes import router
    app.include_router(router)

Преимущества:
- Разделение маршрутов по логическим модулям в папке routes.
- Простота добавления новых роутеров (импорт + включение).
- Чистота кода в основном файле приложения (main.py).
"""

from fastapi import APIRouter


from .interfaces import router as interface_router

router = APIRouter()
router.include_router(interface_router)

__all__ = ['router']
