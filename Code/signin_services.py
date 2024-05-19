import datetime
import os
import socket
import json

file_name = None    
terminal = False
history = False


def create_history_file():
    global file_name

    timestamp = datetime.datetime.now()
    file_timestamp = timestamp.strftime('%Y%m%d_%H%M%S')
    file_name = 'History_' + file_timestamp + '.txt'
    interaction_timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S\n')
    file_timestamp = timestamp.strftime('%Y%m%d_%H%M%S')

    # Get current module location.
    current_folder = os.getcwd()
    #  Create "cache" folder pathname.
    cache_folder = os.path.join(current_folder, "cache")
    # Check whether cache folder has not been created yet.
    if not os.path.isdir(cache_folder):
        # Create cache folder on PC for storing all histories.
        os.mkdir(cache_folder)
    # Create absolute history filename based on full path to cache folder and history filename.
    file_name = os.path.join(cache_folder, 'History_' + file_timestamp + '.txt')

    with open(file_name, 'w') as history_file:
        history_file.write(str(interaction_timestamp).strip() + ' The program initiated.\n')


def write_history_file(message):
    global file_name

    timestamp = datetime.datetime.now()
    interaction_timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S\n')

    if file_name is None:
        print('Please create file first.')
        return False
    if not os.path.isfile(file_name):
        print('The file does not exist.')
        return False
    try:
        with open(file_name, 'a') as history_file:
            history_file.write(str(interaction_timestamp).strip() + ' ' + message)
    except OSError:
        print('Error happened while accessing history file.')
        return False
    return True


def output(message):
    if terminal is True:
        print(message)
    if history is True:
        write_history_file(message + '\n')


def validate_password(password):
    password_length = len(password)
    password_digits_only = str.isdigit(password)
    password_alphabets_only = str.isalpha(password)

    if password_length <= 7:
        output('Too short password!')
        return False
    elif password_digits_only is True:
        output('Password must contain letters!')
        return False
    elif password_alphabets_only is True:
        output('Password must contain digits!')
        return False
    elif password.islower() is True:
        output('Password must contain uppercase letters!')
        return False
    elif password.isupper() is True:
        output('Password must contain lowercase letters!')
        return False
    else:
        return True


class TCPClient:
    def __init__(self, host, port, username=None, password=None):
        self.host = host  # The server's hostname or IP address
        self.port = port  # The port used by the server
        self.__username = username
        self.__password = password

    def send_request(self):
        """
        Encode message and send to server
        :return: True if password and name matches, False otherwise
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))

            header_data = {
                "Content-Type": "application/json",
                "Encoding": "utf-8"
            }

            request_data = {
                "command": "login_request",
                "username": self.__username,
                "password": self.__password
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

            if response == "User logged in successfully":
                return True
            elif response == "User was not logged in :-(":
                return False
            else:
                print("Server response error")

    def set_port(self, number):
        """
        Assign port number to port attribute
        :param number: port number
        :return: True if port is set successfully, False otherwise
        """

        if type(number) is not int:
            return False
        self.port = number
        return True

    def set_host(self, address):
        """
        Assign IP address to host attribute
        :param address: address number
        :return: True if host is set successfully, False otherwise
        """

        if type(address) is not str:
            return False
        self.host = address
        return True
