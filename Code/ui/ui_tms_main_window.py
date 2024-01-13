import sys
from PyQt6.QtWidgets import (QWidget, QApplication, QLabel, QHBoxLayout,
                             QTabWidget, QSplitter, QFormLayout, QMenuBar)
from PyQt6.QtGui import (QAction)
from tax.Code.ui.ui_new_user import NewUserWindow


class TMSMainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create the main layout
        main_layout = QHBoxLayout()

        # Left side with information
        left_widget = QWidget()
        form_layout = QFormLayout()
        self.label_info = QLabel("User overview")
        self.label_info.setStyleSheet("font: bold 16px;")
        self.label_national_id = QLabel("National ID")
        self.label_name = QLabel("User name")
        self.label_id = QLabel("User ID")
        form_layout.addRow(self.label_info, None)
        form_layout.addRow(self.label_national_id, None)
        form_layout.addRow(self.label_name, None)
        form_layout.addRow(self.label_id, None)

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
        action_create_new_user.triggered.connect(self.create_new_user_window)
        action_find_user.triggered.connect(self.find_user_window)

        # Add actions to the menu and submenu
        user_menu.addAction(action_exit)

        # Add actions to the "User options" submenu
        user_options_submenu.addAction(action_create_new_user)
        user_options_submenu.addAction(action_find_user)

        # Connect exit action to close the application
        action_exit.triggered.connect(self.close)

        main_layout.setMenuBar(menubar)

        self.new_user_window = None
        self.find_user_window = None

    def create_new_user_window(self):
        self.new_user_window = NewUserWindow()
        self.new_user_window.show()

    def find_user_window(self):
        from ui_find_user import FindUserWindow
        self.find_user_window_instance = FindUserWindow(self)
        self.find_user_window_instance.show()

    def populate_user_information(self, user_info):
        """
        Populate the main window with the retrieved user information.
        """
        if user_info is not None:
            # Update labels with user information
            self.label_national_id.setText(f"National ID: {user_info['national_id']}")
            self.label_name.setText(f"User name: {user_info['first_name']} {user_info['last_name']}")
            self.label_id.setText(f"User ID: {user_info['user_id']}")
            self.label_date_of_birth.setText(f"Date of birth: {user_info['date_of_birth']}")
            self.label_gender.setText(f"Gender: {user_info['gender']}")
            address_country = user_info.get('address_country', '')
            address_zip_code = user_info.get('address_zip_code', '')
            address_zip_code = address_zip_code.lstrip('*')
            address_city = user_info.get('address_city', '')
            address_street = user_info.get('address_street', '')
            address_house_number = user_info.get('address_house_number', '')
            address_text = (f"{address_street} {address_house_number}, {address_zip_code} {address_city}, "
                            f"{address_country}")
            self.label_address.setText(f"Address: {address_text}")
            phone_country = user_info.get('phone_country', '')
            phone_number = user_info.get('phone_number', '')
            phone_text = f"+{phone_country} {phone_number}"
            self.label_phone_number.setText(f"Phone number: {phone_text}")
            self.label_marital_status.setText(f"Marital status: {user_info['marital_status']}")
            self.label_tax_rate.setText(f"Tax rate: {user_info['tax_rate']}")
            self.label_yearly_income.setText(f"Yearly income: {user_info['yearly_income']}")
            self.label_advance_tax.setText(f"Advance tax: {user_info['advance_tax']}")
            self.label_tax_paid_this_year.setText(f"Tax paid this year: {user_info['tax_paid_this_year']}")
            self.label_property_value.setText(f"Property value: {user_info['property_value']}")
            self.label_loans.setText(f"Loans: {user_info['loans']}")
            self.label_property_tax.setText(f"Property tax: {user_info['property_tax']}")

            print(f"User Information for National ID {user_info['national_id']} "
                  f"{user_info['first_name']} {user_info['last_name']} {user_info['date_of_birth']}")
        else:
            print(f"User Information not found.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = TMSMainWindow()
    main_window.show()
    sys.exit(app.exec())
