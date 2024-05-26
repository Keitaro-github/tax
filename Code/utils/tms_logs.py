import os.path
import sys
import json
import logging
from datetime import datetime


class TMSLogger:
    """
    This class implements the simple wrapper for standard logging module.
    """

    def __init__(self):
        self.__location = None
        self.__level = None
        self.__format = None
        self.__tms_logger = None

    def setup(self) -> bool:
        """
        This method is intended to set up TMS logger based on setting
        described on log_config.json file. All logs should be stored
        in autogenerated cache folder.
        Returns: True if set up has been completed successfully, False otherwise.
        """

        try:
            with open("Code/configs/log_config.json", 'r') as log_config_file:
                log_configs = json.loads(log_config_file.read())
        except OSError:
            logging.critical("Could not get LOG configs. Please, check Code/configs/log_config.json file")
            return False

        try:
            self.__location = log_configs["location"]
            self.__level = log_configs["level"]
            self.__format = log_configs["format"]
        except KeyError as exception:
            logging.critical(exception)
            return False

        if os.path.isdir(self.__location) is False:
            try:
                os.mkdir(self.__location)
            except OSError:
                logging.critical("Could not create cache folder")
                return False

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.__location, f"logs_{timestamp}.txt")

        # Get corresponding level number by level name
        self.__level = logging.getLevelName(self.__level)

        # Configure logger settings
        logging.basicConfig(handlers=[
                                logging.FileHandler(filename),
                                logging.StreamHandler()
                            ],
                            level=self.__level,
                            format=self.__format,)

        # Create logger for TMS based on preliminary settings.
        self.__tms_logger = logging.getLogger()

        return True

    def log_critical(self, message) -> None:
        """
        This method is intended to log message with critical logging level.
        Args:
            message: text user message.
        Returns: None
        """

        if self.__tms_logger is None:
            logging.critical("Could not log the message. Please setup TMS logger at first.")
        else:
            logging.critical(message)

    def log_error(self, message):
        """
        This method is intended to log message with critical logging level.
        Args:
            message: text user message.
        Returns: None
        """

        if self.__tms_logger is None:
            logging.critical("Could not log the message. Please setup TMS logger at first.")
            return
        else:
            logging.error(message)

    def log_info(self, message):
        """
        This method is intended to log message with info logging level.
        Args:
            message: text user message.
        Returns: None
        """

        if self.__tms_logger is None:
            logging.critical("Could not log the message. Please setup TMS logger at first.")
            return
        else:
            logging.info(message)

    def log_debug(self, message):
        """
        This method is intended to log message with debug logging level.
        Args:
            message: text user message.
        Returns: None
        """

        if self.__tms_logger is None:
            logging.critical("Could not log the message. Please setup TMS logger at first.")
            return
        else:
            logging.debug(message)


if __name__ == "__main__":

    tms_logger = TMSLogger()
    status = tms_logger.setup()
    if status is False:
        sys.exit(1)

    tms_logger.log_info("Test info message")
    tms_logger.log_critical("Test critical message")
    tms_logger.log_debug("Test debug message")
    tms_logger.log_error("Test error message")

    sys.exit(0)
