import sys
import Code
import threading
from Code.ui import ui_sign_in_window
from Code.ui import ui_tms_main_window
from PyQt6.QtWidgets import QApplication
from Code.utils.tms_logs import TMSLogger
import json


def thread_run_main_tms_window(*args):
    """
    This function implements the auxiliary thread intended to launch TMS main window.
    Args:
        *args: tuple of input parameters.

    Returns: None
    """

    try:
        client_logger = args[0]
        host = args[1]
        port = args[2]
        username = args[3]
        password = args[4]

        client_logger.log_debug("Main TMS window thread has been launched")

        app = QApplication(sys.argv)
        main_window = ui_tms_main_window.TMSMainWindow(client_logger, username, password, host, port)
        main_window.show()
        sys.exit(app.exec())

    except Exception as exception:
        client_logger.log_error(f"Error occurred while launching main TMS window: {exception}")


if __name__ == "__main__":

    client_logger = TMSLogger("client")
    if not client_logger.setup():
        sys.exit(1)

    client_logger.log_debug("Client logger has been set up successfully")

    try:
        with open(Code.TCP_CONFIGS, 'r') as tcp_config_file:
            tcp_configs = json.loads(tcp_config_file.read())
    except OSError:
        client_logger.log_critical(f"Could not get TCP configs. Please, check file {Code.TCP_CONFIGS}")
        sys.exit(1)
    else:
        client_logger.log_debug("TCP configs have been read successfully")

    try:
        host = tcp_configs["host"]
        port = tcp_configs["port"]
    except KeyError as exception:
        client_logger.log_error(exception)
        sys.exit(1)
    else:
        client_logger.log_debug("TCP configs have been parsed successfully")

    run_sign_in_thread = threading.Thread(name="THREAD_RUN_SIGN_IN_WINDOW",
                                          target=ui_sign_in_window.thread_run_sign_in_window,
                                          args=(client_logger, host, port))
    # Launch separate thread THREAD_RUN_SIGN_IN_WINDOW.
    run_sign_in_thread.start()
    # Suspend Main thread at this point until THREAD_RUN_SIGN_IN_WINDOW is terminated.
    run_sign_in_thread.join()

    if ui_sign_in_window.SignInWindow.request_status:
        ui_sign_in_window.run_main_tms_window(client_logger, host, port, None, None, )
