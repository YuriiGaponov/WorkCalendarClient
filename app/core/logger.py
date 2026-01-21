import logging
from logging.handlers import RotatingFileHandler

from app.core import settings


class Logger:

    def __init__(self, name: str) -> None:
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
        logger = logging.getLogger(self.name)

        handler = RotatingFileHandler(
            filename=f'{settings.LOG_DIR}/{self.name}',
            maxBytes=settings.LOG_MAX_BYTES,
            backupCount=settings.LOG_BACKUP_COUNT,
            encoding=settings.ENCODING
        )
        logger.addHandler(handler)

        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)8s: %(message)s")
        handler.setFormatter(formatter)

        logger.setLevel(self.logging_level())
        
        return logger

main_logger = Logger('main').setup_logger()
