import sys
import ui.ui_signin_window
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 65432

    tms_client_app = QApplication(sys.argv)
    sign_in_window = ui.ui_signin_window.SignInWindow(host, port)
    sign_in_window.show()
    sys.exit(tms_client_app.exec())
