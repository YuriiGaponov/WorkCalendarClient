"""
Модуль валидации входных данных для работы с календарём.
Содержит функции проверки корректности параметров запросов к календарным данным.
"""


from .settings import CalendarSettings


def validate_get_calendar_data(source, year) -> None:
    """
    Проверяет корректность параметров для получения календарных данных.

    Args:
        source: Название источника календаря (должно быть в CalendarSettings.SOURCES).
        year: Год календаря (должен быть в диапазоне MIN_YEAR–MAX_YEAR).

    Raises:
        TypeError: Если source не str или year не int.
        ValueError: Если source неизвестен или year вне допустимого диапазона.

    Example:
        >>> validate_get_calendar_data('official_gov', 2025)
        # Проходит без ошибок

        >>> validate_get_calendar_data(123, 2025)
        # Вызывает TypeError
    """

    if not isinstance(source, str):
        raise TypeError(
            f"Название источника календаря должен быть строкой (str), "
            f"получено: {type(source).__name__}"
        )
    
    if source not in CalendarSettings.SOURCES:
        raise ValueError(
            f"Неизвестный источник данных: '{source}'. "
        )
    
    if not isinstance(year, int):
        raise TypeError(
            f"Год календаря должен быть целым числом (int), "
            f"получено: {type(year).__name__}"
        )
    
    if year < CalendarSettings.MIN_YEAR:
        raise ValueError(
            f"Год {year} меньше минимально допустимого "
            f"({CalendarSettings.MIN_YEAR})."
        )
    
    if year > CalendarSettings.MAX_YEAR:
        raise ValueError(
            f"Год {year} ,больше максимально допустимого "
            f"({CalendarSettings.MAX_YEAR})."
        )