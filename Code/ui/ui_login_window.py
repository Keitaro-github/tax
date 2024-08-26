import json
from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QCheckBox, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt6.QtCore import pyqtSignal, QThread, QObject, QTimer
from Code.tcp_ip.tcp_driver import TCPClient


class LoginWorker(QObject):
    """
    LoginWorker handles the process of sending a sign-in request to the server
    and emitting a signal based on the server's response.

    Attributes:
        finished (pyqtSignal): Signal emitted when the sign-in process is complete.
        client_logger (TMSLogger): Logger instance for logging events.
        host (str): Host address for the TCP connection.
        port (int): Port number for the TCP connection.
        username (str): Username for the sign-in request.
        password (str): Password for the sign-in request.
    """
    finished = pyqtSignal(bool)

    def __init__(self, client_logger, host, port, username, password):
        """
        Initializes the LoginWorker with the necessary information to send a sign-in request.

        Args:
            client_logger (TMSLogger): Logger instance for logging events.
            host (str): Host address for the TCP connection.
            port (int): Port number for the TCP connection.
            username (str): Username for the sign-in request.
            password (str): Password for the sign-in request.
        """
        super().__init__()
        self.client_logger = client_logger
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def run(self):
        """
        Executes the sign-in process by sending a sign-in request to the server
        and emitting a signal based on the server's response.
        """
        self.client_logger.log_debug("Login worker thread has been launched")
        header_data = {
            "Content-Type": "application/json",
            "Encoding": "utf-8"
        }

        request_data = {
            "command": "login_request",
            "username": self.username,
            "password": self.password
        }

        message = {
            "header": header_data,
            "request": request_data
        }

        message_json = json.dumps(message)
        delimiter = b'\r\n'
        request = message_json.encode() + delimiter

        try:
            tcp_client = TCPClient(self.client_logger, self.host, self.port)
            response = tcp_client.send_request(request)

            self.client_logger.log_debug(f"TMS server response is {response}")

            if response["error"] != 0 or response["response"] not in [
                "User logged in successfully",
                "Username and password must be provided",
                "Invalid username or password"
            ]:
                self.client_logger.log_debug("Server response error")
                self.finished.emit(False)
            else:
                self.finished.emit(response["response"] == "User logged in successfully")

        except Exception as exception:
            self.client_logger.log_error(f"Unexpected exception: {exception}")
            self.finished.emit(False)


