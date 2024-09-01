import sys
import json
from PyQt6.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout,
                             QDateEdit, QMessageBox, QComboBox)
from PyQt6.QtCore import QDate, pyqtSignal, QTimer, QThread, QObject
from Code.tcp_ip.tcp_driver import TCPClient
from Code.utils.tms_logs import TMSLogger


class UserRequestThread(QObject):
    """
    A thread class to handle search requests for user information.

    It sends a search request to the server based on provided user details and processes
    the server's response. Signals are emitted to indicate success or failure of the search.
    """
    search_successful_signal = pyqtSignal(list)
    search_unsuccessful_signal = pyqtSignal()
    stop_timer_signal = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, client_logger: TMSLogger, tcp_client, national_id: int, first_name: str, last_name: str,
                 date_of_birth: str):
        """
        Initializes the UserRequestThread with necessary details for the user search request.

        Args:
            client_logger (TMSLogger): Logger instance for logging debug information.
            tcp_client: The TCP client used to send requests.
            national_id (int): National ID of the user to search.
            first_name (str): First name of the user to search.
            last_name (str): Last name of the user to search.
            date_of_birth (str): Date of birth of the user to search (optional).
        """
        super().__init__()
        self.client_logger = client_logger
        self.tcp_client = tcp_client
        self.national_id = national_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth

    def run(self):
        """
        Sends a search request to the server and handles the server's response.

        Emits signals based on whether the search was successful or not.
        """
        self.client_logger.log_debug("Search request thread started execution")
        try:
            self.client_logger.log_debug("Search request timeout started")

            self.client_logger.log_debug("Started sending search request")
            header_data = {
                "Content-Type": "application/json",
                "Encoding": "utf-8"
            }

            request_data = {
                "command": "find_user",
                "national_id": self.national_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
            }

            if self.date_of_birth is not None:
                request_data["date_of_birth"] = self.date_of_birth

            message = {
                "header": header_data,
                "request": request_data
            }

            message_json = json.dumps(message)
            delimiter = b'\r\n'
            request = message_json.encode() + delimiter

            response = self.tcp_client.send_request(request)
            self.client_logger.log_debug(f"TMS server response is {response}")

            response_data = json.loads(response['response'])

            if response_data["command"] == "search_successful":
                results = response_data.get("user_info", [])
                self.search_successful_signal.emit(results)
                self.client_logger.log_debug(f"The search was successful with results: {results}")
            elif response_data["command"] == "search_unsuccessful":
                self.search_unsuccessful_signal.emit()
                self.client_logger.log_debug(f"The search was unsuccessful!")
            else:
                self.client_logger.log_debug(f"Server response error: {response_data}")
        except Exception as exception:
            self.client_logger.log_error(f"Unexpected exception: {exception}")
        finally:
            self.stop_timer_signal.emit()
            self.finished.emit()


