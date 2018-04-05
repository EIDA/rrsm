import logging


class RrsmLoggerMixin():
    def __init__(self):
        self.class_name = self.__class__.__name__
        self.logger = logging.getLogger(self.class_name)

    def log_information(self, info='No description'):
        self.logger.info(
            '{0}: {1}'.format(self.class_name, info))

    def log_warning(self, info='No description'):
        self.logger.warning(
            '{0}: {1}'.format(self.class_name, info))

    def log_exception(self, info='No description'):
        self.logger.exception(
            '{0}: {1}'.format(self.class_name, info))
