import logging
import sys

from src.asc_checksum.definitions import ROOT_DIR


class Logger:
    LOGS_PATH = ROOT_DIR / "out" / "logs.txt"
    CONSOLE_FORMAT = "%(levelname)s | %(message)s"
    FILE_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

    def __init__(self):
        self._console_logger = self._create_logger(
            "console_logger", logging.StreamHandler(sys.stderr), self.CONSOLE_FORMAT
        )
        self._file_logger = self._create_logger(
            "file_logger", logging.FileHandler(self.LOGS_PATH), self.FILE_FORMAT
        )

    def _create_logger(self, name, handler, format):
        handler.setFormatter(logging.Formatter(format))
        logger = logging.getLogger(name)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def log_to_console(self, text, level=logging.INFO):
        self._console_logger.log(level, text)

    def log_to_file(self, text, level=logging.INFO):
        self._file_logger.log(level, text)

    def log_to_file_and_console(self, text, level=logging.INFO):
        self.log_to_console(text, level)
        self.log_to_file(text, level)
