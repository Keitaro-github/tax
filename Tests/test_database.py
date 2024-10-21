import unittest
import sqlite3
from unittest.mock import patch, MagicMock
from Code.database.database import DatabaseServices
import os
import io


class TestDatabaseServices(unittest.TestCase):

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isabs', return_value=False)
    @patch('os.access', return_value=True)
    @patch('os.path.dirname')
    @patch('os.path.join', return_value='database\\test.db')
    def test_get_database_path(self, mock_join, mock_dirname, mock_isabs, mock_exists, mock_access):
        db_services = DatabaseServices(db_file=os.path.join('database', 'test.db'), tms_logger=None)
        db_path = db_services.get_database_path()

        # Ensure the path was constructed correctly
        mock_join.assert_called_once()
        self.assertEqual(db_path, 'database\\test.db')

    @patch('os.path.abspath', return_value='test.db')  # Mock the path resolution
    @patch('Code.utils.tms_logs.TMSLogger')  # Mock the logger
    @patch('sqlite3.connect')  # Mock the sqlite3 connection
    @patch('os.getenv')  # Mock environment variables
    def test_init_server_mode_with_db(self, mock_getenv, mock_connect, mock_logger, mock_abspath):
        # Simulate server mode environment variable
        mock_getenv.return_value = 'server'

        # Mocking the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Instance creation
        db_services = DatabaseServices(db_file=os.path.join('database', 'test.db'), tms_logger=None)
        # Assertions
        mock_logger.assert_called_once_with('server')
        mock_connect.assert_called_once_with('database\\test.db')
        self.assertIsNotNone(db_services.conn)
        self.assertIsNotNone(db_services.cursor)

    @patch('Code.utils.tms_logs.TMSLogger')
    @patch('sqlite3.connect')
    @patch('os.getenv')
    def test_connect_to_database(self, mock_getenv, mock_connect, mock_logger):
        mock_getenv.return_value = 'server'

        # Mock the connection and cursor again
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Create an instance with the mocked dependencies
        db_services = DatabaseServices(db_file=os.path.join('database', 'test.db'), tms_logger=None)
        # Call the method and assert
        conn, cursor = db_services.connect_to_database()
        self.assertEqual(conn, mock_conn)
        self.assertEqual(cursor, mock_cursor)

    @patch('Code.utils.tms_logs.TMSLogger')
    @patch('sqlite3.connect')
    @patch('os.getenv')
    def test_check_credentials(self, mock_getenv, mock_connect, mock_logger):
        mock_getenv.return_value = 'server'

        # Mock connection and cursor for SQL execution
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock bcrypt check and SQL query result
        mock_cursor.fetchall.return_value = [('hashed_password',)]
        with patch('bcrypt.checkpw', return_value=True):
            db_services = DatabaseServices(db_file=os.path.join('database', 'test.db'))

            result = db_services.check_credentials('user', 'password')
            self.assertTrue(result)

    @patch('Code.utils.tms_logs.TMSLogger')
    @patch('os.getenv')
    def test_get_database_path(self, mock_getenv, mock_logger):
        mock_getenv.return_value = 'server'
        db_services = DatabaseServices(db_file=os.path.join('database', 'test.db'), tms_logger=None)
        # Mock os.path methods
        with patch('os.path.exists', return_value=True), patch('os.path.isabs', return_value=False):
            db_path = db_services.get_database_path()
            self.assertIn('test.db', db_path)

    @patch('sqlite3.connect')
    def test_execute_query_success(self, mock_connect):
        # Mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db_services = DatabaseServices(db_file=os.path.join('database', 'test.db'), tms_logger=None)

        # Simulate a query
        mock_cursor.fetchall.return_value = [('result',)]
        result = db_services.execute_query('SELECT * FROM personal_info')

        # Check the query execution and result
        mock_cursor.execute.assert_called_once_with('SELECT * FROM personal_info')
        self.assertEqual(result, [('result',)])
        mock_conn.commit.assert_called_once()

    @patch('sqlite3.connect')
    def test_execute_query_failure(self, mock_connect):
        # Mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simulate an sqlite3.Error exception
        mock_cursor.execute.side_effect = sqlite3.Error("Mocked SQL Error")

        db_services = DatabaseServices(db_file=os.path.join('database', 'test.db'), tms_logger=None)
        result = db_services.execute_query('SELECT * FROM personal_info')

        # Assert rollback was called
        mock_conn.rollback.assert_called_once()

        # Assert the result is an empty list
        self.assertEqual(result, [])

    @patch.object(DatabaseServices, 'execute_query')
    def test_search_personal_info(self, mock_execute_query):
        # Arrange: Prepare the mock data to return when execute_query is called
        mock_execute_query.return_value = [('12345', 'John', 'Doe', '1990-01-01')]

        # Act: Call the method with test parameters
        db_services = DatabaseServices(db_file='test.db', tms_logger=None)
        result = db_services.search_personal_info(national_id=12345, first_name='John', last_name='Doe',
                                                  date_of_birth='1990-01-01')

        # Assert: Check if the query and parameters are correct and if the result is as expected
        mock_execute_query.assert_called_once_with(
            "SELECT * FROM personal_info WHERE national_id = ? OR first_name = ? OR last_name = ? OR date_of_birth = ?",
            (12345, 'John', 'Doe', '1990-01-01')
        )
        self.assertEqual(result, [('12345', 'John', 'Doe', '1990-01-01')])

    @patch.object(DatabaseServices, 'execute_query')
    def test_retrieve_user_details(self, mock_execute_query):
        # Arrange: Prepare mock return data
        mock_execute_query.return_value = [
            ('12345', 'John', 'Doe', '1990-01-01', '12345', 'NY', 'NYC', '5th Avenue', '123', '+1', '5555555', 'Single')
        ]

        # Act: Call the method with a test national_id
        db_services = DatabaseServices(db_file='test.db', tms_logger=None)
        result = db_services.retrieve_user_details(national_id=12345)

        # Assert: Check that the correct query is executed
        mock_execute_query.assert_called_once_with(
            """
            SELECT * 
            FROM personal_info 
            JOIN contact_info ON personal_info.national_id = contact_info.national_id 
            JOIN tax_info ON personal_info.national_id = tax_info.national_id 
            WHERE personal_info.national_id = ?
            """,
            (12345,)
        )
        self.assertEqual(result, [
            ('12345', 'John', 'Doe', '1990-01-01', '12345', 'NY', 'NYC', '5th Avenue', '123', '+1', '5555555', 'Single')
        ])

    @patch.object(DatabaseServices, 'execute_query')
    def test_search_user(self, mock_execute_query):
        # Arrange: Prepare mock return data
        mock_execute_query.return_value = [
            ('12345', 'John', 'Doe', '1990-01-01')
        ]

        # Act: Call the method with some test parameters
        db_services = DatabaseServices(db_file='test.db', tms_logger=None)
        result = db_services.search_user(national_id=12345, first_name='John', last_name='Doe')

        # Assert: Check if the query was built correctly
        mock_execute_query.assert_called_once_with(
            "SELECT * "
            "FROM personal_info "
            "WHERE 1=1 AND national_id = ? AND first_name = ? AND last_name = ?",
            [12345, 'John', 'Doe']
        )
        self.assertEqual(result, [('12345', 'John', 'Doe', '1990-01-01')])

    @patch.object(DatabaseServices, 'execute_query')
    def test_save_to_sql(self, mock_execute_query):
        # Act: Call the method with test data
        db_services = DatabaseServices(db_file='test.db', tms_logger=None)
        db_services.save_to_sql(
            national_id=12345, first_name='John', last_name='Doe', date_of_birth='1990-01-01',
            gender='Male', address_country='US', address_zip_code='12345', address_city='NYC',
            address_street='5th Avenue', address_house_number=123, phone_country_code='+1', phone_number=5555555,
            marital_status='Single', tax_rate=15, yearly_income=60000, advance_tax=5000, tax_paid_this_year=3000,
            property_value=500000, loans=100000, property_tax=3000
        )

        def normalize_sql(sql):
            return ' '.join(sql.split())

        expected_queries = [
            (
            "INSERT INTO personal_info (national_id, first_name, last_name, date_of_birth, gender) VALUES (?, ?, ?, ?, ?)",
            (12345, 'John', 'Doe', '1990-01-01', 'Male')),
            (
            "INSERT INTO contact_info (national_id, address_country, address_zip_code, address_city, address_street, address_house_number, phone_country_code, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (12345, 'US', '12345', 'NYC', '5th Avenue', 123, '+1', 5555555)),
            ("INSERT INTO tax_info (national_id, marital_status) VALUES (?, ?)",
             (12345, 'Single'))
        ]

        # Assert
        for expected_query, expected_params in expected_queries:
            found = False
            for call_args in mock_execute_query.call_args_list:
                actual_query, actual_params = call_args[0]
                if normalize_sql(actual_query) == normalize_sql(expected_query) and actual_params == expected_params:
                    found = True
                    break
            self.assertTrue(found, f"Expected call not found: {expected_query} with params {expected_params}")


if __name__ == '__main__':
    unittest.main()
