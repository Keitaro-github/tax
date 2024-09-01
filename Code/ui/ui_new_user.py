import sys
import json
from PyQt6.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout,
                             QRadioButton, QButtonGroup, QDateEdit, QComboBox, QSpinBox)
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, pyqtSignal, QDate, QThread, QObject
from Code.tcp_ip.tcp_driver import TCPClient
from Code.utils.tms_logs import TMSLogger
from PyQt6.QtWidgets import QMessageBox


class SaveRequestThread(QObject):
    """
    Handles the process of saving user data in a separate thread to avoid blocking the main GUI thread.

    Attributes:
        request_finished (pyqtSignal): Signal emitted when the request is completed.
        tcp_client (TCPClient): The TCP client used to send and receive data.
        data (dict): The data to be sent to the server.
        client_logger (TMSLogger): Logger instance for logging debug and error messages.
    """
    request_finished = pyqtSignal(dict)

    def __init__(self, tcp_client, data, logger, parent=None):
        """
        Initializes the SaveRequestThread with necessary components.

        Args:
            tcp_client (TCPClient): The TCP client to use for sending requests.
            data (dict): The data to be sent to the server.
            logger (TMSLogger): Logger instance for logging messages.
            parent (QObject, optional): Parent QObject. Defaults to None.
        """
        super().__init__(parent)
        self.tcp_client = tcp_client
        self.data = data
        self.client_logger = logger

    def run(self):
        """
        Executes the thread's work: sends a request to the server and processes the response.

        Logs the request and response, and emits the result to the main thread.
        """
        self.client_logger.log_debug("Request thread started execution")
        try:
            # Define header and delimiter
            header_data = {
                "Content-Type": "application/json",
                "Encoding": "utf-8"
            }
            delimiter = b'\r\n'

            # Create the request message
            request_data = {
                "command": "save_new_user",
                **self.data
            }

            message = {
                "header": header_data,
                "request": request_data
            }

            message_json = json.dumps(message)
            request = message_json.encode() + delimiter

            self.client_logger.log_debug(f"Sending request to server: {request}")

            # Send the request and receive the response
            response = self.tcp_client.send_request(request)
            self.client_logger.log_debug(f"Server response: {response}")

            # Process the response
            if isinstance(response, bytes):
                response_str = response.decode()
                response_data = json.loads(response_str)
            elif isinstance(response, dict):
                response_data = response
            else:
                self.client_logger.log_error(f"Unexpected response type: {type(response)}")
                response_data = {"status": "error", "message": "Invalid response type received"}

            # Emit the response data to the main thread
            self.request_finished.emit(response_data)

        except Exception as exception:
            self.client_logger.log_error(f"Unexpected exception: {exception}")
            self.request_finished.emit({"status": "error", "message": str(exception)})