class LoginWindow(QWidget):
    """
    LoginWindow is the GUI window that allows the user to enter their username
    and password to login to the Tax Management System.

    Attributes:
        login_successful (pyqtSignal): Signal emitted when sign-in is successful.
        __client_logger (TMSLogger): Logger instance for logging events.
        host (str): Host address for the TCP connection.
        port (int): Port number for the TCP connection.
        username (str): Entered username by the user.
        password (str): Entered password by the user.
        __main_layout (QVBoxLayout): Main layout of the window.
        __ATTEMPTS_LIMIT (int): Maximum number of sign-in attempts allowed.
        __attempt_count (int): Counter for the number of sign-in attempts.
        __timer (QTimer): Timer for session timeout.
    """
    login_successful = pyqtSignal(str, str, str, int)

    def __init__(self, client_logger, host, port):
        """
        Initializes the LoginWindow with the necessary configurations and sets up the UI.

        Args:
            client_logger (TMSLogger): Logger instance for logging events.
            host (str): Host address for the TCP connection.
            port (int): Port number for the TCP connection.
        """
        super().__init__()
        self.__client_logger = client_logger
        self.host = host
        self.port = port
        self.username = None
        self.password = None

        self.setWindowTitle("Login")
        self.__main_layout = QVBoxLayout()
        self.__init_ui()
        self.setLayout(self.__main_layout)
        self.__ATTEMPTS_LIMIT = 3
        self.__attempt_count = 0
        self.__init_signals()

    def __init_signals(self):
        """
        Connects the sign-in button click signal to the appropriate handler.
        """
        self.__login_button.clicked.connect(self.__click_login_button)

    def __init_ui(self):
        """
        Initializes the user interface components and layout.
        """
        self.__label = QLabel("Welcome to Tax Management System")
        self.__label.setStyleSheet("font: bold 16px;")
        label_username = QLabel("Username")
        label_password = QLabel("Password")

        self.__username_edit = QLineEdit()
        self.__username_edit.setPlaceholderText("Please, enter username")

        self.__password_edit = QLineEdit()
        self.__password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.__password_edit.setPlaceholderText("Please, enter password")

        self.__hide_checkbox = QCheckBox("Hide password")
        self.__hide_checkbox.toggled.connect(self.__click_hide_checkbox)
        self.__hide_checkbox.setChecked(True)
        self.__hide_checkbox.setToolTip("Uncheck to show password")

        self.__login_button = QPushButton("Login")
        self.__login_button.setToolTip("Press to login to Tax Management System")

        self.__cancel_button = QPushButton("Cancel")
        self.__cancel_button.clicked.connect(self.__click_cancel_button)
        self.__cancel_button.setToolTip("Press Cancel to close the window")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.__login_button)
        button_layout.addWidget(self.__cancel_button)

        layout_username = QHBoxLayout()
        layout_password = QHBoxLayout()

        self.__main_layout.addWidget(self.__label)
        layout_username.addWidget(label_username)
        layout_username.addWidget(self.__username_edit)
        self.__main_layout.addLayout(layout_username)

        layout_password.addWidget(label_password)
        layout_password.addWidget(self.__password_edit)
        self.__main_layout.addLayout(layout_password)

        self.__main_layout.addWidget(self.__hide_checkbox)
        self.__main_layout.addLayout(button_layout)

        self.__timer = QTimer()
        self.__timer.setInterval(180000)
        self.__timer.timeout.connect(self.__session_timeout)
        self.__timer.start()

        self.__button_clicked = False
        self.__client_logger.log_debug("Login Window has been initialized successfully")

    def __session_timeout(self):
        """
        Handles the session timeout event by showing a message and closing the window.
        """
        self.__client_logger.log_debug("Login session timeout occurred")
        self.__login_time_out_message()
        self.__timer.stop()
        self.close()

    def __click_hide_checkbox(self):
        """
        Toggles the visibility of the password in the password input field.
        """
        self.__client_logger.log_debug("Hide checkbox has been toggled")
        self.__password_edit.setEchoMode(
            QLineEdit.EchoMode.Password if self.__hide_checkbox.isChecked() else QLineEdit.EchoMode.Normal)

    def __click_login_button(self):
        """
        Handles the sign-in button click event by sending a sign-in request to the server.
        """
        self.__client_logger.log_debug("Login button has been clicked")
        self.__timer.start(180000)

        if self.__attempt_count >= self.__ATTEMPTS_LIMIT:
            self.__login_attempts_limit_message()
            self.close()
            return

        self.username = self.__username_edit.text()
        self.password = self.__password_edit.text()

        self.__button_clicked = True

        self.worker = LoginWorker(self.__client_logger, self.host, self.port, self.username, self.password)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.finished.connect(self.__login_done)
        self.thread.start()

    def __login_done(self, status):
        """
        Handles the completion of the sign-in process by showing appropriate messages and proceeding based on the
        status.
        """
        self.__client_logger.log_debug(f"Request status received with result: {status}")
        if status:
            self.__client_logger.log_debug("Login procedure has been completed successfully")
            self.__login_success_message()
            self.__timer.stop()
            self.login_successful.emit(self.username, self.password, self.host, self.port)
            self.close()
        else:
            self.__client_logger.log_debug("Login procedure has been completed unsuccessfully")
            self.__attempt_count += 1
            self.__login_failure_message()
            self.__username_edit.clear()
            self.__password_edit.clear()

    def __click_cancel_button(self):
        """
        Handles the cancel button click event by closing the window.
        """
        self.__client_logger.log_debug("Cancel button has been clicked. Close application.")
        self.close()

    def __login_attempts_limit_message(self):
        """
        Shows a message indicating that the user has reached the maximum number of sign-in attempts.
        """
        QMessageBox.warning(self, "Login Failed", "You have reached the maximum number of attempts.")

    def __login_success_message(self):
        """
        Shows a message indicating that the sign-in was successful.
        """
        QMessageBox.information(self, "Login Successful", "You have signed in successfully!")

    def __login_failure_message(self):
        """
        Shows a message indicating that the sign-in failed.
        """
        QMessageBox.warning(self, "login Failed", "Invalid username or password. Please try again.")

    def __login_time_out_message(self):
        """
        Shows a message indicating that the sign-in session has timed out.
        """
        QMessageBox.warning(self, "Session Timed Out", "Your session has timed out. Please try to login again.")
