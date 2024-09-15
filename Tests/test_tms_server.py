import unittest
import sys
import os
from Code.tms_server import resource_path, get_config_path


class TestResourcePath(unittest.TestCase):

    def test_development_environment(self):
        # Ensure _MEIPASS is not set
        if hasattr(sys, '_MEIPASS'):
            del sys._MEIPASS

        # Define the relative path to test
        relative_path = 'Code/configs/tcp_config.json'
        # Expected path
        expected_path = os.path.join(os.path.abspath('.'), relative_path)

        # Call the function
        result_path = resource_path(relative_path)

        # Assert the expected path
        self.assertEqual(result_path, expected_path, "The resource path is not correct for the development "
                                                     "environment")

    def test_pyinstaller_environment(self):
        # Mock _MEIPASS for the test
        sys._MEIPASS = '/mock/path/to/_MEIPASS'

        # Define the relative path to test
        relative_path = 'Code/configs/tcp_config.json'
        # Expected path
        expected_path = os.path.join(sys._MEIPASS, relative_path)

        # Call the function
        result_path = resource_path(relative_path)

        # Assert the expected path
        self.assertEqual(result_path, expected_path, "The resource path is not correct for the PyInstaller "
                                                     "environment")
        # Clean up
        del sys._MEIPASS


class TestGetConfigPath(unittest.TestCase):

    def test_get_config_path(self):
        # Create the expected path to the config file
        current_dir = os.path.abspath(".")
        expected_path = os.path.join(current_dir, 'configs', 'tcp_config.json')

        # Test the function to ensure it returns the correct path
        actual_path = get_config_path('tcp_config.json')

        # Check if the paths match
        self.assertEqual(actual_path, expected_path, "The config file path is not correct")

    def test_get_config_path_none(self):
        with self.assertRaises(TypeError):
            get_config_path(None)

    def test_get_config_path_invalid_type(self):
        with self.assertRaises(TypeError):
            get_config_path(12345)  # Invalid type


class TestEnvironmentVariables(unittest.TestCase):

    def test_app_mode_client(self):
        os.environ['APP_MODE'] = 'CLIENT'
        self.assertEqual(os.getenv('APP_MODE'), 'CLIENT', "APP_MODE should be 'CLIENT'")

    def test_app_mode_server(self):
        os.environ['APP_MODE'] = 'SERVER'
        self.assertEqual(os.getenv('APP_MODE'), 'SERVER', "APP_MODE should be 'SERVER'")

    def test_missing_app_mode(self):
        if 'APP_MODE' in os.environ:
            del os.environ['APP_MODE']
        self.assertIsNone(os.getenv('APP_MODE'), "APP_MODE should be None")

    def tearDown(self):
        # Clean up environment variables
        if 'APP_MODE' in os.environ:
            del os.environ['APP_MODE']


if __name__ == '__main__':
    unittest.main()
