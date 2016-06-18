import logging


def get_logger(level, formatter, handler):
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def debug(msg, formatter=None, handler=None):
    return log(msg, logging.DEBUG, formatter, handler)


def warn(msg, formatter=None, handler=None):
    return log(msg, logging.WARN, formatter, handler)


def info(msg, formatter=None, handler=None):
    return log(msg, logging.INFO, formatter, handler)


def error(msg, formatter=None, handler=None):
    return log(msg, logging.ERROR, formatter, handler)


def log(msg, level=None, formatter=None, handler=None):
    if not handler:
        handler = logging.StreamHandler()
    if not formatter:
        formatter = logging.Formatter('[%(levelname)-8s] %(asctime)s %(name)-12s %(message)s')
    if not level:
        level = logging.DEBUG

    logger = get_logger(level, formatter, handler)
    logger.log(level, msg)
