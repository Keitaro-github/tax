import sys
import os
# import ui.ui_signin_window
from Code.ui import ui_signin_window
from PyQt6.QtWidgets import QApplication
import json

if __name__ == "__main__":

    filename = os.getcwd()
    print(filename)

    try:
        with open("Code/configs/tcp_config.json", 'r') as tcp_config_file:
            tcp_configs = json.loads(tcp_config_file.read())
    except OSError:
        print("Could not get TCP configs. Please, check Code/configs/tcp_config.json file")
        sys.exit(1)

    try:
        host = tcp_configs["host"]
        port = tcp_configs["port"]
    except KeyError as exception:
        print(exception)
        sys.exit(1)

    tms_client_app = QApplication(sys.argv)
    sign_in_window = ui_signin_window.SignInWindow(host, port)
    sign_in_window.show()
    sys.exit(tms_client_app.exec())