class NewUserWindow(QWidget):
    """
    Main window for adding a new user with a GUI form.

    Attributes:
        user_saved (pyqtSignal): Signal emitted when a user is successfully saved.
        __main_layout (QVBoxLayout): Layout for arranging the UI components.
        tcp_client (TCPClient): The TCP client used to send requests.
        __client_logger (TMSLogger): Logger instance for logging messages.
        __main_window (QWidget, optional): Parent window.
        thread (QThread, optional): The thread handling the save request.
        save_request_thread (SaveRequestThread, optional): Worker thread for saving the user data.
    """
    # Define the user_saved signal
    user_saved = pyqtSignal()

    def __init__(self, __client_logger: TMSLogger, host: str, port: int, main_window=None):
        """
        Initializes the NewUserWindow with necessary components and GUI setup.

        Args:
            __client_logger (TMSLogger): An instance of the logger.
            host (str): The host address for the TCP connection.
            port (int): The port number for the TCP connection.
            main_window (QWidget, optional): The parent window. Defaults to None.
        """
        super().__init__()
        self.__client_logger = __client_logger
        self.host = host
        self.port = port
        self.__client_logger.log_debug("Logger assigned successfully.")

        # Initialize the TCPClient with host and port
        self.tcp_client = TCPClient(host=host, port=port, tms_logger=self.__client_logger)
        self.__main_window = main_window

        # Call PyQt6 API to set current window's title.
        self.setWindowTitle("New user")
        # Call PyQt6 API to create a layout where all UI components are placed.
        self.__main_layout = QVBoxLayout()
        self.__client_logger.log_debug("Main layout created.")
        # Create all UI components on layout.
        self.__init_ui()
        self.__client_logger.log_debug("UI initialized.")
        # Call PyQt6 API to set prepared layout with all UI components.
        self.setLayout(self.__main_layout)
        self.__client_logger.log_debug("Layout set.")

        # Initialize the RequestThread without data
        self.thread = None
        self.save_request_thread = None

    def __init_ui(self):
        """
        Sets up the user interface including input fields and buttons.

        Creates and configures all UI components such as labels, line edits, combo boxes, and buttons.
        Arranges these components in layouts and adds them to the main layout of the window.
        """

        # Create and set up the label.
        self.__label = QLabel()
        self.__label.setStyleSheet("font: bold 16px;")
        label_national_id = QLabel("National ID")
        label_first_name = QLabel("First name")
        label_last_name = QLabel("Last name")
        label_date_of_birth = QLabel("Date of birth")
        label_gender = QLabel("Gender")
        label_address = QLabel("Address")
        label_phone_number = QLabel("Phone number")
        label_marital_status = QLabel("Marital status")

        # Create and set up line edit widget for entering first name.
        self.__national_id_edit = QLineEdit()
        self.__national_id_edit.setPlaceholderText("Enter national ID")

        # Create and set up line edit widget for entering first name.
        self.__first_name_edit = QLineEdit()
        self.__first_name_edit.setPlaceholderText("Enter first name")

        # Create and set up line edit widget for entering last name.
        self.__last_name_edit = QLineEdit()
        self.__last_name_edit.setPlaceholderText("Enter last name")

        # Create and set up date edit widget for entering date.
        self.__date_of_birth_edit = QDateEdit()
        self.__date_of_birth_edit.setStyleSheet("color: gray;")
        self.__date_of_birth_edit.setDate(QDate(1900, 1, 1))
        self.__date_of_birth_edit.editingFinished.connect(self.__handle_widget_edit)

        # Create and set up line edit widget for selection of gender.
        self.__gender_group = QButtonGroup(self)
        self.__radio_male = QRadioButton("male")
        self.__radio_female = QRadioButton("female")
        self.__gender_group.addButton(self.__radio_male)
        self.__gender_group.addButton(self.__radio_female)

        # Create and set up line edit widget for entering address.
        self.__address_edit = QLineEdit()
        self.__address_country_edit = QComboBox()
        self.__address_country_edit.setPlaceholderText("Country")
        self.__address_country_edit.setStyleSheet("color: gray;")
        self.__address_country_edit.currentIndexChanged.connect(self.__handle_widget_edit)
        countries = ["Denmark", "Finland", "Norway", "Sweden"]
        self.__address_country_edit.addItems(countries)
        self.__address_zip_code_edit = QLineEdit()
        self.__address_zip_code_edit.setPlaceholderText("Zip code")
        self.__address_zip_code_edit.setMaxLength(5)
        self.__address_zip_code_edit.textChanged.connect(self.__enforce_min_length)

        numeric_validator = QRegularExpressionValidator(QRegularExpression("[0-9]+"))
        self.__address_zip_code_edit.setValidator(numeric_validator)
        self.__address_city_edit = QLineEdit()
        self.__address_city_edit.setPlaceholderText("City")
        self.__address_street_edit = QLineEdit()
        self.__address_street_edit.setPlaceholderText("Street")
        self.__address_house_number_edit = QSpinBox()
        self.__address_house_number_edit.setStyleSheet("color: gray;")
        self.__address_house_number_edit.setRange(0, 9999)
        self.__address_house_number_edit.setValue(0)
        self.__address_house_number_edit.editingFinished.connect(self.__handle_widget_edit)

        # Create and set up line edit widget for entering phone number.
        self.__phone_country_code_edit = QComboBox()
        self.__phone_country_code_edit.setPlaceholderText("Country code")
        self.__phone_country_code_edit.setStyleSheet("color: gray;")

        # self.__set_widget_color(self.__phone_country_code_edit, "gray")
        self.__phone_country_code_edit.currentIndexChanged.connect(self.__handle_widget_edit)
        country_codes = ["Denmark +45", "Finland +358", "Norway +47", "Sweden +46"]
        self.__phone_country_code_edit.addItems(country_codes)
        self.__phone_number_edit = QLineEdit()
        self.__phone_number_edit.setPlaceholderText("XXXXXXXXX")
        self.__phone_number_edit.setMaxLength(9)
        self.__phone_number_edit.setValidator(numeric_validator)
        self.__phone_number_edit.textChanged.connect(self.__enforce_min_length)

        # Create and set up line edit widget for selection of marital status.
        self.__marital_status_group = QButtonGroup(self)
        self.__radio_single = QRadioButton("single")
        self.__radio_married = QRadioButton("married")
        self.__marital_status_group.addButton(self.__radio_single)
        self.__marital_status_group.addButton(self.__radio_married)

        # Create and set up button widget for saving data.
        self.__ok_button = QPushButton()
        self.__ok_button.setText("OK")
        self.__ok_button.clicked.connect(self.__click_ok_button)
        self.__ok_button.setToolTip("Press OK to save entered data")

        # Create and set up button widget for cancel procedure.
        self.__cancel_button = QPushButton()
        self.__cancel_button.setText("Cancel")
        self.__cancel_button.clicked.connect(self.__click_cancel_button)
        self.__cancel_button.setToolTip("Press Cancel to abort operation")

        # Create a horizontal layout for the labels and widgets
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

        layout_gender = QHBoxLayout()
        layout_gender.addWidget(label_gender)
        layout_gender.addWidget(self.__radio_male)
        layout_gender.addWidget(self.__radio_female)

        layout_address = QHBoxLayout()
        layout_address.addWidget(label_address)
        layout_address.addWidget(self.__address_country_edit)
        layout_address.addWidget(self.__address_zip_code_edit)
        layout_address.addWidget(self.__address_city_edit)
        layout_address.addWidget(self.__address_street_edit)
        layout_address.addWidget(self.__address_house_number_edit)

        layout_phone_number = QHBoxLayout()
        layout_phone_number.addWidget(label_phone_number)
        layout_phone_number.addWidget(self.__phone_country_code_edit)
        layout_phone_number.addWidget(self.__phone_number_edit)

        layout_marital_status = QHBoxLayout()
        layout_marital_status.addWidget(label_marital_status)
        layout_marital_status.addWidget(self.__radio_single)
        layout_marital_status.addWidget(self.__radio_married)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.__ok_button)
        button_layout.addWidget(self.__cancel_button)

        # Add the widgets to the main layout
        self.__main_layout.addLayout(layout_national_id)
        self.__main_layout.addLayout(layout_first_name)
        self.__main_layout.addLayout(layout_last_name)
        self.__main_layout.addLayout(layout_date_of_birth)
        self.__main_layout.addLayout(layout_gender)
        self.__main_layout.addLayout(layout_address)
        self.__main_layout.addLayout(layout_phone_number)
        self.__main_layout.addLayout(layout_marital_status)
        self.__main_layout.addLayout(button_layout)

    def __click_ok_button(self):
        """
        Handles the OK button click event.

        This method is called when the OK button is clicked. It retrieves user input from various UI components,
        formats the data into a dictionary, and sends it to a server for further processing.
        """
        national_id = self.__national_id_edit.text().strip()
        first_name = self.__first_name_edit.text().strip()
        last_name = self.__last_name_edit.text().strip()
        date_of_birth = self.__date_of_birth_edit.date().toString("yyyy-MM-dd")
        gender = "male" if self.__radio_male.isChecked() else "female"
        address_country = self.__address_country_edit.currentText().strip()
        address_zip_code = self.__address_zip_code_edit.text().strip()
        address_city = self.__address_city_edit.text().strip()
        address_street = self.__address_street_edit.text().strip()
        address_house_number = str(self.__address_house_number_edit.value()).strip()

        phone_country_code_text = self.__phone_country_code_edit.currentText().strip()

        # Check if phone_country_code_text is not empty and can be split
        if phone_country_code_text:
            phone_country_code = phone_country_code_text.split()[-1].strip()
        else:
            phone_country_code = ""

        phone_number = self.__phone_number_edit.text().strip()
        marital_status = "single" if self.__radio_single.isChecked() else "married"

        # Validate the input fields
        if not all([national_id, first_name, last_name, date_of_birth != "1900-01-01",
                    address_country, address_zip_code, address_city, address_street,
                    address_house_number != "0", phone_country_code, phone_number]):
            QMessageBox.warning(self, "Validation Error", "Please fill in all required fields.")
            return

        data = {
            "national_id": national_id,
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "address_country": address_country,
            "address_zip_code": address_zip_code,
            "address_city": address_city,
            "address_street": address_street,
            "address_house_number": address_house_number,
            "phone_country_code": phone_country_code,
            "phone_number": phone_number,
            "marital_status": marital_status,
        }

        self.__client_logger.log_debug(f"User input collected: {data}")

        self.save_new_user_request(data)

    def __click_cancel_button(self):
        """
        Handles the Cancel button click event.

        This method is called when the Cancel button is clicked. It closes the current window.
        """
        self.__client_logger.log_debug("Cancel button clicked. Closing the window.")
        self.close()

    def __handle_widget_edit(self):
        """
        Handles changes made to widget values, providing real-time feedback or validation.
        """
        sender = self.sender()
        self.__client_logger.log_debug(f"Widget edit finished for: {sender}")
        if isinstance(sender, (QComboBox, QDateEdit, QSpinBox)):
            sender.setStyleSheet("color: black;")
            self.__client_logger.log_debug(f"Set widget color to black for: {sender}")

    def __set_widget_color(self, widget, color):
        """
        Sets the color of a widget.

        Args:
            widget (QWidget): The widget to set the color for.
            color (str): The color to set.
        """
        if isinstance(widget, QSpinBox):
            widget.setStyleSheet(f"QSpinBox::edit {{ color: {color}; }}")
        elif isinstance(widget, QDateEdit):
            widget.setStyleSheet(f"QDateEdit::edit {{ color: {color}; }}")
        elif isinstance(widget, QComboBox):
            widget.setStyleSheet(f"QComboBox::item {{ color: {color}; }}")
            widget.setStyleSheet(f"QComboBox QAbstractItemView {{ color: {color}; }}")
        else:
            widget.setStyleSheet(f"color: {color};")
        widget.repaint()  # Force the widget to repaint
        self.__client_logger.log_debug(f"Set color for {widget} to {color}")

    def __enforce_min_length(self):
        """
        Ensures that user input in specific fields meets minimum length requirements.

        This function is used to validate fields such as address zip code and phone number,
        ensuring that the user enters enough digits.
        """
        sender_widget = self.sender()
        if isinstance(sender_widget, QLineEdit):
            if sender_widget == self.__address_zip_code_edit:
                min_length = 4
            elif sender_widget == self.__phone_number_edit:
                min_length = 9
            else:
                self.__client_logger.log_debug(f"Unexpected sender widget: {sender_widget}")
                return

            if len(sender_widget.text()) < min_length:
                sender_widget.setStyleSheet("QLineEdit { background-color: rgba(255, 0, 0, 0.2); }")
            else:
                sender_widget.setStyleSheet("")
        else:
            self.__client_logger.log_debug(f"Sender widget is not a QLineEdit: {sender_widget}")

    def save_new_user_request(self, data):
        """
        Saves a new user request by sending data to a TCP server.

        This method sends a JSON-encoded request to a TCP server to save a new user with the provided data. It
        waits for the server response and emits a signal upon successful saving.

        Args:
            data (dict): The user data to be saved.
        """
        self.__client_logger.log_debug(f"Preparing to send new user request with data: {data}")

        # Create a QThread
        self.thread = QThread()

        # Create the worker and move it to the thread
        self.save_request_thread = SaveRequestThread(self.tcp_client, data, self.__client_logger)
        self.save_request_thread.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.save_request_thread.run)
        self.save_request_thread.request_finished.connect(self.handle_request_finished)
        self.save_request_thread.request_finished.connect(self.thread.quit)  # Stop the thread once done
        self.save_request_thread.request_finished.connect(self.save_request_thread.deleteLater)  # Clean up the worker
        self.thread.finished.connect(self.thread.deleteLater)  # Clean up the thread

        # Start the thread
        self.thread.start()

    def handle_request_finished(self, response):
        """
        Handles the response from the server after the save request is completed.

        Displays a message box with the result and closes the window if the save was successful.
        """

        self.__client_logger.log_debug(f"Received response from server: {response}")

        try:
            response_data = json.loads(response.get("response", "{}"))
            self.__client_logger.log_debug(f"Parsed response data: {response_data}")

            if response_data.get("status") == "success":
                self.__client_logger.log_info("User successfully saved.")
                QMessageBox.information(self, "Addition status", "The user was saved successfully!")
                self.reset_fields()
                self.user_saved.emit()
            else:
                error_message = response_data.get("message", "Unknown error occurred")
                self.__client_logger.log_error(f"Failed to save user. Response: {error_message}")
                QMessageBox.warning(self, "Save Error", f"Failed to save user: {error_message}")
        except json.JSONDecodeError as json_error:
            self.__client_logger.log_error(f"JSON decoding error: {json_error}")
            QMessageBox.critical(self, "Error", f"An unexpected JSON decoding error occurred: {json_error}")
        except Exception as exception:
            self.__client_logger.log_error(f"An unexpected error occurred: {exception}")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {exception}")

    def reset_fields(self):
        """
        Resets all input fields in the form.
        """
        self.__national_id_edit.clear()
        self.__first_name_edit.clear()
        self.__last_name_edit.clear()
        self.__date_of_birth_edit.setDate(QDate(1900, 1, 1))
        self.__date_of_birth_edit.setStyleSheet("color: gray;")

        self.__gender_group.setExclusive(False)
        self.__radio_male.setChecked(False)
        self.__radio_female.setChecked(False)
        self.__gender_group.setExclusive(True)

        # Reset QComboBox (address_country_edit)
        self.__address_country_edit.setCurrentIndex(-1)  # Reset to show placeholder text
        self.__address_country_edit.setPlaceholderText("Country")  # Ensure placeholder text is set
        self.__address_country_edit.setStyleSheet("color: gray;")  # Reset color

        self.__address_zip_code_edit.clear()
        self.__address_city_edit.clear()
        self.__address_street_edit.clear()
        self.__address_house_number_edit.setValue(0)
        self.__address_house_number_edit.setStyleSheet("color: gray;")

        self.__phone_country_code_edit.setCurrentIndex(-1)
        self.__phone_country_code_edit.setPlaceholderText("Country code")
        self.__phone_country_code_edit.setStyleSheet("color: gray;")

        self.__phone_number_edit.clear()
        self.__marital_status_group.setExclusive(False)
        self.__radio_single.setChecked(False)
        self.__radio_married.setChecked(False)
        self.__marital_status_group.setExclusive(True)

        # # Clear any background color styles
        self.__address_zip_code_edit.setStyleSheet("")
        self.__phone_number_edit.setStyleSheet("")
        # self.__date_of_birth_edit.setStyleSheet("")
        # self.__address_house_number_edit.setStyleSheet("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_logger = TMSLogger("client")

    # Ensure the logger is properly set up
    if not client_logger.setup():
        sys.exit(1)

    host = 'localhost'
    port = 65432
    window = NewUserWindow(client_logger, "localhost", port)
    window.show()
    sys.exit(app.exec())
