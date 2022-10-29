import logging

__all__ = ["logger"]


class ColoredFormatter(logging.Formatter):
    blue = "\x1b[0;34m"
    cyan = "\x1b[0;36m"
    grey = "\x1b[38;20m"
    red = "\x1b[31;20m"
    yellow = "\x1b[33;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

handler.setFormatter(ColoredFormatter())

logger.addHandler(handler)
