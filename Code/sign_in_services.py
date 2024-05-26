import socket
import json

file_name = None    
terminal = False
history = False


def validate_password(password):
    password_length = len(password)
    password_digits_only = str.isdigit(password)
    password_alphabets_only = str.isalpha(password)

    if password_length <= 7:
        return False
    elif password_digits_only is True:
        return False
    elif password_alphabets_only is True:
        return False
    elif password.islower() is True:
        return False
    elif password.isupper() is True:
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

            response = client_socket.recv(1024).decode().strip('')
            print(f"Received response: {response!r}")

            if response == "User logged in successfully":
                return True
            elif response == "Username and password must be provided":
                return False
            elif response == "Invalid username or password":
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
