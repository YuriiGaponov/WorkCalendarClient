"""
Модуль app.core.logger — система логирования для WorkCalendarClient.

Определяет централизованный механизм логирования с:
- динамическим уровнем логирования в зависимости от окружения;
- ротацией файлов по размеру;
- форматированием записей с временной меткой;
- поддержкой разных именованных логгеров.

Ключевые возможности:
- автоматическая настройка уровня логирования (DEBUG для dev/test, ERROR для prod);
- запись логов в файлы с ротацией (RotatingFileHandler);
- гибкое именование файлов логов по имени логгера;
- использование настроек из app.core.settings для конфигурации.

Используемые компоненты:
- logging — стандартная библиотека Python для логирования;
- logging.handlers.RotatingFileHandler — обработчик с ротацией файлов;
- app.core.settings — модель настроек приложения (уровень логирования, пути и т. д.).


Экспортируемые объекты:
- Logger — класс для создания и настройки логгеров;
- main_logger — готовый экземпляр логгера с именем 'main' для общего использования.

Требования:
- установленный пакет pydantic-settings (для загрузки настроек);
- наличие директории, указанной в settings.LOG_DIR (должна быть доступна для записи);
- корректные значения настроек: LOG_MAX_BYTES, LOG_BACKUP_COUNT, ENCODING.


Пример использования:
    from app.core.logger import main_logger

    main_logger.debug("Отладочная информация")  # появится только в dev/test
    main_logger.error("Критическая ошибка")  # запишется всегда

    # Создание собственного логгера
    custom_logger = Logger('api').setup_logger()
    custom_logger.info("Запрос к API обработан")
"""

import logging
from logging.handlers import RotatingFileHandler

from app.core.settings import settings


class Logger:
    """
    Класс для создания и настройки именованных логгеров с ротацией файлов.

    Каждый экземпляр связан с уникальным именем логгера и соответствующим файлом логов.

    Attributes:
        name (str): имя логгера (используется в сообщениях и имени файла);
        log_file (str): имя файла логов (формируется как '{name}.log').

    Пример:
        logger = Logger('database')
        db_logger = logger.setup_logger()  # создаст логгер с файлом 'database.log'
    """

    def __init__(self, name: str) -> None:
        """
        Инициализирует экземпляр Logger.

        Args:
            name (str): уникальное имя логгера. Определяет имя файла логов и метку в записях.
        """
        self.name = name
        self.log_file = f'{name}.log'
    
    @classmethod
    def logging_level(cls) -> int:
        """
        Определяет уровень логирования в зависимости от окружения.

        Возвращает уровень DEBUG, если используется окружение .env.development
        или .env.testing, иначе возвращает уровень ERROR.

        Returns:
            int: Уровень логирования (DEBUG или ERROR)
        """
        if settings.ENVIRONMENT == 'development' or settings.ENVIRONMENT == 'testing':
            return logging.DEBUG
        return logging.ERROR

    def setup_logger(self) -> logging.Logger:
        """
        Настраивает и возвращает экземпляр логгера с обработчиком RotatingFileHandler.

        Выполняет:
        1. получение или создание логгера по имени (self.name);
        2. создание обработчика RotatingFileHandler с параметрами из настроек;
        3. настройку форматировщика для читаемого вывода;
        4. установку уровня логирования через logging_level();
        5. подключение обработчика к логгеру.

        Returns:
            logging.Logger: настроенный экземпляр логгера, готовый к использованию.

        Raises:
            OSError: если директория settings.LOG_DIR недоступна для записи или не существует.
            ValueError: если настройки (LOG_MAX_BYTES и др.) некорректны.
        """

        logger = logging.getLogger(self.name)

        handler = RotatingFileHandler(
            filename=f'{settings.LOG_DIR}/{self.log_file}',
            maxBytes=settings.LOG_MAX_BYTES,
            backupCount=settings.LOG_BACKUP_COUNT,
            encoding=settings.ENCODING
        )
        logger.addHandler(handler)

        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)8s: %(message)s")
        handler.setFormatter(formatter)

        logger.setLevel(self.logging_level())
        
        return logger

# Экземпляр основного логгера для общего использования
main_logger = Logger('main').setup_logger()
