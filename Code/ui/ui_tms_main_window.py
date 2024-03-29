import sys
from PyQt6.QtWidgets import (QWidget, QApplication, QLabel, QHBoxLayout,
                             QTabWidget, QSplitter, QFormLayout, QMenuBar)
from PyQt6.QtGui import (QAction)
from Code.ui.ui_new_user import NewUserWindow
from Code.ui.ui_find_user import FindUserWindow
from PyQt6.QtCore import pyqtSignal


class TMSMainWindow(QWidget):
    user_details_retrieved_signal = pyqtSignal(dict)
    def __init__(self, username, password, host, port):
        super().__init__()

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

    def __show_new_user_window(self):
        """
        Show NewUserWindow UI to create new user.
        :return: None
        """

        self.__new_user_window = NewUserWindow(self.host, self.port)
        self.__new_user_window.show()

    def __show_find_user_window(self):
        """
        Show FindUserWindow UI to find user.
        :return: None
        """

        self.__find_user_window = FindUserWindow(self.host, self.port, main_window=self)
        self.__find_user_window.show()

    def update_main_window(self, user_details):
        # Define what happens when the request is complete
        self.populate_user_information(user_details)

    def populate_user_information(self, user_details):
        """
        Populate the main window with the retrieved user information.
        """
        print("Received user details:", user_details)
        try:
            if user_details is not None:
                # Update labels with user information
                self.label_national_id.setText(f"National ID: {user_details['national_id']}")
                self.label_name.setText(f"User name: {user_details['first_name']} {user_details['last_name']}")
                self.label_date_of_birth.setText(f"Date of birth: {user_details['date_of_birth']}")
                self.label_gender.setText(f"Gender: {user_details['gender']}")
                address_country = user_details.get('address_country', '')
                address_zip_code = user_details.get('address_zip_code', '')
                address_zip_code = address_zip_code.lstrip('*')
                address_city = user_details.get('address_city', '')
                address_street = user_details.get('address_street', '')
                address_house_number = user_details.get('address_house_number', '')
                address_text = (f"{address_street} {address_house_number}, {address_zip_code} {address_city}, "
                                f"{address_country}")
                self.label_address.setText(f"Address: {address_text}")
                phone_country = user_details.get('phone_country', '')
                phone_number = user_details.get('phone_number', '')
                phone_text = f"+{phone_country} {phone_number}"
                self.label_phone_number.setText(f"Phone number: {phone_text}")
                self.label_marital_status.setText(f"Marital status: {user_details['marital_status']}")
                self.label_tax_rate.setText(f"Tax rate: {user_details['tax_rate']}")
                self.label_yearly_income.setText(f"Yearly income: {user_details['yearly_income']}")
                self.label_advance_tax.setText(f"Advance tax: {user_details['advance_tax']}")
                self.label_tax_paid_this_year.setText(f"Tax paid this year: {user_details['tax_paid_this_year']}")
                self.label_property_value.setText(f"Property value: {user_details['property_value']}")
                self.label_loans.setText(f"Loans: {user_details['loans']}")
                self.label_property_tax.setText(f"Property tax: {user_details['property_tax']}")

                print("User information populated successfully.")  # Debugging output
            else:
                print("User details are None. Unable to populate information.")  # Debugging output
        except Exception as e:
            print("Error while populating user information:", e)  # Error handling


if __name__ == "__main__":
    app = QApplication(sys.argv)
    host = "127.0.0.1"
    port = 65432

    try:
        username = sys.argv[1]
        password = sys.argv[2]
        main_window = TMSMainWindow(username, password, host, port)

    except IndexError:
        main_window = TMSMainWindow(None, None, host, port)

    main_window.show()
    sys.exit(app.exec())
