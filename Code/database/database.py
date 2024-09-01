import os
import sys
import sqlite3
import bcrypt
from Code.utils import tms_logs


class DatabaseServices:
    def __init__(self, db_file=None, tms_logger=None):
        self.db_file = db_file
        self.app_mode = os.getenv('APP_MODE', 'server').lower()

        if tms_logger is None:
            logger_type = "server" if self.app_mode == "server" else "client"
            self.tms_logger = tms_logs.TMSLogger(logger_type)
            if not self.tms_logger.setup():
                raise RuntimeError(f"Failed to setup {logger_type} Logger.")
        else:
            self.tms_logger = tms_logger

        if self.app_mode == 'server':
            self.tms_logger.log_debug("Initializing in server mode")
            if self.db_file:
                self.tms_logger.log_debug(f"DB file provided: {self.db_file}")
                self.conn, self.cursor = self.connect_to_database()
            else:
                raise ValueError("Database file must be specified for server mode.")
        else:
            self.tms_logger.log_debug("Initializing in client mode")
            self.conn = self.cursor = None

    def get_database_path(self):
        if self.app_mode == 'server':
            if os.path.isabs(self.db_file):
                db_path = self.db_file
            else:
                if getattr(sys, 'frozen', False):
                    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
                else:
                    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

                # Ensure the 'database' directory is directly appended
                db_path = os.path.join(base_path, 'database', os.path.basename(self.db_file))

            self.tms_logger.log_debug(f"Base path: {base_path if not os.path.isabs(self.db_file) else ''}")
            self.tms_logger.log_debug(f"Constructed DB path: {db_path}")

            if not os.path.exists(db_path):
                self.tms_logger.log_debug(f"File does not exist at: {db_path}")
            elif not os.access(db_path, os.R_OK):
                self.tms_logger.log_debug(f"File is not readable at: {db_path}")

            if os.name == 'nt':
                db_path = db_path.replace('/', '\\')

            return db_path
        else:
            return None

    def connect_to_database(self):
        if self.app_mode == 'server':
            db_path = self.get_database_path()
            self.tms_logger.log_debug(f"Connecting to database at: {db_path}")
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                return conn, cursor
            except sqlite3.Error as error:
                self.tms_logger.log_critical(f"Failed to connect to the database: {error}")
                raise
        else:
            return None, None

    def execute_query(self, query, params=None):
        """
        Executes a SQL query on the database.

        :param query: The SQL query to execute.
        :type query: str
        :param params: Parameters for the query.
        :type params: tuple, optional
        :rtype: list
        """
        conn, cursor = self.connect_to_database()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            # Commit changes regardless of type of query
            conn.commit()
            return result
        except Exception as exception:
            self.tms_logger.log_critical(f"Error executing query: {exception}")
            # Rollback changes in case of an error
            conn.rollback()
            return []
        finally:
            conn.close()

    def check_credentials(self, username, password):
        """
        Checks whether the provided combination of username and password is valid.

        :param username: The username for authentication.
        :type username: str
        :param password: The password for authentication.
        :type password: str
        :return: True if the provided credentials are valid, False otherwise.
        :rtype: bool
        """
        # Retrieve the hashed password from the database for the given username
        query = "SELECT password FROM tms_users WHERE username = ?"
        result = self.execute_query(query, (username,))

        if result and len(result) > 0:
            # Retrieve the stored hashed password
            stored_hashed_password = result[0][0]

            # Check if the entered password matches the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                # Passwords match
                return True
            else:
                # Passwords don't match
                return False
        else:
            # No user found with the given username
            return False

    def search_personal_info(self, national_id, first_name, last_name, date_of_birth):
        """
        Searches for user in the database based on different input parameters.

        :param national_id: The national ID of user.
        :type national_id: int
        :param first_name: The first name of user.
        :type first_name: str
        :param last_name: The last name  of user.
        :type last_name: str
        :param date_of_birth: The date of birth of user.
        :type date_of_birth: date
        :return: A list of tuples containing user data retrieved from the database.
        :rtype: list of tuples
        """
        # Search for user match in personal_info table
        query = ("SELECT * FROM personal_info WHERE national_id = ? OR first_name = ? OR last_name = ? "
                 "OR date_of_birth = ?")
        return self.execute_query(query, (national_id, first_name, last_name, date_of_birth))

    def retrieve_user_details(self, national_id):
        """
        Receives user details from three different tables in the database.

        :param national_id: The national ID of user.
        :type national_id: int
        :return: A list of tuples containing user data retrieved from the database.
        :rtype: list of tuples
        """
        query = """
            SELECT * 
            FROM personal_info 
            JOIN contact_info ON personal_info.national_id = contact_info.national_id 
            JOIN tax_info ON personal_info.national_id = tax_info.national_id 
            WHERE personal_info.national_id = ?
            """
        return self.execute_query(query, (national_id,))

    def search_user(self, national_id=None, first_name=None, last_name=None, date_of_birth=None):
        """
        Searches for user in the database based on one or combination of parameters.

        :param national_id: The national ID of the user.
        :type national_id: int
        :param first_name: The first name of the user.
        :type first_name: str
        :param last_name: The last name of the user.
        :type last_name: str
        :param date_of_birth: The date of birth of the user.
        :type date_of_birth: str
        :return: A list of tuples containing user data retrieved from the database.
        :rtype: list of tuples
        """
        query = "SELECT * FROM personal_info WHERE 1=1"
        params = []

        if national_id:
            query += " AND national_id = ?"
            params.append(national_id)
        if first_name:
            query += " AND first_name = ?"
            params.append(first_name)
        if last_name:
            query += " AND last_name = ?"
            params.append(last_name)
        if date_of_birth:
            query += " AND date_of_birth = ?"
            params.append(date_of_birth)
        return self.execute_query(query, params)

    def save_to_sql(self, national_id, first_name, last_name, date_of_birth, gender, address_country, address_zip_code,
                    address_city, address_street, address_house_number, phone_country_code, phone_number,
                    marital_status, tax_rate=None, yearly_income=None, advance_tax=None, tax_paid_this_year=None,
                    property_value=None, loans=None, property_tax=None):
        """
        Saves user information sent by client to the server into the database.

        :param national_id: The national ID of the user.
        :type national_id: int
        :param first_name: The first name of the user.
        :type first_name: str
        :param last_name: The last name of the user.
        :type last_name: str
        :param date_of_birth: The date of birth of the user in 'YYYY-MM-DD' format.
        :type date_of_birth: str
        :param gender: The gender of the user ('Male' or 'Female').
        :type gender: str
        :param address_country: The country of the user's address.
        :type address_country: str
        :param address_zip_code: The zip code of the user's address.
        :type address_zip_code: str
        :param address_city: The city of the user's address.
        :type address_city: str
        :param address_street: The street of the user's address.
        :type address_street: str
        :param address_house_number: The house number of the user's address.
        :type address_house_number: int
        :param phone_country_code: The country code of the user's phone number.
        :type phone_country_code: str
        :param phone_number: The phone number of the user.
        :type phone_number: int
        :param marital_status: The marital status of the user.
        :type marital_status: str ('Single' or 'Married')
        :param tax_rate: The tax rate for the user (optional).
        :type tax_rate: int or None
        :param yearly_income: The yearly income of the user (optional).
        :type yearly_income: int or None
        :param advance_tax: The advance tax paid by the user (optional).
        :type advance_tax: int or None
        :param tax_paid_this_year: The tax paid this year by the user (optional).
        :type tax_paid_this_year: int or None
        :param property_value: The value of the property owned by the user (optional).
        :type property_value: int or None
        :param loans: The amount of loans taken by the user (optional).
        :type loans: int or None
        :param property_tax: The property tax of the user (optional).
        :type property_tax: int or None
        :return: None
        :rtype: None
        """

        # SQL INSERT statements for each table
        try:
            # Insert into personal_info table
            personal_info_query = """
                INSERT INTO personal_info (national_id, first_name, last_name, date_of_birth, gender)
                VALUES (?, ?, ?, ?, ?)
            """
            self.execute_query(personal_info_query, (national_id, first_name, last_name, date_of_birth, gender))

            # Insert into contact_info table
            contact_info_query = """
                INSERT INTO contact_info (national_id, address_country, address_zip_code, address_city, address_street,
                address_house_number, phone_country_code, phone_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.execute_query(contact_info_query, (national_id, address_country, address_zip_code, address_city,
                                                    address_street, address_house_number, phone_country_code,
                                                    phone_number))

            # Insert into tax_info table with only the provided fields
            tax_info_query = """
                INSERT INTO tax_info (national_id, marital_status)
                VALUES (?, ?)
            """
            self.execute_query(tax_info_query, (national_id, marital_status))

            self.tms_logger.log_critical("User data saved successfully.")
        except Exception as exception:
            self.tms_logger.log_critical(f"Error saving user data: {exception}")
