import logging
import multiprocessing

logger = multiprocessing.log_to_stderr()

logger.setLevel(logging.WARNING)
