import sys
import os

# Force APP_MODE to CLIENT
os.environ['APP_MODE'] = 'client'

import json
from PyQt6.QtWidgets import QApplication
from Code.ui.ui_login_window import LoginWindow
from Code.ui.ui_tms_main_window import TMSMainWindow
from Code.utils.tms_logs import TMSLogger


def get_base_path():
    """
    Returns the base path for the application.

    :return: The base path as a string.
    :rtype: str
    """
    if getattr(sys, 'frozen', False):
        # When running as a frozen application (e.g., PyInstaller)
        return getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        # When running in a standard Python environment (e.g., PyCharm)
        return os.path.dirname(os.path.abspath(__file__))


def get_config_path(config_file):
    """
    Constructs the path to the config file.

    :param config_file: The name of the config file.
    :type config_file: str
    :return: The absolute path to the config file.
    :rtype: str
    """
    base_path = get_base_path()

    # Adjust path based on whether running from PyInstaller or directly
    if getattr(sys, 'frozen', False):
        config_path = os.path.join(base_path, 'Code', 'configs', config_file)
    else:
        config_path = os.path.join(base_path, 'configs', config_file)

    return config_path


class TMSClient:
    def __init__(self):
        self.client_logger = TMSLogger("client")
        if not self.client_logger.setup():
            sys.exit(1)

        self.client_logger.log_debug("Client logger has been set up successfully")

        # Use the correct function to get the config path
        tcp_config_path = get_config_path('tcp_config.json')
        self.client_logger.log_debug(f"TCP config Path: {tcp_config_path}")

        if not os.path.exists(tcp_config_path):
            self.client_logger.log_critical(f"TCP Config file not found: {tcp_config_path}")
            sys.exit(1)

        try:
            with open(tcp_config_path, 'r') as tcp_config_file:
                tcp_configs = json.load(tcp_config_file)
        except OSError as e:
            self.client_logger.log_critical(
                f"Could not get TCP configs. Please check the file {tcp_config_path}. Error: {e}")
            sys.exit(1)
        else:
            self.client_logger.log_debug("TCP configs have been read successfully")

        try:
            self.host = tcp_configs["host"]
            self.port = tcp_configs["port"]
        except KeyError as exception:
            self.client_logger.log_error(f"Missing configuration key: {exception}")
            sys.exit(1)
        else:
            self.client_logger.log_debug("TCP configs have been parsed successfully")

        self.app = QApplication(sys.argv)
        self.login_window = LoginWindow(self.client_logger, self.host, self.port)
        self.login_window.login_successful.connect(self.on_login_success)
        self.login_window.show()

    def on_login_success(self, username, password, host, port):
        """
        Handles the successful login event by closing the login window and launching the main TMS window.

        Args:
            username (str): The username entered by the user.
            password (str): The password entered by the user.
            host (str): The host address for the TCP connection.
            port (int): The port number for the TCP connection.
        """
        self.client_logger.log_debug("Login was successful, launching main TMS window")
        self.login_window.close()

        self.main_window = TMSMainWindow(self.client_logger, username, password, host, port)
        self.main_window.show()

    def run(self):
        """
            Starts the Qt application event loop.
        """
        sys.exit(self.app.exec())


if __name__ == "__main__":
    tms_client = TMSClient()
    tms_client.run()
