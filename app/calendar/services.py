from .validators import validate_get_calendar_data

async def calendar_service(source: str, year: int):
    try:
        validate_get_calendar_data(source, year)
        print(f'Источник: {source}, год: {year}')
    except (TypeError, ValueError) as e:
        print(f"Ошибка валидации данных для скачивания календаря: {e}")
