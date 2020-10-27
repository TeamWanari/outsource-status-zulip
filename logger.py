import logging
import os
import logstash

LOGLEVEL = os.getenv('LOGLEVEL', 'DEBUG')
LOG_HUMAN_READABLE = bool(os.getenv('LOG_HUMAN_READABLE', False))
LOG_FILE = bool(os.getenv('LOG_FILE', False))
LOG_FILE_NAME = str(os.getenv("LOG_FILE_NAME", "app.log"))

class AppLogger:
    def __init__(self, logger_name):
        global LOG_FILE_NAME
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(LOGLEVEL)
        logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if not LOG_HUMAN_READABLE:
            logger_formatter = logstash.LogstashFormatterVersion1()
            LOG_FILE_NAME = "app.json"

        console_logger = logging.StreamHandler()
        console_logger.setFormatter(logger_formatter)
        self.logger.addHandler(console_logger)

        if LOG_FILE:
            if not os.path.exists("../logs"):
                os.mkdir("../logs")
            file_logger = logging.FileHandler(f'../logs/{LOG_FILE_NAME}')
            file_logger.setFormatter(logger_formatter)
            self.logger.addHandler(file_logger)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def error(self, msg, ex=None):
        if ex is not None:
            self.logger.exception(msg, exc_info=ex)
        else:
            self.logger.error(msg)
