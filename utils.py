import logging
import sys


def create_logger():
    logger = logging.getLogger("azure")
    logger.setLevel(logging.DEBUG)
    # Set the logging level for the azure.storage.blob library
    logger = logging.getLogger("azure.storage.blob")
    logger.setLevel(logging.DEBUG)
    # Direct logging output to stdout. Without adding a handler,
    # no logging output is visible.
    handler = logging.StreamHandler(stream=sys.stdout)
    logger.addHandler(handler)
    return logger
