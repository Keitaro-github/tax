import os
import sqlite3
import bcrypt


class DatabaseServices:
    """
    Represents a number of methods to interact with SQLite database.

    Attributes:
        db_file (str): The path to the SQLite database file.
        conn: An instance of connection to the database.
        cursor: An instance of cursor for executing SQL queries.
    """
    def __init__(self, db_file):
        """
        Initializes a DatabaseServices instance.

        :param db_file: The path to the SQLite database file.
        :type db_file: str
        """
        self.db_file = db_file
        self.conn, self.cursor = self.connect_to_database(db_file)

    @staticmethod
    def connect_to_database(db_file):
        """
        Connects to an SQL database file.

        :param db_file: The path to the SQLite database file.
        :type db_file: str
        :return: A tuple containing the connection and cursor to the database.
        :rtype: tuple (sqlite3.Connection, sqlite3.Cursor)
        """
        # Get the absolute path to the directory containing the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the absolute path to the database file using the script directory
        db_path = os.path.join(script_dir, 'database', db_file)
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        return conn, cursor

    def execute_query(self, query, params=None):
        """
        Executes a SQL query on the database.

        :param query: The SQL query to execute.
        :type query: str
        :param params: Parameters for the query.
        :type params: tuple, optional
        :rtype: None
        """
        conn, cursor = self.connect_to_database(self.db_file)
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
            print("Error executing query:", exception)
            # Rollback changes in case of an error
            conn.rollback()
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
                    marital_status):
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
        :type address_zip_code: int
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
        :return: None
        :rtype: None
        """
        # Construct the SQL INSERT statement
        queries = [
            """
            INSERT INTO personal_info (national_id, first_name, last_name, date_of_birth, gender)
            VALUES (?, ?, ?, ?, ?)
            """,
            """             
            INSERT INTO contact_info (national_id, address_country, address_zip_code, address_city, address_street, 
            address_house_number, phone_country_code, phone_number)    
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            """         
            INSERT INTO tax_info (national_id, marital_status)    
            VALUES (?, ?)
            """
        ]

        # Prepare the data for insertion
        data = [
            (national_id, first_name, last_name, date_of_birth, gender),
            (national_id, address_country, address_zip_code, address_city, address_street, address_house_number,
             phone_country_code, phone_number),
            (national_id, marital_status)
        ]
        # Execute each query separately
        for query, params in zip(queries, data):
            self.execute_query(query, params)
