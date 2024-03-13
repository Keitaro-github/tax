import sys
from PyQt6.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout,
                             QRadioButton, QButtonGroup, QDateEdit, QMessageBox, QComboBox, QSpinBox)
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, pyqtSignal
import socket
import json


class NewUserWindow(QWidget):
    # Define the user_saved signal
    user_saved = pyqtSignal()

    def __init__(self, host, port):
        super().__init__()  # Initialize default constructor of parent class
        self.host = host  # Define the host attribute
        self.port = port  # Define the port attribute

        # Call PyQt6 API to set current window's title.
        self.setWindowTitle("New user")
        # Call PyQt6 API to create a layout where all UI components are placed.
        self.__main_layout = QVBoxLayout()
        # Create all UI components on layout.
        self.__init_ui()
        # Call PyQt6 API to set prepared layout with all UI components.
        self.setLayout(self.__main_layout)

    def __init_ui(self):
        """
        This function is intended to create all UI components.
        :return: None
        :rtype:
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
        self.__set_widget_color(self.__date_of_birth_edit, "gray")
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
        self.__set_widget_color(self.__address_country_edit, "gray")
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
        self.__address_house_number_edit.setRange(1, 999)
        self.__set_widget_color(self.__address_house_number_edit, "gray")
        self.__address_house_number_edit.editingFinished.connect(self.__handle_widget_edit)

        # Create and set up line edit widget for entering phone number.
        self.__phone_country_edit = QComboBox()
        self.__phone_country_edit.setPlaceholderText("Country code")
        self.__set_widget_color(self.__phone_country_edit, "gray")
        self.__phone_country_edit.currentIndexChanged.connect(self.__handle_widget_edit)
        country_codes = ["Denmark +45", "Finland +358", "Norway +47", "Sweden +46"]
        self.__phone_country_edit.addItems(country_codes)
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
        layout_phone_number.addWidget(self.__phone_country_edit)
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

    def __handle_widget_edit(self):
        # Slot method to handle the editingFinished signal for various widgets
        sender = self.sender()
        if isinstance(sender, (QComboBox, QDateEdit, QSpinBox)):
            # Change the text color to black once the widget is edited
            self.__set_widget_color(sender, "black")

    def __set_widget_color(self, widget, color):
        # Set the text color of the widget
        widget.setStyleSheet(f"{widget.metaObject().className()} {{ color: {color}; }}")

    def __are_all_fields_filled(self, national_id, first_name, last_name, date_of_birth, gender, address_country,
                                address_zip_code, address_city, address_street, address_house_number,
                                phone_country_code, phone_number, marital_status):
        """
        Check if all the fields are filled.
        """
        return all([
            national_id,
            first_name,
            last_name,
            date_of_birth,
            gender is not None,
            address_country,
            address_zip_code,
            address_city,
            address_street,
            address_house_number,
            phone_country_code,
            phone_number,
            marital_status is not None
        ])

    def __click_cancel_button(self):
        """
        This function is intended to be called automatically when the user clicks on Cancel button.
        :return: None
        """

        self.close()

    def __click_ok_button(self):
        """
        This function is intended to be called automatically when the user clicks on OK button.
        """

        # Collect data from all widgets
        national_id = self.__national_id_edit.text()
        first_name = self.__first_name_edit.text()
        last_name = self.__last_name_edit.text()
        date_of_birth = self.__date_of_birth_edit.date().toString("dd.MM.yyyy")
        if self.__radio_male.isChecked():
            gender = "male"
        elif self.__radio_female.isChecked():
            gender = "female"
        else:
            self.__missing_data_message()
            return
        address_country = self.__address_country_edit.currentText()
        address_zip_code = self.__address_zip_code_edit.text()
        address_city = self.__address_city_edit.text()
        address_street = self.__address_street_edit.text()
        address_house_number = self.__address_house_number_edit.text()
        phone_country_code = self.__phone_country_edit.currentText()
        phone_number = self.__phone_number_edit.text()
        if self.__radio_single.isChecked():
            marital_status = "single"
        elif self.__radio_married.isChecked():
            marital_status = "married"
        else:
            self.__missing_data_message()
            return
        if not self.__are_all_fields_filled(national_id, first_name, last_name, date_of_birth, gender, address_country,
                                            address_zip_code, address_city, address_street, address_house_number,
                                            phone_country_code, phone_number, marital_status):
            self.__missing_data_message()
            return

        if self.__are_all_fields_filled(national_id, first_name, last_name, date_of_birth, gender, address_country,
                                        address_zip_code, address_city, address_street, address_house_number,
                                        phone_country_code, phone_number, marital_status):
            self.__saved_successfully_message()
            self.close()

        else:
            self.__unexpected_error_message()

        # Call the function to save new user with the collected data
        self.save_new_user_request(national_id, first_name, last_name, date_of_birth, gender, address_country,
                                   address_zip_code, address_city, address_street, address_house_number,
                                   phone_country_code, phone_number, marital_status)

    def save_new_user_request(self, national_id, first_name, last_name, date_of_birth, gender, address_country,
                              address_zip_code, address_city, address_street, address_house_number,
                              phone_country_code, phone_number, marital_status):
        try:
            # Create a socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                # Connect to the server
                client_socket.connect((self.host, self.port))

                header_data = {
                    "Content-Type": "application/json",
                    "Encoding": "utf-8"
                }

                request_data = {
                    "command": "save_new_user",
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
                    "marital_status": marital_status
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
                message_json_with_delimiter = message_json.encode() + delimiter

                # Send the JSON-formatted message over the socket
                client_socket.sendall(message_json_with_delimiter)

                response = client_socket.recv(1024).decode()

                if response == "New user saved successfully":
                    self.__saved_successfully_message()
                    self.user_saved.emit()
                    print("New user saved successfully")
                elif response == "User was not saved :-(":
                    self.__unexpected_error_message()
                    print("User was not saved :-(")
                else:
                    print("Server response error 'here'")
                    return False
        except Exception as e:
            print("Error", e)
            return False

    def __enforce_min_length(self):
        sender_widget = self.sender()

        if sender_widget == self.__address_zip_code_edit:
            min_length = 4
        elif sender_widget == self.__phone_number_edit:
            min_length = 9
        else:
            self.__unexpected_error_message()
            return

        if len(sender_widget.text()) < min_length:
            sender_widget.setStyleSheet("QLineEdit { background-color: rgba(255, 0, 0, 0.2); }")
        else:
            sender_widget.setStyleSheet("")

    def __missing_data_message(self):
        """
              This message is intended to be called automatically when the user tries to save data with missing entries.
              :return: None
              """

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowTitle("Form incomplete")
        warning_dialog.setText("Some fields are missing information!\nPlease fill out empty fields.")
        warning_dialog.exec()

    def __wrong_format_data_message(self):
        """
              This message is intended to be called automatically when the user tries to enter data in wrong format.
              :return: None
              """

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowTitle("Data entered in wrong format")
        warning_dialog.setText("Some fields are missing information!\nPlease fill out empty fields.")
        warning_dialog.exec()

    def __unexpected_error_message(self):
        """
              This message is intended to be called automatically in case of unexpected error.
              :return: None
              """

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowTitle("Unexpected error")
        warning_dialog.setText("Unexpected error!\nPlease restart the application.")
        warning_dialog.exec()

    def __saved_successfully_message(self):
        """
              This message is intended to be called automatically when the user's data is successfully saved.
              :return: None
              """
        confirmation_dialog = QMessageBox(self)
        confirmation_dialog.setWindowTitle("Form complete")
        confirmation_dialog.setText("The data was saved successfully!")
        confirmation_dialog.exec()


if __name__ == "__main__":
    application = QApplication(sys.argv)
    host = "127.0.0.1"
    port = 65432
    user = NewUserWindow(host, port)

    # Define a slot to close the window
    def close_window():
        user.close()

    # Connect the user_saved signal to the slot function
    user.user_saved.connect(close_window)

    user.show()
    application.exec()
