# ./app/logging_config.py

import logging
import sys

def setup_logging():
    logger = logging.getLogger("serendipity")
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler("serendipity.log")

    handler_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(handler_format)
    file_handler.setFormatter(handler_format)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger