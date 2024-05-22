import sys
import json
from PyQt6.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QCheckBox, QVBoxLayout, QHBoxLayout,
                             QMessageBox)
from PyQt6.QtCore import pyqtSignal, QObject
import Code
import Code.sign_in_services as sign_in_services
import Code.ui.ui_tms_main_window as ui_tms_main_window
from Code.utils import tms_logs
from PyQt6.QtCore import QTimer
import threading


class Communicate(QObject):
    signal = pyqtSignal()
    is_set = False
    initiate_main_window_signal = pyqtSignal(bool)


def thread_run_sign_in_window(*args):
    """
    This function implements the auxiliary thread intended to launch Sign In window.
    Args:
        *args: tuple of input parameters.
    Returns: None
    """

    try:
        tms_logger = args[0]
        host = args[1]
        port = args[2]

        tms_logger.log_debug("Sign in window thread has been launched")

        application = QApplication(sys.argv)
        sign_in_window = SignInWindow(tms_logger, host, port)
        sign_in_window.show()
        sys.exit(application.exec())

    except IndexError:
        pass


def thread_sign_in_request(*args):
    """
    This function implements the auxiliary thread intended to send TCP sign in request and wait TCP response.
    Args:
        *args: tuple of input parameters.
    Returns: None
    """

    try:
        tms_logger = args[0]
        host = args[1]
        port = args[2]
        username = args[3]
        password = args[4]
        signal = args[5]

        tms_logger.log_debug("Sign in thread has been launched")

        tcp_client = sign_in_services.TCPClient(host, port, username, password)
        result = tcp_client.send_request()

        tms_logger.log_debug(f"TMS server response is {result}")

        if result is True:
            SignInWindow.request_status = True
        else:
            SignInWindow.request_status = False

        tms_logger.log_debug(f"Emitting signal with result: {result}")
        signal.emit()
    except IndexError:
        pass


def run_main_tms_window(*args):
    """
    This function is intended to launch TMS main window.
    Args:
        *args: tuple of input parameters.
    Returns: None
    """

    try:
        tms_logger = args[0]
        host = args[1]
        port = args[2]
        username = args[3]
        password = args[4]

        tms_logger.log_debug("Main TMS window thread has been launched")

        app = QApplication(sys.argv)
        main_window = ui_tms_main_window.TMSMainWindow(tms_logger, username, password, host, port)
        main_window.show()
        sys.exit(app.exec())

    except IndexError:
        pass


