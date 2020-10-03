import os
import logging
from datetime import datetime
from rich.logging import RichHandler


def check(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def clear(file):
    if os.path.exists(file):
        os.remove(file)


# init log file
log_folder = "./logs"
check(log_folder)

log_file = os.path.join(log_folder, datetime.now().strftime("%Y%m%d_T%H%M%S.log"))
clear(log_file)

# init loggers
logger = logging.getLogger(__name__)
shell_handler = RichHandler()
file_handler = logging.FileHandler(log_file)

# set logging levels
logger.setLevel(logging.DEBUG)
shell_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

# set formats and formatters
fmt_shell = "%(message)s"
fmt_file = "%(levelname)s %(asctime)s [%(threadName)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"

shell_formatter = logging.Formatter(fmt_shell)
file_formatter = logging.Formatter(fmt_file)

shell_handler.setFormatter(shell_formatter)
file_handler.setFormatter(file_formatter)

# connect handlers to logger
logger.addHandler(shell_handler)
logger.addHandler(file_handler)
