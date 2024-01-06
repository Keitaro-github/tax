import sys
from PyQt6.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel, QCheckBox, QVBoxLayout, QHBoxLayout,
                             QMessageBox)
import tax.Code.signin_services as signin_services
from PyQt6.QtCore import QTimer


class SignInWindow(QWidget):
    def __init__(self):
        super().__init__()  # Initialize default constructor of parent class

        # Call PyQt6 API to set current window's title.
        self.setWindowTitle("Sign In")
        # Call PyQt6 API to create a layout where all UI components are placed.
        self.__main_layout = QVBoxLayout()
        # Create all UI components on layout.
        self.__init_ui()
        # Call PyQt6 API to set prepared layout with all UI components.
        self.setLayout(self.__main_layout)
        # Sign in attempts limit and count.
        self.__attempt_limit = 3
        self.__attempt_count = 0

    def __init_ui(self):
        """
        This function is intended to create all UI components.
        :return: None
        :rtype:
        """

        # Create and set up the label.
        self.__label = QLabel()
        self.__label.setText("Wellcome to Tax Management System")
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
        self.__signin_button = QPushButton()
        self.__signin_button.setText("Sign In")
        self.__signin_button.clicked.connect(self.__click_signin_button)
        self.__signin_button.setToolTip("Press to sign in to Tax Management System")

        # Create and set up button widget for cancel procedure.
        self.__cancel_button = QPushButton()
        self.__cancel_button.setText("Cancel")
        self.__cancel_button.clicked.connect(self.__click_cancel_button)
        self.__cancel_button.setToolTip("Press Cancel to close the window")

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.__signin_button)
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

    def __session_timeout(self):
        self.__sign_in_time_out_message()
        self.__timer.stop()
        print("Time out!")

    def __click_hide_checkbox(self):
        """
        This function is intended to be called automatically when the user clicks on Hide password checkbox.
        :return: None
        :rtype:
        """

        if self.__hide_checkbox.isChecked() is True:
            self.__password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.__password_edit.setEchoMode(QLineEdit.EchoMode.Normal)

    def __click_signin_button(self):
        """
        This function is intended to be called automatically when the user clicks on Sign In button.
        :return: None
        :rtype:
        """
        self.__timer.start(180000)

        # Attempts limit check
        if self.__attempt_count >= self.__attempt_limit:
            self.__sign_in_attempts_limit_message()
            return

        username = self.__username_edit.text()
        password = self.__password_edit.text()

        print(f"Entered username: {username}")
        print(f"Entered password: {password}")

        self.__button_clicked = True

        if signin_services.credential_check(username, password):
            self.__sign_in_success_message()

        elif not username and not password:
            if self.__button_clicked:
                self.__attempt_count += 1
                self.__sign_in_credentials_missing_message()

        else:
            self.__attempt_count += 1
            self.__sign_in_failure_message()

            # Reset the username and password fields
            self.__username_edit.clear()
            self.__password_edit.clear()

    def __click_cancel_button(self):
        """
        This function is intended to be called automatically when the user clicks on Cancel button.
        :return: None
        """

        self.close()

    def __sign_in_success_message(self):
        """
              This message is intended to be called automatically when the user successfully signs in.
              :return: None
              """
        confirmation_dialog = QMessageBox(self)
        confirmation_dialog.setWindowTitle("Sign in successful")
        confirmation_dialog.setText("You have successfully signed in!")
        confirmation_dialog.exec()

    def __sign_in_failure_message(self):
        """
              This message is intended to be called automatically when the user unsuccessfully tries to sign in.
              :return: None
              """

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowTitle("Incorrect credentials")
        warning_dialog.setText("Entered username and/or password did not match!\nPlease re-enter your credentials.")
        warning_dialog.exec()

    def __sign_in_credentials_missing_message(self):
        """
              This message is intended to be called automatically when the user tries to sign in without entering
              credentials.
              :return: None
              """

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        warning_dialog.setWindowTitle("Missing credentials")
        warning_dialog.setText("No credentials were entered!\nPlease enter your credentials.")
        warning_dialog.exec()

    def __sign_in_attempts_limit_message(self):
        """
              This message is intended to be called automatically when the user reaches sign in attempts limit.
              :return: None
              """

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Critical)
        warning_dialog.setWindowTitle("Attempts limit reached!")
        warning_dialog.setText("Too many unsuccessful attempts to sign in!\nAccount is locked.")
        self.__signin_button.setDisabled(True)
        self.__cancel_button.setDisabled(True)
        self.__password_edit.setDisabled(True)
        self.__username_edit.setDisabled(True)
        self.__hide_checkbox.setDisabled(True)
        warning_dialog.exec()

    def __sign_in_time_out_message(self):
        """
              This message is intended to be called automatically when the time for sing in runs out.
              :return: None
              """

        warning_dialog = QMessageBox(self)
        warning_dialog.setIcon(QMessageBox.Icon.Critical)
        warning_dialog.setWindowTitle("Sign in time out!")
        warning_dialog.setText("Sign in session expired!\nPlease restart application.")
        self.__signin_button.setDisabled(True)
        self.__cancel_button.setDisabled(True)
        self.__password_edit.setDisabled(True)
        self.__username_edit.setDisabled(True)
        self.__hide_checkbox.setDisabled(True)
        warning_dialog.exec()


if __name__ == "__main__":
    application = QApplication(sys.argv)
    signin_window = SignInWindow()
    signin_window.show()
    application.exec()