class SignInWindow(QWidget):
    """
    Represents the sign in window of the Tax Management System (TMS) application, created using PyQt6 for user
    interaction with the GUI.

    Attributes:
        host (str): The hostname or IP address of the server to connect to.
        port (int): The port used by the server for the connection.
        __main_layout (QVBoxLayout): A layout widget for organizing GUI components.
    """

    request_complete = Communicate()
    request_status = False

    def __init__(self, tms_logger, host, port):
        super().__init__()  # Initialize default constructor of parent class
        self.__tms_logger = tms_logger
        self.host = host  # Define the host attribute
        self.port = port  # Define the port attribute

        # Call PyQt6 API to set current window's title.
        self.setWindowTitle("Sign In")
        # Call PyQt6 API to create a layout where all UI components are placed.
        self.__main_layout = QVBoxLayout()
        # Create all UI components on layout.
        self.__init_ui()
        # Call PyQt6 API to set prepared layout with all UI components.
        self.setLayout(self.__main_layout)
        # Sign in attempts limit and count.
        self.__ATTEMPTS_LIMIT = 3
        self.__attempt_count = 0

        # Initialize request_status to False
        self.request_status = False

    def __init_ui(self):
        """
        Initialize the user interface components.
        """

        # Create and set up the label.
        self.__label = QLabel()
        self.__label.setText("Welcome to Tax Management System")
        self.__label.setStyleSheet("font: bold 16px;")
        label_username = QLabel("Username")
        label_password = QLabel("Password")

        # Create and set up line edit widget for entering username.
        self.__username_edit = QLineEdit()
        self.__username_edit.setPlaceholderText("Please, enter username")

        # Create and set up line edit widget for entering password.
        self.__password_edit = QLineEdit()
        self.__password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.__password_edit.setPlaceholderText("Please, enter password")

        # Create checkbox to let the user hide the password
        self.__hide_checkbox = QCheckBox()
        self.__hide_checkbox.setText("Hide password")
        self.__hide_checkbox.toggled.connect(self.__click_hide_checkbox)
        self.__hide_checkbox.setChecked(True)
        self.__hide_checkbox.setToolTip("Uncheck to show password")

        # Create and set up button widget for sign in procedure.
        self.__sign_in_button = QPushButton()
        self.__sign_in_button.setText("Sign In")
        self.__sign_in_button.clicked.connect(self.__click_sign_in_button)
        self.__sign_in_button.setToolTip("Press to sign in to Tax Management System")

        # Create and set up button widget for cancel procedure.
        self.__cancel_button = QPushButton()
        self.__cancel_button.setText("Cancel")
        self.__cancel_button.clicked.connect(self.__click_cancel_button)
        self.__cancel_button.setToolTip("Press Cancel to close the window")

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.__sign_in_button)
        button_layout.addWidget(self.__cancel_button)

        # Create a horizontal layout for the labels and widgets
        layout_username = QHBoxLayout()
        layout_password = QHBoxLayout()

        # Add the layouts to the main layout
        self.__main_layout.addWidget(self.__label)
        self.__main_layout.addLayout(layout_username)
        self.__main_layout.addLayout(layout_password)

        # Add all the widgets to layout.
        layout_username.addWidget(label_username)
        layout_username.addWidget(self.__username_edit)

        layout_password.addWidget(label_password)
        layout_password.addWidget(self.__password_edit)

        self.__main_layout.addWidget(self.__hide_checkbox)
        self.__main_layout.addLayout(button_layout)

        self.__timer = QTimer()
        self.__timer.setInterval(180000)  # msecs 100 = 1/10th sec
        self.__timer.timeout.connect(self.__session_timeout)
        self.__timer.start()

        self.__button_clicked = False

        self.__tms_logger.log_debug("Sign In Window has been initialized successfully")

    def __session_timeout(self):
        """
        Handles session timeout.
        """

        self.__tms_logger.log_debug("Sign in session timeout occurred")
        self.__sign_in_time_out_message()
        self.__timer.stop()
        self.close()

    def __click_hide_checkbox(self):
        """
        Hides or displays the password based on the state of the checkbox.
        """

        if self.__hide_checkbox.isChecked() is True:
            self.__tms_logger.log_debug("Hide checkbox has been checked")
            self.__password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.__tms_logger.log_debug("Hide checkbox has been unchecked")
            self.__password_edit.setEchoMode(QLineEdit.EchoMode.Normal)

    def __click_sign_in_button(self):
        """
        Automatically called when the user clicks the "Sign in" button.
        - Starts a session timer.
        - Checks if the attempt limit has been reached.
        - Validates the entered username and password.
        - Displays success or failure messages accordingly.
        """

        self.__tms_logger.log_debug("Sign in button has been clicked")

        self.__timer.start(180000)

        # Attempts limit check
        if self.__attempt_count >= self.__ATTEMPTS_LIMIT:
            self.__sign_in_attempts_limit_message()
            self.close()
            return

        username = self.__username_edit.text()
        password = self.__password_edit.text()

        self.__button_clicked = True

        if self.__class__.request_complete.is_set is False:
            self.__class__.request_complete.signal.connect(lambda: self.__sign_in_done(username, password))
            self.__class__.request_complete.is_set = True

        # Create separate thread THREAD_SIGN_IN_REQUEST intended to send TCP sign in request.
        sign_in_request_thread = threading.Thread(target=thread_sign_in_request,
                                                 name="THREAD_SIGN_IN_REQUEST",
                                                 args=(self.__tms_logger,
                                                       self.host,
                                                       self.port,
                                                       username,
                                                       password,
                                                       self.__class__.request_complete.signal))
        # Launch separate thread THREAD_SIGN_IN_REQUEST.
        sign_in_request_thread.start()

    def __sign_in_done(self, username, password):
        """
        This method is intended to be called automatically when the signal has been emitted by SIGN_IN_THREAD.
        This method launches ui_tms_main_window module if sign in is successful.
        Args:
            username: username entered by the user
            password: password entered by the user

        Returns: None

        """
        self.__tms_logger.log_debug(f"Request status received with result: {self.__class__.request_status}")

        if self.__class__.request_status is True:
            self.__tms_logger.log_debug("Sign in procedure has been completed successfully")
            self.__sign_in_success_message()
            self.__timer.stop()
            self.close()
            return True

        elif self.__class__.request_status is False:
            self.__tms_logger.log_debug("Sign in procedure has been completed unsuccessfully")
            self.__attempt_count += 1
            self.__sign_in_failure_message()

            # Reset the username and password fields
            self.__username_edit.clear()
            self.__password_edit.clear()

        self.__class__.request_status = False

    def __click_cancel_button(self):
        """
        Automatically called when the user clicks the "Cancel" button.
        - Closes the sign-in window.
        """

        self.__tms_logger.log_debug("Cancel button has been clicked. Close application.")
        self.close()

    def __sign_in_success_message(self):
        """
        Displays a confirmation message when sign-in is successful.
        """

        self.__tms_logger.log_debug(f"Pop up: sign-in is successful")

        confirmation_dialog = QMessageBox(self)
        confirmation_dialog.setWindowTitle("Sign in successful")
        confirmation_dialog.setText("You have successfully signed in!")
        confirmation_dialog.exec()

    def __sign_in_failure_message(self):
        """
        Displays a warning message when sign-in fails due to incorrect credentials.
        """

        self.__tms_logger.log_info(f"Pop up: incorrect credentials")

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowTitle("Incorrect credentials")
        warning_dialog.setText("Entered username and/or password did not match!\nPlease re-enter your credentials.")
        warning_dialog.exec()

    def __sign_in_credentials_missing_message(self):
        """
        Displays a warning message when no credentials are entered.
        """

        self.__tms_logger.log_info(f"Pop up: no credentials are entered")

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowTitle("Missing credentials")
        warning_dialog.setText("No credentials were entered!\nPlease enter your credentials.")
        warning_dialog.exec()

    def __sign_in_attempts_limit_message(self):
        """
        Displays a warning message when the sign-in attempts limit is reached.
        - Disables sign-in and cancel buttons, password and username fields, and the hide checkbox.
        """

        self.__tms_logger.log_info(f"Pop up: attempts limit is reached")

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Critical)
        warning_dialog.setWindowTitle("Attempts limit reached!")
        warning_dialog.setText("Too many unsuccessful attempts to sign in!\nAccount is locked.")
        self.__sign_in_button.setDisabled(True)
        self.__cancel_button.setDisabled(True)
        self.__password_edit.setDisabled(True)
        self.__username_edit.setDisabled(True)
        self.__hide_checkbox.setDisabled(True)
        warning_dialog.exec()

    def __sign_in_time_out_message(self):
        """
        Displays a warning message when the sign-in session times out.
        - Disables sign-in and cancel buttons, password and username fields, and the hide checkbox.
        """

        self.__tms_logger.log_info(f"Pop up: sign-in session times out")

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Critical)
        warning_dialog.setWindowTitle("Sign in time out!")
        warning_dialog.setText("Sign in session expired!\nPlease restart application.")
        self.__sign_in_button.setDisabled(True)
        self.__cancel_button.setDisabled(True)
        self.__password_edit.setDisabled(True)
        self.__username_edit.setDisabled(True)
        self.__hide_checkbox.setDisabled(True)
        warning_dialog.exec()


