import os
import sys
import threading
import json
from typing import Union


# Function to get the correct path to resources
def resource_path(relative_path):
    """ Get the absolute path to a resource, works for both dev and PyInstaller environments """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_config_path(config_file: Union[str, os.PathLike]) -> str:
    """
    Constructs the path to the config file.

    :param config_file: The name of the config file.
    :type config_file: str or PathLike
    :return: The absolute path to the config file.
    :rtype: str
    """
    base_path = resource_path('')

    # Ensure base_path and config_file are strings
    base_path = str(base_path)
    config_file = str(config_file)

    # Combine the paths
    return os.path.join(base_path, 'configs', config_file)


if __name__ == '__main__':
    # Update the sys.path to include the correct module paths
    sys.path.append(resource_path('Code'))

    # Import after adjusting sys.path
    from tcp_ip.tcp_driver import TCPServer
    from utils import tms_logs
    from database.database import DatabaseServices

    # Create a TMSLogger instance for the server
    server_logger = tms_logs.TMSLogger("server")
    if not server_logger.setup():
        sys.exit(1)

    # Force APP_MODE to SERVER
    os.environ['APP_MODE'] = 'SERVER'
    app_mode = os.getenv('APP_MODE')

    # Pass the server logger to DatabaseServices
    db_service = DatabaseServices(db_file='taxpayers.db', tms_logger=server_logger)

    # Read the TCP configuration
    tcp_config_path = get_config_path('tcp_config.json')
    server_logger.log_debug(f"TCP config Path: {tcp_config_path}")

    if not os.path.exists(tcp_config_path):
        server_logger.log_critical(f"TCP Config file not found: {tcp_config_path}")
        sys.exit(1)

    try:
        with open(tcp_config_path, 'r') as tcp_config_file:
            tcp_configs = json.load(tcp_config_file)
    except OSError as e:
        server_logger.log_critical(f"Could not get TCP configs. Please check the file {tcp_config_path}. Error: {e}")
        sys.exit(1)
    else:
        server_logger.log_debug("TCP configs have been read successfully")

    try:
        host = tcp_configs["host"]
        port = tcp_configs["port"]
    except KeyError as exception:
        server_logger.log_error(f"Missing configuration key: {exception}")
        sys.exit(1)
    else:
        server_logger.log_debug(f"Starting server on {host}:{port}")

    # Initialize the server instance with the host and port from config
    server = TCPServer(host, port, new_user_window_instance=None)

    while True:
        client_socket, client_address = server.server_socket.accept()
        server_logger.log_debug(f"Connected client: {client_address}")
        multiple_client_connection_thread = threading.Thread(target=server.handle_request, args=(client_socket,))
        multiple_client_connection_thread.start()

    sys.exit(0)