class UserDetailsThread(QThread):
    """
    A thread class to handle requests for detailed user information based on national ID.

    It sends a request to retrieve detailed information about a specific user and emits
    a signal with the retrieved details upon completion.
    """
    request_complete = pyqtSignal(dict)

    def __init__(self, client_logger, tcp_client, national_id: int):
        """
        Initializes the UserDetailsThread with a logger, TCP client, and national ID.

        Args:
            client_logger (TMSLogger): Logger instance for logging debug information.
            tcp_client: The TCP client used to send requests.
            national_id (int): National ID of the user whose details are to be retrieved.
        """
        super().__init__()
        self.client_logger = client_logger
        self.tcp_client = tcp_client
        self.national_id = national_id

    def run(self):
        """
        Sends a request to retrieve detailed information for a specific user based on national ID.

        Emits a signal with the retrieved user details upon completion.
        """
        try:
            header_data = {
                "Content-Type": "application/json",
                "Encoding": "utf-8"
            }

            request_data = {
                "command": "retrieve_user_details",
                "national_id": self.national_id
            }

            message = {
                "header": header_data,
                "request": request_data
            }

            message_json = json.dumps(message)
            delimiter = b'\r\n'
            request = message_json.encode() + delimiter

            response = self.tcp_client.send_request(request)
            self.client_logger.log_debug(f"TMS server response is {response}")

            response_data = json.loads(response['response'])

            if response_data["command"] == "retrieving_successful":
                user_info = response_data["user_info"][0]
                user_details = {
                    "national_id": user_info.get("national_id"),
                    "first_name": user_info.get("first_name"),
                    "last_name": user_info.get("last_name"),
                    "date_of_birth": user_info.get("date_of_birth"),
                    "gender": user_info.get("gender"),
                    "address_country": user_info.get("address_country"),
                    "address_zip_code": user_info.get("address_zip_code"),
                    "address_city": user_info.get("address_city"),
                    "address_street": user_info.get("address_street"),
                    "address_house_number": user_info.get("address_house_number"),
                    "phone_country_code": user_info.get("phone_country_code"),
                    "phone_number": user_info.get("phone_number"),
                    "marital_status": user_info.get("marital_status"),
                    "tax_rate": user_info.get("tax_rate"),
                    "yearly_income": user_info.get("yearly_income"),
                    "advance_tax": user_info.get("advance_tax"),
                    "tax_paid_this_year": user_info.get("tax_paid_this_year"),
                    "property_value": user_info.get("property_value"),
                    "loans": user_info.get("loans"),
                    "property_tax": user_info.get("property_tax")
                }
                self.request_complete.emit(user_details)

            elif response_data["command"] == "retrieving_unsuccessful":
                self.request_complete.emit(None)

        except (json.JSONDecodeError, KeyError) as JSONDecodeError:
            self.client_logger.log_error(f"JSON decode or key error: {JSONDecodeError}")
        except Exception as Exception:
            self.client_logger.log_error(f"Unexpected exception: {Exception}")


