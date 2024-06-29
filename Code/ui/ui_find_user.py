import sys
import socket
import json
import threading
import Code.tcp_ip.tcp_driver as tcp_driver
from PyQt6.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout,
                             QDateEdit, QMessageBox, QComboBox, QSpinBox)
from PyQt6.QtCore import QDate, pyqtSignal, QTimer
from Code.utils.tms_logs import TMSLogger


class FindUserWindow(QWidget):
    """
    Represents a Window created with PyQt6 for interaction of system user with GUI.

    Attributes:
        host (str): The hostname or IP address of the server to connect to.
        port (int): The port used by the server for the connection.
        main_window (FindUserWindow): An instance of the FindUserWindow class.
        __main_layout (QVBoxLayout): A layout widget for organizing GUI components.
    """

    # User saved signal
    request_complete = pyqtSignal()
    # Search successful signal
    search_successful_signal = pyqtSignal()
    # Search unsuccessful signal
    search_unsuccessful_signal = pyqtSignal()
    # Retrieving successful signal
    retrieving_successful_signal = pyqtSignal()
    # Retrieving unsuccessful signal
    retrieving_unsuccessful_signal = pyqtSignal()
    # Define a signal for handling server timeout
    server_timeout_signal = pyqtSignal()

    start_timer_signal = pyqtSignal(int)
    stop_timer_signal = pyqtSignal()

    def __init__(self, client_logger: TMSLogger, host, port, main_window):
        """
        Initializes a new instance of the FindUserWindow class.

        Args:
            client_logger (logging.Logger): An instance of the logger.
            host (str): The server's hostname or IP address to connect to.
            port (int): The port used by the server to connect to.
            main_window (TMSMainWindow): An instance of the TMSMainWindow class.
        """
        super().__init__()
        self.__client_logger = client_logger
        self.host = host
        self.port = port
        self.tcp_client = tcp_driver.TCPClient(client_logger, host, port)
        self.__main_window = main_window
        # Flag to track date changes
        self.__date_of_birth_changed = False
        # Call PyQt6 API to set current window's title.
        self.setWindowTitle("Find user")
        # Call PyQt6 API to create a layout where all UI components are placed.
        self.setMinimumWidth(500)
        self.__main_layout = QVBoxLayout()
        # Call PyQt6 API to set prepared layout with all UI components.
        self.setLayout(self.__main_layout)
        self.__thread_event = threading.Event()

        self.running = False
        self.__init_ui()

        # Connect the signals to the messages
        self.search_successful_signal.connect(self.__search_successful_message)
        self.search_unsuccessful_signal.connect(self.__search_unsuccessful_message)
        self.retrieving_successful_signal.connect(self.handle_retrieving_successful)
        self.retrieving_unsuccessful_signal.connect(self.handle_retrieving_unsuccessful)

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__handle_timeout)
        self.start_timer_signal.connect(self.__start_timer)
        self.stop_timer_signal.connect(self.__stop_timer)
        # Connect the search results combo box signal to the handler
        self.__search_results_edit.currentIndexChanged.connect(self.__handle_search_result_selected)


    def __init_ui(self):
        """
         Creates and sets up all UI components necessary for user input.

            This method initializes various input fields and buttons required for entering and saving user information.
        Each UI component is created and configured with appropriate settings such as placeholders, validators, and
        event handlers. Layouts are created to organize these components in a visually appealing manner. Finally, the
        components are added to the main layout of the window for display.
        """

        # Create and set up the label.
        self.__label1 = QLabel()
        self.__label1.setText("Search user by ID or name:")
        self.__label1.setStyleSheet("font: bold 12px;")

        self.__label = QLabel()
        self.__label.setStyleSheet("font: bold 16px;")
        label_national_id = QLabel("National ID")

        label_first_name = QLabel("First name")
        label_last_name = QLabel("Last name")
        label_date_of_birth = QLabel("Date of birth")

        # Create and set up line edit widget for entering user ID.
        self.__national_id_edit = QLineEdit()
        self.__national_id_edit.setPlaceholderText("Enter national ID")

        # Create and set up line edit widget for entering first name.
        self.__first_name_edit = QLineEdit()
        self.__first_name_edit.setPlaceholderText("Enter first name")

        # Create and set up line edit widget for entering last name.
        self.__last_name_edit = QLineEdit()
        self.__last_name_edit.setPlaceholderText("Enter last name")

        # Create and set up date edit widget for entering date.
        self.__date_of_birth_edit = QDateEdit(QDate.currentDate())
        self.__set_widget_color(self.__date_of_birth_edit, "white")
        self.__date_of_birth_edit.setCalendarPopup(True)
        self.__date_of_birth_edit.editingFinished.connect(self.__handle_widget_edit)

        # Create and set up button widget for saving data.
        self.__ok_button = QPushButton()
        self.__ok_button.setText("OK")
        self.__ok_button.clicked.connect(self.__click_ok_button)
        self.__ok_button.setToolTip("Press OK perform search")

        # Create and set up button widget for cancel procedure.
        self.__cancel_button = QPushButton()
        self.__cancel_button.setText("Cancel")
        self.__cancel_button.clicked.connect(self.__click_cancel_button)
        self.__cancel_button.setToolTip("Press Cancel to abort operation")

        self.__search_results_edit = QComboBox()
        self.__search_results_edit.setPlaceholderText("Search results")
        self.__set_widget_color(self.__search_results_edit, "gray")
        self.__search_results_edit.currentIndexChanged.connect(self.__handle_widget_edit)

        # Create a horizontal layout for the labels and widgets
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

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.__ok_button)
        button_layout.addWidget(self.__cancel_button)

        # Add the widgets to the main layout
        self.__main_layout.addLayout(layout_national_id)
        self.__main_layout.addLayout(layout_first_name)
        self.__main_layout.addLayout(layout_last_name)
        self.__main_layout.addLayout(layout_date_of_birth)
        self.__main_layout.addLayout(layout_search_results)
        self.__main_layout.addLayout(button_layout)

        self.__client_logger.log_debug("Find User Window has been initialized successfully")

    def __start_timer(self, timeout):
        """
        Starts a timer for the specified timeout duration.
        Args:
            timeout (int): The timeout duration in seconds.
        """
        self.__client_logger.log_debug("Starting timer")
        self.__timer.start(timeout * 1000)  # Milliseconds

    def __stop_timer(self):
        """
        Stops the currently running timer.
        """
        self.__client_logger.log_debug("Stopping timer")
        self.__timer.stop()

    def __handle_widget_edit(self):
        """
        A slot method that handles the Editing finished signal for various widgets.
        """

        sender = self.sender()
        if isinstance(sender, QDateEdit):
            # Mark date as changed
            self.__date_of_birth_changed = True
        if isinstance(sender, (QComboBox, QDateEdit, QSpinBox)):
            # Change the text color to black once the widget is edited
            self.__set_widget_color(sender, "black")

    @staticmethod
    def __set_widget_color(widget, color):
        """
        Changes text color to black once editing is finished.
        """

        widget.setStyleSheet(f"{widget.metaObject().className()} {{ color: {color}; }}")

    @staticmethod
    def __are_required_fields_filled(national_id, first_name, last_name, date_changed):
        """
        Checks if any of the 4 fields are filled: national_id, first_name, last_name or date_of_birth.

        :param national_id: The national ID of user.
        :type national_id: int
        :param first_name: The first name of user.
        :type first_name: str
        :param last_name: The last name  of user.
        :type last_name: str
        :param date_changed: The changed date of birth of the user in the format 'dd.MM.yyyy'.
        :type date_changed: str
        :return: True if any of the required fields are filled or the date_of_birth is not the current date, False
        otherwise.
        :rtype: bool
        """

        return any([national_id, first_name, last_name]) or date_changed

    def __click_cancel_button(self):
        """
        Calls automatically when the user clicks on Cancel button.
        """

        self.close()

    def __click_ok_button(self):
        """
        Calls automatically when the user clicks on OK button.
        """
        # Delete previous search result if available
        self.__search_results_edit.clear()
        self.__search_results_edit.setStyleSheet("color: gray;")
        # Collect data from all widgets
        national_id = self.__national_id_edit.text()
        if national_id:
            national_id = int(national_id)  # Convert to int if not empty
        first_name = self.__first_name_edit.text()
        last_name = self.__last_name_edit.text()
        date_of_birth = self.__date_of_birth_edit.date().toString("dd.MM.yyyy") if self.__date_of_birth_changed else \
            None

        if not self.__are_required_fields_filled(national_id, first_name, last_name, self.__date_of_birth_changed):
            self.__missing_data_message()
            return

        self.running = True  # Reset the running flag
        self.__thread_event.clear()  # Clear the event

        # Perform the actual search request in a separate thread
        threading.Thread(target=self.__send_search_request,
                         args=(national_id, first_name, last_name, date_of_birth)).start()
        self.__client_logger.log_debug("Search request thread started")

    def __handle_timeout(self):
        """
        Handles the timeout event when a search request exceeds the specified duration.
        """
        self.__client_logger.log_debug("Search request timed out")
        self.__stop_timer()
        self.running = False  # Reset the running flag
        self.__thread_event.set()  # Ensure the thread is signaled to stop
        self.__stop_timer()
        # Emit server timeout signal
        self.server_timeout_signal.emit()
        self.__client_logger.log_debug("Timeout handled and signal emitted")

        self.__server_timeout_message()

    def __send_search_request(self, national_id, first_name, last_name, date_of_birth):
        """
        Sends search request to the server containing one or the combination of the following parameters: national_id,
        first_name, last_name or date_of_birth. Handles the server's response to determine if the search was successful
        or unsuccessful.

        :param national_id: The national ID of user.
        :type national_id: int
        :param first_name: The first name of user.
        :type first_name: str
        :param last_name: The last name  of user.
        :type last_name: str
        :param date_of_birth: The date of birth of the user in the format 'dd.MM.yyyy'.
        :type date_of_birth: str
        :return: True if the server responds with "search_successful", False otherwise.
        :rtype: bool
        """

        self.__client_logger.log_debug("Search request thread started execution")
        try:
            timeout = 5  # seconds

            self.__client_logger.log_debug("Search request timeout started")
            self.start_timer_signal.emit(timeout)

            self.__client_logger.log_debug("Started sending search request")
            header_data = {
                "Content-Type": "application/json",
                "Encoding": "utf-8"
            }

            request_data = {
                "command": "find_user",
                "national_id": national_id,
                "first_name": first_name,
                "last_name": last_name,
            }

            # Add date_of_birth to the request only if it has been changed
            if date_of_birth is not None:
                request_data["date_of_birth"] = date_of_birth

            # Combine header and request data into a single dictionary
            message = {
                "header": header_data,
                "request": request_data
            }

            # Serialize the combined dictionary into JSON format
            message_json = json.dumps(message)

            # Define a delimiter to mark the end of the message
            delimiter = b'\r\n'

            # Append the delimiter to the serialized message
            request = message_json.encode() + delimiter

            while self.running:
                response = self.tcp_client.send_request(request)
                if not self.running:
                    self.__client_logger.log_debug("Search request was stopped")
                    return False

                self.__client_logger.log_debug(f"TMS server response is {response}")

                response_data = json.loads(response['response'])

                if response_data["command"] == "search_successful":
                    self.search_successful_signal.emit()
                    limited_user_info = response_data.get("user_info")
                    self.__populate_search_results(limited_user_info)
                    self.__client_logger.log_debug(f"The search was successful!")
                    return True
                elif response_data["command"] == "search_unsuccessful":
                    self.search_unsuccessful_signal.emit()
                    self.__client_logger.log_debug(f"The search was unsuccessful!")
                    return False
                else:
                    self.__client_logger.log_debug(f"Server response error")
                    return False

        except Exception as exception:
            self.__client_logger.log_error(f"Unexpected exception: {exception}")
            return False

        finally:
            self.running = False
            self.__client_logger.log_debug("Search request thread finished")
            self.stop_timer_signal.emit()

    def extract_national_id(self, selected_text):
        """
        Extracts the national ID from the selected search result text.
        # """
        # Split the text and assume the national_id is the first part
        parts = selected_text.split()
        national_id = parts[0]  # Extract the first part which is the national ID
        return national_id

    def __populate_search_results(self, results):
        """
        Populates the search results combo box with user information provided by the server or displays "No matching
        results" placeholder text if no results are found.

        :param results: A list of dictionaries containing user information (national_id, first_name, last_name,
        date_of_birth).
        :type results: list of dict
        :return: None
        :rtype: None
        """

        self.__search_results_edit.clear()
        self.__search_results_edit.setStyleSheet("color: black;")
        if not results:
            self.__search_results_edit.setPlaceholderText("No matching results")
            self.__client_logger.log_debug(f"No matching results")

        else:
            for result in results:
                self.__client_logger.log_debug(f"The search result: {result}")
                display_text = (f"{result['national_id']} {result['first_name']} {result['last_name']} "
                                f"{result['date_of_birth']}")
                self.__search_results_edit.addItem(display_text)
                self.__client_logger.log_debug(f"Preliminary results of the search displayed")

    def __handle_search_result_selected(self, index):
        """
        A slot method that handles selection of a user from the search results combo box.

        :param index: The index of the selected item in the search results combo box.
        :type index: int
        :return: None
        :rtype: None
        """

        if index >= 0:
            # Get the selected item text
            selected_text = self.__search_results_edit.itemText(index)

            # Parse the selected text to extract the necessary information
            selected_info = selected_text.split()

            # Extract the national ID from the selected information
            national_id = str(selected_info[0])

            # Start a new thread to handle the request
            threading.Thread(target=self.__request_user_details, args=(national_id,)).start()

    def __request_user_details(self,  national_id):
        """
        Sends a request to the server to retrieve detailed information about a user identified by the provided national
        ID. Handles the server's response and emits signals to communicate the result.

        :param national_id: The national ID of the user as an integer value.
        :type national_id: int
        """

        self.__client_logger.log_debug("User details request thread started execution")
        try:
            timeout = 5  # seconds

            self.__timer.setSingleShot(True)
            self.__client_logger.log_debug("User info request timeout started")
            self.start_timer_signal.emit(timeout)

            self.__client_logger.log_debug("Entered __request_user_details method")
            header_data = {
                "Content-Type": "application/json",
                "Encoding": "utf-8"
            }

            request_data = {
                "command": "retrieve_user_details",
                "national_id": national_id
            }

            # Combine header and request data into a single dictionary
            message = {
                "header": header_data,
                "request": request_data
            }

            # Serialize the combined dictionary into JSON format
            message_json = json.dumps(message)

            # Define a delimiter to mark the end of the message
            delimiter = b'\r\n'

            # Append the delimiter to the serialized message
            request = message_json.encode() + delimiter

            try:
                response = self.tcp_client.send_request(request)
            except socket.timeout:
                self.__client_logger.log_error("Request to TMS server timed out")
                self.retrieving_unsuccessful_signal.emit()  # Emit signal for unsuccessful retrieval
                self.running = False  # Reset the running flag
                return

            self.__client_logger.log_debug(f"TMS server response is {response}")
            self.stop_timer_signal.emit()

            response = self.tcp_client.send_request(request)

            # Parse the JSON response
            response_data = json.loads(response['response'])

            if response_data["command"] == "retrieving_successful":
                self.__client_logger.log_debug("User details retrieved successfully")
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
                self.__client_logger.log_debug("Emit user_details_retrieved_signal to send user details")
                try:
                    self.__main_window.user_details_retrieved_signal.emit(user_details)
                    self.retrieving_successful_signal.emit()  # Emit signal for successful retrieval
                except Exception as exception:
                    self.__client_logger.log_error(f"Error emitting user_details_retrieved_signal: {exception}")
            elif response_data["command"] == "retrieving_unsuccessful":
                self.__client_logger.log_debug("Retrieving of user details was unsuccessful!")
                self.retrieving_unsuccessful_signal.emit()
            else:
                self.__client_logger.log_debug("Server response error")
                self.retrieving_unsuccessful_signal.emit()

        except (ConnectionError, TimeoutError, socket.error) as error:
            self.__client_logger.log_error(f"Error during socket communication: {error}")
            self.retrieving_unsuccessful_signal.emit()

        except Exception as exception:
            self.__client_logger.log_error(f"Unexpected exception: {exception}")
            self.retrieving_unsuccessful_signal.emit()

        finally:
            self.running = False
            self.__client_logger.log_debug("User details request thread finished")

    def handle_retrieving_successful(self):
        """
        Handles the successful retrieval of user details.

        Emits the request_complete signal and logs the event. Resets the running flag,
        signals thread completion, closes connections, and logs method exit.
        """
        try:
            self.request_complete.emit()
            self.__client_logger.log_debug("Request complete signal emitted")
        except Exception as exception:
            self.__client_logger.log_error(f"Error emitting request_complete signal:  {exception}")
        self.__thread_event.set()  # Signal that the thread has completed
        self.running = False  # Reset the running flag
        self.close()
        self.__client_logger.log_debug("Exiting __request_user_details method")

    def handle_retrieving_unsuccessful(self):
        """
        Handles the unsuccessful retrieval of user details.

        Emits the request_complete signal due to unsuccessful retrieval and logs the event.
        Resets the running flag, signals thread completion, closes connections, and logs method exit.
        """
        try:
            self.request_complete.emit()
            self.__client_logger.log_debug("Request complete signal emitted due to unsuccessful retrieval")
        except Exception as exception:
            self.__client_logger.log_error(f"Error emitting request_complete signal: {exception}")
        self.__thread_event.set()  # Signal that the thread has completed
        self.running = False  # Reset the running flag
        self.close()
        self.__client_logger.log_debug("Exiting __request_user_details method")

    def __missing_data_message(self):
        """
        Displays a warning message when the user tries to save data with missing entries.
        """

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowTitle("Form incomplete")
        warning_dialog.setText("Missing input!\nPlease fill any field or fields.")
        warning_dialog.exec()

    def __unexpected_error_message(self):
        """
        Displays a warning message in case of an unexpected error.
        """

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowTitle("Unexpected error")
        warning_dialog.setText("Unexpected error!\nPlease restart the application.")
        warning_dialog.exec()

    def __search_unsuccessful_message(self):
        """
        Displays a warning message in case of an unsuccessful search.
        """

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowTitle("Search unsuccessful")
        warning_dialog.setText("No user was wound!")
        warning_dialog.exec()

    def __search_successful_message(self):
        """
        Displays a confirmation message in case of a successful search.
        """

        confirmation_dialog = QMessageBox(self)
        confirmation_dialog.setWindowTitle("Search successful")
        confirmation_dialog.setText("Here is a result of the search!")
        confirmation_dialog.open()

    def __retrieving_successful_message(self):
        """
        Displays a confirmation message in case of successful data retrieval.
        """

        confirmation_dialog = QMessageBox(self)
        confirmation_dialog.setWindowTitle("Retrieving successful")
        confirmation_dialog.setText("Here is a result of the retrieving!")
        confirmation_dialog.open()

    def __retrieving_unsuccessful_message(self):
        """
        Displays a warning message in case of unsuccessful data retrieval.
        """

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowTitle("Retrieving unsuccessful")
        warning_dialog.setText("No data was wound!")
        warning_dialog.exec()

    def __server_timeout_message(self):
        """
        Displays a warning message in case of server timeout.
        """

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowTitle("Server timeout")
        warning_dialog.setText("No response from the server!")
        warning_dialog.exec()


if __name__ == "__main__":

    client_logger = TMSLogger("client")
    if not client_logger.setup():
        sys.exit(1)

    client_logger.log_debug("Client logger has been set up successfully")
    application = QApplication(sys.argv)
    host = "127.0.0.1"
    port = 65432
    # Create an instance of FindUserWindow
    find_user_window = FindUserWindow(client_logger, host, port, main_window=None)
    find_user_window.show()
    try:
        application.exec()
    except Exception as exception:
        client_logger.log_error(f"Unhandled exception: {exception}")  # Changed line
    finally:
        client_logger.log_debug("Application exited")  # Changed line
