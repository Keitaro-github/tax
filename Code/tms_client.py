import sys
import Code
from Code.ui import ui_signin_window
from Code.utils import tms_logs
from PyQt6.QtWidgets import QApplication
import json
import threading


if __name__ == "__main__":

    tms_logger = tms_logs.TMSLogger()
    status = tms_logger.setup()
    if status is False:
        sys.exit(1)

    try:
        with open(Code.TCP_CONFIGS, 'r') as tcp_config_file:
            tcp_configs = json.loads(tcp_config_file.read())
    except OSError:
        tms_logger.log_critical(f"Could not get TCP configs. Please, check file {Code.TCP_CONFIGS}")
        sys.exit(1)
    else:
        tms_logger.log_debug("TCP configs have been read successfully")

    try:
        host = tcp_configs["host"]
        port = tcp_configs["port"]
    except KeyError as exception:
        tms_logger.log_critical(exception)
        sys.exit(1)
    else:
        tms_logger.log_debug("TCP configs have been parsed successfully")

    # tms_client_app = QApplication(sys.argv)
    # sign_in_window = ui_signin_window.SignInWindow(tms_logger, host, port)
    # sign_in_window.show()
    # sys.exit(tms_client_app.exec())

    # Create separate thread to run Sign In window independently on Main thread.
    run_sign_in_thread = threading.Thread(name="THREAD_RUN_SIGNIN_WINDOW",
                                          target=ui_signin_window.thread_run_signin_window,
                                          args=(tms_logger, host, port))
    # Launch separate thread THREAD_RUN_SIGNIN_WINDOW.
    run_sign_in_thread.start()
    # Suspend Main thread at this point until THREAD_RUN_SIGNIN_WINDOW is terminated.
    run_sign_in_thread.join()

    # TODO: Check when Main TMS window must be launched has to be added
    if True:
        ui_signin_window.thread_run_main_tms_window(tms_logger, host, port, None, None, )
