import sys, csv
from ui_tms_main_window import TMSMainWindow
from PyQt6.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout,
                             QDateEdit, QMessageBox, QComboBox, QSpinBox)
from PyQt6.QtCore import QDate


class FindUserWindow(QWidget):
    def __init__(self, tms_main_window):
        super().__init__()  # Initialize default constructor of parent class
        self.tms_main_window = tms_main_window
        # Call PyQt6 API to set current window's title.
        self.setWindowTitle("Find user")
        # Call PyQt6 API to create a layout where all UI components are placed.
        self.setMinimumWidth(500)
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
        # Connect the activated signal to the method that retrieves user information
        self.__search_results_edit.activated.connect(self.__get_selected_user_info)
        user_list = []
        self.__search_results_edit.addItems(user_list)

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


    def __handle_widget_edit(self):
        # Slot method to handle the editingFinished signal for various widgets
        sender = self.sender()
        if isinstance(sender, (QComboBox, QDateEdit, QSpinBox)):
            # Change the text color to black once the widget is edited
            self.__set_widget_color(sender, "black")

    def __set_widget_color(self, widget, color):
        widget.setStyleSheet(f"{widget.metaObject().className()} {{ color: {color}; }}")

    def __are_required_fields_filled(self, national_id, first_name, last_name, date_of_birth):
        """
        Check if any fields are filled.
        """
        current_date = QDate.currentDate()
        date_of_birth_qdate = QDate.fromString(date_of_birth, 'dd.MM.yyyy')

        return any([national_id, first_name, last_name]) or date_of_birth_qdate != current_date

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
        # Clear the previous search results from the combo box
        self.__search_results_edit.clear()

        # Collect data from all widgets
        national_id = self.__national_id_edit.text()
        first_name = self.__first_name_edit.text()
        last_name_input = self.__last_name_edit.text()
        date_of_birth = self.__date_of_birth_edit.date().toString("dd.MM.yyyy")

        if not self.__are_required_fields_filled(national_id, first_name, last_name_input, date_of_birth):
            self.__missing_data_message()
            return

        else:
            search_results = self.__search_csv(national_id, first_name, last_name_input, date_of_birth)
            self.__populate_search_results(search_results)

    def __search_csv(self, national_id, first_name, last_name, date_of_birth):
        csv_file_path = r'C:\Users\serge\PycharmProjects\pythonProject\pet_projects\tax\Code\users.csv'
        search_results = []

        with open(csv_file_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (
                        (national_id == row["national_id"]) or
                        (first_name.lower() == row["first_name"].lower()) or
                        (last_name.lower() == row["last_name"].lower()) or
                        (date_of_birth != QDate.currentDate().toString("dd.MM.yyyy") and
                         date_of_birth == row["date_of_birth"])):
                    search_results.append(row)
        return search_results

    def __populate_search_results(self, results):
        self.__search_results_edit.clear()
        self.__search_results_edit.setStyleSheet("color: black;")
        if not results:
            # self.__search_results_edit.setStyleSheet("color: black;")
            self.__search_results_edit.setPlaceholderText("No matching results")
        else:
            # self.__search_results_edit.setStyleSheet("color: black;")
            for result in results:
                display_text = f"{result['national_id']} {result['first_name']} {result['last_name']} \
                                 {result['date_of_birth']}"
                self.__search_results_edit.addItem(display_text)

    def __handle_search_result_selected(self, index):
        if index >= 0:
            # Get the selected item text
            selected_text = self.__search_results_edit.itemText(index)

            # Update tms_main_window with user information
            self.__update_tms_main_window(selected_text)

    def __get_selected_user_info(self):
        """
        Retrieve and display information of the selected user.
        """
        # Get the selected text from the combo box
        selected_text = self.__search_results_edit.currentText()

        # Update the main window with the retrieved user information
        user_info = self.__retrieve_user_information(selected_text)
        self.__update_main_window(user_info)

    def __retrieve_user_information(self, data_input):
        """
        Retrieve user information from the CSV file based on national_id.
        Implement the logic to read the CSV file and extract user information.
        """
        # Add your logic to read the CSV file and retrieve user information based on national_id
        csv_file_path = r'C:\Users\serge\PycharmProjects\pythonProject\pet_projects\tax\Code\users.csv'

        with open(csv_file_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                entered_national_id = data_input.split()[0].strip()
                stored_national_id = row["national_id"]
                if entered_national_id == stored_national_id:
                    print(row)
                    return row
        return None

    def __update_main_window(self, user_info):
        """
        Update the main window with the retrieved user information.
        """
        # Use the national ID to retrieve user information
        self.tms_main_window.populate_user_information(user_info)
        self.close()

    def __missing_data_message(self):
        """
              This message is intended to be called automatically when the user tries to save data with missing entries.
              :return: None
              """

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowTitle("Form incomplete")
        warning_dialog.setText("Missing input!\nPlease fill any field or fields.")
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


if __name__ == "__main__":
    application = QApplication(sys.argv)
    main_window = TMSMainWindow()
    user = FindUserWindow(main_window)
    user.show()
    application.exec()
