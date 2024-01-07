import sys

import tax.Code.database_services as database_services
import socket


class SignInServices:
    def __init__(self, host, port):
        self.host = host  # The server's hostname or IP address
        self.port = port  # The port used by the server
        self.__username = None
        self.__password = None

    def create_socket(self):
        """
        Create socket for communicating with TMS server.
        :return: None
        """

        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((self.host, self.port))
                server_socket.listen()
                conn, addr = server_socket.accept()
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        data = data.decode()
                        username, password = data.split('|')
                        result = self.__check_credentials(username, password)
                        if result is True:
                            # Create response using the same username and password divided by | symbol
                            response = data.encode()
                            conn.sendall(response)
                        else:
                            response = data.encode()[::-1]  # reverse data to indicate negative response
                            conn.sendall(response)

    def __check_credentials(self, username, password):
        """
        Check whether provided credentials are valid
        :param username: username
        :param password: password
        :return: True if credentials are valid, False otherwise
        """

        self.__username = username
        self.__password = password

        user_list = database_services.read_csv()
        for user in user_list:
            if self.__username == user['username'] and self.__password == user['password']:
                return True
        return False


if __name__ == '__main__':
    sign_in_servies = SignInServices("127.0.0.1", 65432)
    sign_in_servies.create_socket()
    sys.exit(0)