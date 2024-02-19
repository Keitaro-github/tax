import sys
import ui.ui_signin_window
from PyQt6.QtWidgets import QApplication

tms_client_app = QApplication(sys.argv)
sign_in_window = ui.ui_signin_window.SignInWindow()
sign_in_window.show()
sys.exit(tms_client_app.exec())

