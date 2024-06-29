import sys
import Code
import json
from PyQt6.QtWidgets import (QWidget, QApplication, QLabel, QHBoxLayout,
                             QTabWidget, QSplitter, QFormLayout, QMenuBar)
from PyQt6.QtGui import (QAction)
from Code.utils.tms_logs import TMSLogger
from Code.ui.ui_new_user import NewUserWindow
from Code.ui.ui_find_user import FindUserWindow
from PyQt6.QtCore import pyqtSignal


class TMSMainWindow(QWidget):
    """
    Represents the main window of the Tax Management System (TMS) application, created using PyQt6 for user interaction
    with the GUI.

    Attributes:
        username (str): The username of the TMS user.
        password (str): The password of the TMS user.
        host (str): The hostname or IP address of the server to connect to.
        port (int): The port used by the server for the connection.
        main_layout (QVBoxLayout): A layout widget for organizing GUI components.
        user_details_retrieved_signal (pyqtSignal): A signal emitted when user details are retrieved.
    """

    user_details_retrieved_signal = pyqtSignal(dict)

    def __init__(self, client_logger: TMSLogger, username: str, password: str, host: str, port: int):
        """
        Initializes a new instance of the TMSMainWindow class.

        Args:
            client_logger (TMSLogger): TMS Logger instance.
            username (str): The username of the TMS user.
            password (str): The password of the TMS user.
            host (str): The server's hostname or IP address to connect to.
            port (int): The port used by the server to connect to.
        """
        super().__init__()

        self.__client_logger = client_logger
        self.__username = username
        self.__password = password
        self.host = host
        self.port = port

        # Connect signal from FindUserWindow to slot in TMSMainWindow
        self.user_details_retrieved_signal.connect(self.populate_user_information)

        # Create the main layout
        main_layout = QHBoxLayout()

        # Left side with information
        left_widget = QWidget()
        form_layout = QFormLayout()
        self.label_info = QLabel("User overview")
        self.label_info.setStyleSheet("font: bold 16px;")
        self.label_national_id = QLabel("National ID")
        self.label_name = QLabel("User name")
        form_layout.addRow(self.label_info, None)
        form_layout.addRow(self.label_national_id, None)
        form_layout.addRow(self.label_name, None)

        left_widget.setLayout(form_layout)

        right_widget = QTabWidget()

        # Create tabs
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        # Add content to tab1
        tab1_layout = QFormLayout()
        self.label_date_of_birth = QLabel("Date  of birth")
        self.label_gender = QLabel("Gender")
        self.label_address = QLabel("Address")
        self.label_phone_number = QLabel("Phone number")
        self.label_marital_status = QLabel("Marital status")
        tab1_layout.addRow(self.label_date_of_birth, None)
        tab1_layout.addRow(self.label_gender, None)
        tab1_layout.addRow(self.label_address, None)
        tab1_layout.addRow(self.label_phone_number, None)
        tab1_layout.addRow(self.label_marital_status, None)

        tab1.setLayout(tab1_layout)

        # Add content to tab2
        tab2_layout = QFormLayout()
        self.label_tax_rate = QLabel("Tax rate")
        self.label_yearly_income = QLabel("Yearly income")
        self.label_advance_tax = QLabel("Advance tax")
        self.label_tax_paid_this_year = QLabel("Tax paid this year")
        tab2_layout.addRow(self.label_tax_rate, None)
        tab2_layout.addRow(self.label_yearly_income, None)
        tab2_layout.addRow(self.label_advance_tax, None)
        tab2_layout.addRow(self.label_tax_paid_this_year, None)

        tab2.setLayout(tab2_layout)

        # Add content to tab3
        tab3_layout = QFormLayout()
        self.label_property_value = QLabel("Property value")
        self.label_loans = QLabel("Loans")
        self.label_property_tax = QLabel("Property tax")
        tab3_layout.addRow(self.label_property_value, None)
        tab3_layout.addRow(self.label_loans, None)
        tab3_layout.addRow(self.label_property_tax, None)

        tab3.setLayout(tab3_layout)

        # Add tabs to the tab widget
        right_widget.addTab(tab1, "General info")
        right_widget.addTab(tab2, "Tax card")
        right_widget.addTab(tab3, "Assets and liabilities")
        # Set font size for tab names
        tab_font = right_widget.font()
        tab_font.setPointSize(12)  # Set the desired font size for tab names
        right_widget.setFont(tab_font)

        # Set font size for tab content
        content_font = tab1.font()
        content_font.setPointSize(10)
        tab1.setFont(content_font)
        tab2.setFont(content_font)
        tab3.setFont(content_font)

        # Create a splitter and add left and right widgets to it
        splitter = QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        # Add the left and right sides to the main layout
        main_layout.addWidget(splitter)

        # Set the main layout for the main window
        self.setLayout(main_layout)

        self.setWindowTitle("Tax Management System")
        self.setGeometry(100, 100, 800, 400)

        menubar = QMenuBar()

        user_menu = menubar.addMenu("User menu")

        # Create a submenu for "User menu"
        user_options_submenu = user_menu.addMenu("User options")

        # Create actions for the menu
        action_create_new_user = QAction("Create new user", self)
        action_find_user = QAction("Find user", self)
        action_exit = QAction("Exit", self)

        # Connect the options to the functions
        action_create_new_user.triggered.connect(self.__show_new_user_window)
        action_find_user.triggered.connect(self.__show_find_user_window)

        # Add actions to the menu and submenu
        user_menu.addAction(action_exit)

        # Add actions to the "User options" submenu
        user_options_submenu.addAction(action_create_new_user)
        user_options_submenu.addAction(action_find_user)

        # Connect exit action to close the application
        action_exit.triggered.connect(self.close)

        main_layout.setMenuBar(menubar)

        self.__new_user_window = None
        self.__find_user_window = None

        self.__client_logger.log_debug("Main TMS window has been launched")

    def __show_new_user_window(self):
        """
        Displays NewUserWindow UI to create new user.
        """

        self.__new_user_window = NewUserWindow(self.__client_logger, self.host, self.port)
        self.__new_user_window.show()

    def __show_find_user_window(self):
        """
        Displays FindUserWindow UI to find user.
        """

        self.__find_user_window = FindUserWindow(self.__client_logger, self.host, self.port, main_window=self)
        self.__find_user_window.show()

    def populate_user_information(self, user_details):
        """
        Populates the main window with the retrieved user information.
        """
        self.__client_logger.log_debug(f"Received user details: {user_details}")
        try:
            if user_details is not None:
                # Update labels with user information
                self.label_national_id.setText(f"National ID: {user_details['national_id']}")
                self.label_name.setText(f"User name: {user_details['first_name']} {user_details['last_name']}")
                self.label_date_of_birth.setText(f"Date of birth: {user_details['date_of_birth']}")
                self.label_gender.setText(f"Gender: {user_details['gender']}")
                address_country = user_details.get('address_country', '')
                address_zip_code = user_details.get('address_zip_code', '')
                # address_zip_code = address_zip_code.lstrip('*')
                address_city = user_details.get('address_city', '')
                address_street = user_details.get('address_street', '')
                address_house_number = user_details.get('address_house_number', '')
                address_text = (f"{address_street} {address_house_number}, {address_zip_code} {address_city}, "
                                f"{address_country}")
                self.label_address.setText(f"Address: {address_text}")
                phone_country_code = user_details.get('phone_country_code', '')
                phone_number = user_details.get('phone_number', '')
                phone_text = f"{phone_country_code} {phone_number}"
                self.label_phone_number.setText(f"Phone number: {phone_text}")
                self.label_marital_status.setText(f"Marital status: {user_details['marital_status']}")

                # Format numerical fields with commas, defaulting to empty string if None
                yearly_income = f"{user_details['yearly_income']:,}" if user_details['yearly_income'] is not None else ''
                advance_tax = f"{user_details['advance_tax']:,}" if user_details['advance_tax'] is not None else ''
                tax_paid_this_year = f"{user_details['tax_paid_this_year']:,}" if user_details[
                                                                                      'tax_paid_this_year'] is not None else ''
                property_value = f"{user_details['property_value']:,}" if user_details[
                                                                              'property_value'] is not None else ''
                loans = f"{user_details['loans']:,}" if user_details['loans'] is not None else ''
                property_tax = f"{user_details['property_tax']:,}" if user_details['property_tax'] is not None else ''

                self.label_tax_rate.setText(f"Tax rate: {user_details['tax_rate']}")
                self.label_yearly_income.setText(f"Yearly income: {yearly_income}")
                self.label_advance_tax.setText(f"Advance tax: {advance_tax}")
                self.label_tax_paid_this_year.setText(f"Tax paid this year: {tax_paid_this_year}")
                self.label_property_value.setText(f"Property value: {property_value}")
                self.label_loans.setText(f"Loans: {loans}")
                self.label_property_tax.setText(f"Property tax: {property_tax}")

                self.__client_logger.log_debug("User information populated successfully")
            else:
                self.__client_logger.log_debug("User details are None")
        except Exception as exception:
            self.__client_logger.log_debug(f"Unexpected exception: {exception}")


if __name__ == "__main__":

    client_logger = TMSLogger("client")
    if not client_logger.setup():
        sys.exit(1)

    try:
        with open(Code.TCP_CONFIGS, 'r') as tcp_config_file:
            tcp_configs = json.loads(tcp_config_file.read())
    except OSError:
        client_logger.log_critical(f"Could not get TCP configs. Please, check file {Code.TCP_CONFIGS}")
        sys.exit(1)
    else:
        client_logger.log_debug("TCP configs have been read successfully")
    # Parse TCP configurations represented in JSON format.
    try:
        host = tcp_configs["host"]
        port = tcp_configs["port"]
    except KeyError as exception:
        client_logger.log_critical(f"Unexpected exception: {exception}")
        sys.exit(1)
    else:
        client_logger.log_debug("TCP configs have been parsed successfully")

    app = QApplication(sys.argv)

    username = None
    password = None

    main_window = TMSMainWindow(client_logger, username, password, host, port)

    main_window.show()
    sys.exit(app.exec())
