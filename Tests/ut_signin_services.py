import unittest
import os
import shutil
import glob
from unittest.mock import patch
from Code import signin_services


class TestSigninServices (unittest.TestCase):

    def setUp(self):
        self.cache_folder = os.path.join(os.getcwd(), "cache")

    def test01_create_directory(self):
        """ The test case is designed to check generation of cache folder. """
        if os.path.exists(self.cache_folder):
            shutil.rmtree(self.cache_folder)

        signin_services.create_history_file()

        self.assertTrue(os.path.exists(self.cache_folder), "Cache folder not created")

    def test02_create_history_file(self):
        """ The test case is designed to check generation of history file. """

        signin_services.create_history_file()
        history_file_path = os.path.join(self.cache_folder, "History_*.txt")
        self.assertTrue(len(glob.glob(history_file_path)) > 0, "History file not created")

    def test03_content_writing(self):
        """ The test case is designed to check writing of log to history file. """

        history_file_path = os.path.join(self.cache_folder, "History_*.txt")
        files = glob.glob(history_file_path)
        self.assertTrue(len(glob.glob(history_file_path)) > 0, "History file not created")
        history_file_content = None
        with open(files[0], "r") as history_file:
            history_file_content = history_file.read()
        self.assertTrue("The program initiated." in history_file_content, "Incorrect content")

    @patch("database_services.read_csv")
    def test04_generate_id_for_empty_user_list(self, mock_read_csv):
        """ The test case is designed to generate ID for empty user list. """

        mock_read_csv.return_value = []
        result = signin_services.generate_id()
        self.assertEqual(result,1)

    @patch("database_services.read_csv")
    def test05_generate_id_for_consecutive_user_list(self, mock_read_csv):
        """ The test case is designed to generate ID for consecutive user list with empty slots. """

        mock_read_csv.return_value = [
            {'username': 'Keitaro', 'password': '123456', 'user_id': '1'},
            {'username': 'Ivan', 'password': '87654321aS', 'user_id': '2'},
            {'username': 'Ben', 'password': '999999', 'user_id': '3'},
            {'username': 'David', 'password': '888888', 'user_id': '4'},
            {'username': 'Chris', 'password': '777777', 'user_id': '5'},
            {'username': 'Gregor', 'password': '666666', 'user_id': '6'},
            {'username': 'Michael', 'password': 'qazwsxEDC1', 'user_id': '7'},
            {'username': 'Andrej', 'password': '54652', 'user_id': '8'},
            {'username': 'Boris', 'password': '45654521a', 'user_id': '13'},
            {'username': 'Nikolai', 'password': 'cdskj1221J', 'user_id': '122'}]

        result = signin_services.generate_id()
        self.assertEqual(result,9)

    @patch("database_services.read_csv")
    def test06_generate_id_for_consecutive_user_list(self, mock_read_csv):
        """ The test case is designed to generate ID for consecutive user list w/out empty slots. """

        mock_read_csv.return_value = [
            {'username': 'Keitaro', 'password': '123456', 'user_id': '1'},
            {'username': 'Ivan', 'password': '87654321aS', 'user_id': '2'},
            {'username': 'Ben', 'password': '999999', 'user_id': '3'},
            {'username': 'David', 'password': '888888', 'user_id': '4'},
            {'username': 'Chris', 'password': '777777', 'user_id': '5'},
            {'username': 'Gregor', 'password': '666666', 'user_id': '6'},
            {'username': 'Michael', 'password': 'qazwsxEDC1', 'user_id': '7'},
            {'username': 'Andrej', 'password': '54652', 'user_id': '8'},
            {'username': 'Boris', 'password': '45654521a', 'user_id': '9'},
            {'username': 'Nikolai', 'password': 'cdskj1221J', 'user_id': '10'}]

        result = signin_services.generate_id()
        self.assertEqual(result,11)


    @patch("database_services.read_csv")
    def test07_generate_id_for_non_consecutive_user_list(self, mock_read_csv):
        """ The test case is designed to generate ID for nonconsecutive user list with ID 1 missing. """

        mock_read_csv.return_value = [
            {'username': 'Keitaro', 'password': '123456', 'user_id': '4'},
            {'username': 'Ivan', 'password': '87654321aS', 'user_id': '3'},
            {'username': 'Ben', 'password': '999999', 'user_id': '12'},
            {'username': 'David', 'password': '888888', 'user_id': '8'},
            {'username': 'Chris', 'password': '777777', 'user_id': '5'},
            {'username': 'Gregor', 'password': '666666', 'user_id': '7'},
            {'username': 'Michael', 'password': 'qazwsxEDC1', 'user_id': '9'},
            {'username': 'Andrej', 'password': '54652', 'user_id': '10'},
            {'username': 'Boris', 'password': '45654521a', 'user_id': '15'},
            {'username': 'Nikolai', 'password': 'cdskj1221J', 'user_id': '6'}]

        result = signin_services.generate_id()
        self.assertEqual(result,1)

    @patch("database_services.read_csv")
    def test08_generate_id_for_non_consecutive_user_lis(self, mock_read_csv):
        """ The test case is designed to generate ID for nonconsecutive user list with first 4 ID available. """

        mock_read_csv.return_value = [
            {'username': 'Keitaro', 'password': '123456', 'user_id': '14'},
            {'username': 'Ivan', 'password': '87654321aS', 'user_id': '2'},
            {'username': 'Ben', 'password': '999999', 'user_id': '12'},
            {'username': 'David', 'password': '888888', 'user_id': '3'},
            {'username': 'Chris', 'password': '777777', 'user_id': '15'},
            {'username': 'Gregor', 'password': '666666', 'user_id': '7'},
            {'username': 'Michael', 'password': 'qazwsxEDC1', 'user_id': '1'},
            {'username': 'Andrej', 'password': '54652', 'user_id': '10'},
            {'username': 'Boris', 'password': '45654521a', 'user_id': '4'},
            {'username': 'Nikolai', 'password': 'cdskj1221J', 'user_id': '16'}
        ]
        result = signin_services.generate_id()
        self.assertEqual(result, 5)

    @patch("database_services.read_csv")
    def test09_delete_user_from_empty_user_list(self, mock_read_csv):
        """ The test case is designed to check deletion of user ID No2 from empty user list. """

        mock_read_csv.return_value = []
        result = signin_services.delete_user(2)
        self.assertIsNone(result)

    @patch("database_services.read_csv")
    def test10_delete_user_from_empty_user_list(self, mock_read_csv):
        """ The test case is designed to check deletion of user ID No2 from user list, where user No2 is not listed. """

        mock_read_csv.return_value = [
            {'username': 'Keitaro', 'password': '123456', 'user_id': '14'},
            {'username': 'Ivan', 'password': '87654321aS', 'user_id': '2'},
            {'username': 'Ben', 'password': '999999', 'user_id': '12'},
            {'username': 'David', 'password': '888888', 'user_id': '28'},
            {'username': 'Chris', 'password': '777777', 'user_id': '15'},
            {'username': 'Gregor', 'password': '666666', 'user_id': '7'},
            {'username': 'Michael', 'password': 'qazwsxEDC1', 'user_id': '1'},
            {'username': 'Andrej', 'password': '54652', 'user_id': '10'},
            {'username': 'Boris', 'password': '45654521a', 'user_id': '35'},
            {'username': 'Nikolai', 'password': 'cdskj1221J', 'user_id': '16'}]

        result = signin_services.delete_user(5)
        self.assertIsNone(result)

    @patch("database_services.read_csv")
    def test11_delete_user_from_empty_user_list(self, mock_read_csv):
        """ The test case is designed to check deletion of user ID No2 from user list, where user No2 is listed. """

        mock_read_csv.return_value = [
            {'username': 'Keitaro', 'password': '123456', 'user_id': '14'},
            {'username': 'Ivan', 'password': '87654321aS', 'user_id': '2'},
            {'username': 'Ben', 'password': '999999', 'user_id': '12'},
            {'username': 'David', 'password': '888888', 'user_id': '28'},
            {'username': 'Chris', 'password': '777777', 'user_id': '15'},
            {'username': 'Gregor', 'password': '666666', 'user_id': '7'},
            {'username': 'Michael', 'password': 'qazwsxEDC1', 'user_id': '1'},
            {'username': 'Andrej', 'password': '54652', 'user_id': '10'},
            {'username': 'Boris', 'password': '45654521a', 'user_id': '35'},
            {'username': 'Nikolai', 'password': 'cdskj1221J', 'user_id': '16'}]

        result = signin_services.delete_user(2)
        self.assertEqual(result, [
            {'username': 'Keitaro', 'password': '123456', 'user_id': '14'},
            {'username': 'Ben', 'password': '999999', 'user_id': '12'},
            {'username': 'David', 'password': '888888', 'user_id': '28'},
            {'username': 'Chris', 'password': '777777', 'user_id': '15'},
            {'username': 'Gregor', 'password': '666666', 'user_id': '7'},
            {'username': 'Michael', 'password': 'qazwsxEDC1', 'user_id': '1'},
            {'username': 'Andrej', 'password': '54652', 'user_id': '10'},
            {'username': 'Boris', 'password': '45654521a', 'user_id': '35'},
            {'username': 'Nikolai', 'password': 'cdskj1221J', 'user_id': '16'}])

    @patch("database_services.read_csv")
    def test12_find_user_in_empty_list(self, mock_read_csv):
        """ The test case is designed to find a user in empty list. """

        mock_read_csv.return_value = []
        result = signin_services.find_user("Sebastian")
        self.assertIsNone(result)

    @patch("database_services.read_csv")
    def test13_find_user_non_listed(self, mock_read_csv):
        """ The test case is designed to find non-listed user. """

        mock_read_csv.return_value = [{'username': "Johan"}, {'username': "Ulrik"}, {'username': "Sven"}]
        result = signin_services.find_user("Sebastian")
        self.assertIsNone(result)

    @patch("database_services.read_csv")
    def test14_find_user_listed(self, mock_read_csv):
        """ The test case is designed to find listed user. """

        mock_read_csv.return_value = [{'username': "Johan"}, {'username': "Ulrik"}, {'username': "Sebastian"}]
        result = signin_services.find_user("Sebastian")
        self.assertEqual(result, "Sebastian")

    def test15_validate_too_short_password(self):
        """ The test case is designed to check if too short password is valid. """

        result = signin_services.validate_password("passy")
        self.assertFalse(result)

    def test16_validate_digits_only_password(self):
        """ The test case is designed to check whether password with digits only is valid. """

        result = signin_services.validate_password("4564654654165")
        self.assertFalse(result)

    def test17_validate_lowercase_letters_only_password(self):
        """ The test case is designed to check whether password with lowercase letters only is valid. """

        result = signin_services.validate_password("shgesherh")
        self.assertFalse(result)

    def test18_validate_uppercase_letters_only_password(self):
        """ The test case is designed to check whether password with uppercase letters only is valid. """

        result = signin_services.validate_password("HGKJHGKJ")
        self.assertFalse(result)

    def test19_validate_qualified_password(self):
        """ The test case is designed to check whether password meets all requirements. """

        result = signin_services.validate_password("djkfhsdkj1JA")
        self.assertTrue(result)

    def test20_generate_password(self):
        """ The test case is designed to check whether password which meets all requirements can be generated. """

        generated_password = signin_services.generate_password()
        self.assertTrue(signin_services.validate_password(generated_password), "Generated password is not valid.")


if __name__ == "__main__":
    unittest.main()
