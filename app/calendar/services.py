from app.parser import ConsultantPlusParser
from .validators import validate_get_calendar_data

def calendar_service(source: str, year: int):
    try:
        validate_get_calendar_data(source, year)
        print(f'Источник: {source}, год: {year}')
        parser = ConsultantPlusParser(year)
        parser.get_calendar_data()
    except (TypeError, ValueError) as e:
        print(f"Ошибка валидации данных для скачивания календаря: {e}")