class FindUserWindow(QWidget):
    """
    A window class that provides a user interface for searching users by their ID or name.

    It allows users to input search parameters, initiates search requests, and displays search results.
    It also handles user interactions such as selecting a search result and retrieving user details.
    """
    request_complete = pyqtSignal()
    search_successful_signal = pyqtSignal(list)
    search_unsuccessful_signal = pyqtSignal()
    server_timeout_signal = pyqtSignal()

    start_timer_signal = pyqtSignal(int)
    stop_timer_signal = pyqtSignal()

    def __init__(self, client_logger: TMSLogger, host, port, main_window=None):
        """
        Initializes the FindUserWindow with a logger, server host, port, and optional main window reference.

        Args:
            client_logger (TMSLogger): Logger instance for logging debug information.
            host (str): Host address of the server.
            port (int): Port number of the server.
            main_window (QWidget, optional): Reference to the main window, if applicable.
        """
        super().__init__()
        self.client_logger = client_logger
        self.host = host
        self.port = port
        self.tcp_client = TCPClient(client_logger, host, port)
        self.__main_window = main_window
        self.__date_of_birth_changed = False
        self.setMinimumWidth(500)
        self.__main_layout = QVBoxLayout()
        self.setLayout(self.__main_layout)

        self.__init_ui()

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__handle_timeout)
        self.start_timer_signal.connect(self.__start_timer)
        self.stop_timer_signal.connect(self.__stop_timer)

        self.thread = None
        self.user_request_thread = None

    def __init_ui(self):
        """
        Initializes the user interface components of the FindUserWindow.

        Sets up the labels, text fields, buttons, and layouts.
        """
        # Initialize UI components
        if self.__main_window is None:
            self.setWindowTitle("Find User Window - Standalone Mode")
            # Additional setup for standalone mode
        else:
            self.setWindowTitle("Find User Window")
        self.__label1 = QLabel("Search user by ID or name:")
        self.__label1.setStyleSheet("font: bold 12px;")

        label_national_id = QLabel("National ID")
        label_first_name = QLabel("First name")
        label_last_name = QLabel("Last name")
        label_date_of_birth = QLabel("Date of birth")

        self.__national_id_edit = QLineEdit()
        self.__national_id_edit.setPlaceholderText("Enter national ID")

        self.__first_name_edit = QLineEdit()
        self.__first_name_edit.setPlaceholderText("Enter first name")

        self.__last_name_edit = QLineEdit()
        self.__last_name_edit.setPlaceholderText("Enter last name")

        self.__date_of_birth_edit = QDateEdit(QDate.currentDate())
        self.__set_widget_color(self.__date_of_birth_edit, "white")
        self.__date_of_birth_edit.setCalendarPopup(True)
        self.__date_of_birth_edit.editingFinished.connect(self.__handle_widget_edit)

        self.__ok_button = QPushButton("OK")
        self.__ok_button.clicked.connect(self.__click_ok_button)

        self.__cancel_button = QPushButton("Cancel")
        self.__cancel_button.clicked.connect(self.__click_cancel_button)

        self.__search_results_edit = QComboBox()
        self.__search_results_edit.setPlaceholderText("Search results")
        self.__set_widget_color(self.__search_results_edit, "gray")
        self.__search_results_edit.currentIndexChanged.connect(self.__handle_search_result_selected)

        self.__main_layout.addWidget(self.__label1)

        layout_national_id = QHBoxLayout()
        layout_national_id.addWidget(label_national_id)
        layout_national_id.addWidget(self.__national_id_edit)

        layout_first_name = QHBoxLayout()
        layout_first_name.addWidget(label_first_name)
        layout_first_name.addWidget(self.__first_name_edit)

        layout_last_name = QHBoxLayout()
        layout_last_name.addWidget(label_last_name)
        layout_last_name.addWidget(self.__last_name_edit)

        layout_date_of_birth = QHBoxLayout()
        layout_date_of_birth.addWidget(label_date_of_birth)
        layout_date_of_birth.addWidget(self.__date_of_birth_edit)

        layout_search_results = QHBoxLayout()
        layout_search_results.addWidget(self.__search_results_edit)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.__ok_button)
        button_layout.addWidget(self.__cancel_button)

        self.__main_layout.addLayout(layout_national_id)
        self.__main_layout.addLayout(layout_first_name)
        self.__main_layout.addLayout(layout_last_name)
        self.__main_layout.addLayout(layout_date_of_birth)
        self.__main_layout.addLayout(layout_search_results)
        self.__main_layout.addLayout(button_layout)

        self.client_logger.log_debug("Find User Window has been initialized successfully")

    def __start_timer(self, timeout):
        """
        Starts a timer to handle request timeout.

        Args:
           timeout (int): Timeout duration in seconds.
        """
        self.client_logger.log_debug("Starting timer")
        self.__timer.start(timeout * 1000)  # Milliseconds

    def __stop_timer(self):
        """
        Stops the timeout timer.
        """
        self.client_logger.log_debug("Stopping timer")
        self.__timer.stop()

    def __handle_widget_edit(self):
        """
        Handles editing events for widgets, specifically date of birth and search results combo box.
        """
        sender = self.sender()
        if isinstance(sender, QDateEdit):
            self.__date_of_birth_changed = True
        if isinstance(sender, (QComboBox, QDateEdit)):
            self.__set_widget_color(sender, "black")

    @staticmethod
    def __set_widget_color(widget, color):
        """
        Sets the text color of the specified widget.

        Args:
            widget (QWidget): The widget whose color is to be set.
            color (str): The color to set.
        """
        widget.setStyleSheet(f"{widget.metaObject().className()} {{ color: {color}; }}")

    @staticmethod
    def __are_required_fields_filled(national_id, first_name, last_name, date_changed):
        """
        Checks if at least one required search parameter is filled.

        Args:
            national_id (int): National ID input.
            first_name (str): First name input.
            last_name (str): Last name input.
            date_changed (bool): Flag indicating if the date of birth has been changed.

        Returns:
            bool: True if at least one parameter is filled, otherwise False.
        """
        return any([national_id, first_name, last_name]) or date_changed

    def __click_cancel_button(self):
        """
        Handles the event when the Cancel button is clicked.
        Closes the FindUserWindow.
        """
        self.close()

    def __click_ok_button(self):
        """
        Handles the event when the OK button is clicked.
        Initiates the search request based on the provided parameters.
        """
        self.__search_results_edit.clear()
        self.__search_results_edit.setStyleSheet("color: gray;")
        national_id_text = self.__national_id_edit.text()
        try:
            national_id = int(national_id_text) if national_id_text else None
        except ValueError:
            QMessageBox.warning(self, "Invalid National ID", "National ID must be a number.")
            return
        first_name = self.__first_name_edit.text()
        last_name = self.__last_name_edit.text()
        date_of_birth = self.__date_of_birth_edit.date().toString("dd.MM.yyyy") if self.__date_of_birth_changed else \
            None

        if not self.__are_required_fields_filled(national_id, first_name, last_name, self.__date_of_birth_changed):
            # self.__missing_data_message()
            QMessageBox.warning(self, "Missing data", "Please enter at least one search parameter.")
            return

        self.client_logger.log_debug("Starting search request thread")
        self.start_timer_signal.emit(5)

        self.thread = QThread()
        self.user_request_thread = UserRequestThread(self.client_logger, self.tcp_client, national_id, first_name,
                                                     last_name, date_of_birth)
        self.user_request_thread.moveToThread(self.thread)

        self.user_request_thread.search_successful_signal.connect(self.__populate_search_results)
        self.user_request_thread.search_unsuccessful_signal.connect(self.__search_unsuccessful_message)
        self.user_request_thread.stop_timer_signal.connect(self.__stop_timer)
        self.thread.started.connect(self.user_request_thread.run)
        self.user_request_thread.finished.connect(self.thread.quit)
        self.user_request_thread.finished.connect(self.user_request_thread.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def __populate_search_results(self, results):
        """
        Populates the search results combo box with the results of the search request.

        Args:
            results (list): List of search results to be displayed.
        """
        self.__search_results_edit.clear()
        self.__search_results_edit.setStyleSheet("color: black;")
        self.client_logger.log_debug(f"Populating search results: {results}")
        if not results:
            self.__search_results_edit.setPlaceholderText("No matching results")
            self.client_logger.log_debug("No matching results")
        else:
            for result in results:
                display_text = (f"{result['national_id']} {result['first_name']} {result['last_name']} "
                                f"{result['date_of_birth']}")
                self.__search_results_edit.addItem(display_text)
                self.client_logger.log_debug(f"Adding result to combo box: {display_text}")
            self.__search_results_edit.setCurrentIndex(-1)
            QMessageBox.information(self, "Search Status", "The user was found successfully!")

    def __handle_search_result_selected(self, index):
        """
        Handles the selection of a user from the search results combo box.

        Args:
            index (int): Index of the selected search result.
        """
        if index >= 0:
            # Get the selected item text
            selected_text = self.__search_results_edit.itemText(index)

            # Parse the selected text to extract the necessary information
            selected_info = selected_text.split()

            # Extract the national ID from the selected information
            national_id = int(selected_info[0])

            # Send a request to the server to retrieve detailed information about the selected user
            self.__request_user_details(national_id)
            self.client_logger.log_debug(
                f"Request to the server to retrieve detailed information about a selected user is sent")

    def __request_user_details(self, national_id):
        """
        Requests detailed information about a specific user from the server.

        Args:
            national_id (int): National ID of the user to retrieve details for.
        """
        self.client_logger.log_debug(f"Requesting user details for National ID: {national_id}")
        self.user_details_thread = UserDetailsThread(self.client_logger, self.tcp_client, national_id)
        self.user_details_thread.request_complete.connect(self.__handle_user_details_response)
        self.user_details_thread.start()

    def __handle_user_details_response(self, user_details):
        """
        Handles the response containing user details.

        Args:
            user_details (dict or None): User details if successful, otherwise None.
        """
        if user_details:
            self.client_logger.log_debug("User details retrieved successfully")
            if self.__main_window is not None:
                self.__main_window.user_details_retrieved_signal.emit(user_details)
                self.close()
        else:
            QMessageBox.warning(self, "Retrieving Unsuccessful", "Could not retrieve information.")
            self.client_logger.log_debug("Retrieving of user details was unsuccessful!")

    def __search_unsuccessful_message(self):
        QMessageBox.information(self, "Search Status", "No matching results")

    def __handle_timeout(self):
        """
        Handles the timeout event for search requests.
        """
        self.client_logger.log_debug("Timeout occurred. Aborting search request thread.")
        self.thread.quit()
        QMessageBox.warning(self, "Timeout", "The search request timed out.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_logger = TMSLogger("client")

    # Ensure the logger is properly set up
    if not client_logger.setup():
        sys.exit(1)

    host = 'localhost'
    port = 65432
    main_window = None
    window = FindUserWindow(client_logger, host, port, main_window)
    window.show()
    sys.exit(app.exec())
