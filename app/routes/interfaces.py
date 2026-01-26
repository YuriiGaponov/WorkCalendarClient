"""
Модуль app.routes.interfaces — определяет базовые маршруты API WorkCalendarClient.

Модуль содержит роутер FastAPI с базовыми эндпоинтами. Цель:
- обеспечить стартовую точку взаимодействия с приложением;
- заготовить основу для расширения функциональности;
- предоставить HTML‑интерфейсы для базовой проверки работы.

Используемые компоненты:
- fastapi.APIRouter — механизм группировки и управления маршрутами;
- fastapi.Request — объект HTTP‑запроса, передаваемый в обработчики;
- app.core.templates — движок шаблонов Jinja2 для рендеринга HTML;
- app.calendar.CalendarSettings — настройки календаря (диапазон лет, источники данных).

Экспортируемые объекты:
- router — экземпляр APIRouter с определёнными маршрутами.
  Может быть включён в основное приложение через app.include_router(router).

Определённые маршруты:
- GET / — главная страница сервиса. Рендерит index.html.
- GET /calendar — страница календаря. Рендерит calendar.html с параметрами.


Пример подключения:
    from app.routes.interfaces import router
    app.include_router(router)

Примечания:
- Все маршруты возвращают TemplateResponse (HTML), а не JSON/текст.
- Для работы требуется настроенное окружение шаблонов (templates) и валидные настройки CalendarSettings.
- Модуль спроектирован для постепенного расширения: новые маршруты добавляются в этот роутер.
- Рекомендуется вынести шаблоны (index.html, calendar.html) в отдельную директорию templates/.
"""

from fastapi import APIRouter, Request

from app.core import templates
from app.calendar import CalendarSettings


router = APIRouter()


@router.get('/')
def index_page(request: Request):
    """
    Эндпоинт главной страницы сервиса.

    Отображает HTML‑страницу `index.html` для проверки доступности сервиса.
    Предназначен для дальнейшей замены на полноценный интерфейс.

    Args:
        request (Request): Объект HTTP‑запроса от клиента.

    Returns:
        TemplateResponse: HTML‑ответ с шаблоном `index.html`.
    """
    return templates.TemplateResponse(request, 'index.html')

@router.get("/calendar", name="calendar")
def calendar_page(request: Request):
    """
    Эндпоинт страницы календаря.

    Отображает HTML‑страницу calendar.html с динамическими параметрами:
    - список источников данных (sources);
    - диапазон доступных лет (years).

    Args:
        request (Request): Объект HTTP‑запроса от клиента.

    Returns:
        TemplateDialog: HTML‑ответ с шаблоном calendar.html.
        В контекст передаются:
        - sources: список источников календаря (из CalendarSettings.SOURCES);
        - years: диапазон лет от MIN_YEAR до MAX_YEAR (включительно).
    """

    context = {
        "sources": CalendarSettings.SOURCES,
        "years": list(
            range(
                CalendarSettings.MIN_YEAR,
                CalendarSettings.MAX_YEAR + 1
            )
        )
    }

    return templates.TemplateResponse(request, "calendar.html", context)
