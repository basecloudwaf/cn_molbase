import logging


def get_log(chart):
    logger = logging.getLogger(chart)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("log_%s.log" % chart)
    handler.setLevel(logging.INFO)
    # handler.setLevel(logging.ERROR)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


