import logging
from pythonjsonlogger import jsonlogger
import sys

def get_logger(name=__name__):
    """
    Creates and returns a logger that outputs structured JSON.
    """
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s %(module)s %(funcName)s'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.propagate = False
    
    return logger