if __name__ == "__main__":

    # Create and setup TMS logger.
    tms_logger = tms_logs.TMSLogger()
    status = tms_logger.setup()
    if status is False:
        sys.exit(1)
    # Get TCP configurations from external JSON file.
    try:
        with open(Code.TCP_CONFIGS, 'r') as tcp_config_file:
            tcp_configs = json.loads(tcp_config_file.read())
    except OSError:
        tms_logger.log_critical(f"Could not get TCP configs. Please, check file {Code.TCP_CONFIGS}")
        sys.exit(1)
    else:
        tms_logger.log_debug("TCP configs have been read successfully")
    # Parse TCP configurations represented in JSON format.
    try:
        host = tcp_configs["host"]
        port = tcp_configs["port"]
    except KeyError as exception:
        tms_logger.log_critical(exception)
        sys.exit(1)
    else:
        tms_logger.log_debug("TCP configs have been parsed successfully")

    # Create separate thread to run Sign In Window independently on Main thread.
    run_sign_in_thread = threading.Thread(name="THREAD_RUN_SIGN_IN_WINDOW",
                                          target=thread_run_sign_in_window,
                                          args=(tms_logger, host, port))
    # Launch separate thread THREAD_RUN_SIGN_IN_WINDOW.
    run_sign_in_thread.start()
    # Suspend Main thread at this point until THREAD_RUN_SIGN_IN_WINDOW is terminated.
    run_sign_in_thread.join()

    if SignInWindow.request_status:
        run_main_tms_window(tms_logger, host, port, None, None,)
