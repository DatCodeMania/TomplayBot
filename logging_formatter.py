import logging

from colorama import Fore, Style


class CustomFormatter(logging.Formatter):
    base_format = "%(asctime)s - %(message)s"
    date_format = "%d/%m/%Y %H:%M:%S"

    FORMATS = {
        logging.DEBUG: Fore.CYAN + "[DEBUG] " + Style.RESET_ALL + base_format,
        logging.INFO: Fore.BLUE + "[INFO] " + Style.RESET_ALL + base_format,
        logging.WARNING: Fore.YELLOW + "[WARNING] " + Style.RESET_ALL + base_format,
        logging.ERROR: Fore.RED + "[ERROR] " + Style.RESET_ALL + base_format,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + "[CRITICAL] " + Style.RESET_ALL + base_format
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, self.date_format)
        return formatter.format(record)


def setup_logger(name, level):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    return logger
