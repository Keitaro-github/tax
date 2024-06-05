from database import DatabaseServices
import socket
import json
import datetime
import sys
from Code.utils import tms_logs

db_services = DatabaseServices("taxpayers.db")


class TCPServer:
    """
    Represents a TCP server that listens for incoming connections and handles client requests.

    Attributes:
        host (str): The server's hostname or IP address.
        port (int): The port used by the server.
        new_user_window_instance (NewUserWindow): An instance of the NewUserWindow class.
        server_socket (socket.socket): The server socket used for accepting connections.
    """
    def __init__(self, host, port, new_user_window_instance):
        """
       Initializes a new instance of the Server class.

       Args:
           host (str): The server's hostname or IP address.
           port (int): The port used by the server.
           new_user_window_instance (NewUserWindow): An instance of the NewUserWindow class.
       """
        self.host = host  # The server's hostname or IP address
        self.port = port  # The port used by the server
        self.__username = None
        self.__password = None
        # Store the instance of NewUserWindow
        self.new_user_window_instance = new_user_window_instance

        # Bind the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        server_logger.log_debug(f"Server is listening on: {self. host, self. port}")

    def __del__(self):
        """
        Closes server socket when server object is deleted.
        :return: None
        """
        if hasattr(self, 'server_socket'):
            self.server_socket.close()

    @staticmethod
    def parse_header(header_data):
        """
        Parses the provided header data, which is expected to be in JSON format and returns the corresponding object.

        :param header_data: A string containing JSON-formatted data representing the header.
        :type header_data: str
        :return: A dictionary representing the parsed header data.
        :rtype: dict
        """
        return json.loads(header_data)

    @staticmethod
    def recv_until(client_socket_, delimiter):
        """
        Receives data from a client socket until a specified delimiter is encountered.

        :param client_socket_: The socket object representing the connection to the client.
        :type client_socket_: socket.socket
        :param delimiter: The delimiter indicating the end of the data.
        :type delimiter: bytes
        :return: Data received from the client up to the delimiter.
        :rtype: bytes
        """
        data = b''   # Initialize an empty byte string to store received data
        while not data.endswith(delimiter):
            chunk = client_socket_.recv(1024)   # Receive data in chunks of up to 1024 bytes
            if not chunk:
                # Handle case where client disconnects unexpectedly
                break
            data += chunk   # Append the received chunk to the data buffer
        return data

    def handle_request(self, client_socket_):
        """
        Handles different types of commands received from a client socket, sends a JSON response to the client.

        :param client_socket_: The socket object representing the connection to the client.
        :type client_socket_: socket.socket
        :return: None
        :rtype: None
        """
        user_info_list = []

        try:
            # Receive header
            message_data = self.recv_until(client_socket_, b'\r\n').decode().strip()
            server_logger.log_debug(f"Received message: {message_data}")

            # Process the request
            request_data = json.loads(message_data)
            server_logger.log_debug(f"Parsed request data: {request_data}")

            command = request_data["request"].get("command")

            if command == "login_request":
                username = request_data["request"].get("username")
                password = request_data["request"].get("password")

                if not username or not password:
                    response = "Username and password must be provided"
                    client_socket_.sendall(response.encode())
                    server_logger.log_debug(f"Sent response: 'Username and password must be provided'")
                    return

                result = db_services.check_credentials(username, password)
                if result:
                    response = "User logged in successfully"
                    client_socket_.sendall(response.encode())
                    server_logger.log_debug(f"Sent response: 'User logged in successfully'")

                else:
                    response = "Invalid username or password"
                    client_socket_.sendall(response.encode())
                    server_logger.log_debug(f"Sent response: 'Invalid username or password'")


            if command == "save_new_user":
                national_id = request_data["request"].get("national_id")
                first_name = request_data["request"].get("first_name")
                last_name = request_data["request"].get("last_name")
                date_of_birth = request_data["request"].get("date_of_birth")
                gender = request_data["request"].get("gender")
                address_country = request_data["request"].get("address_country")
                address_zip_code = request_data["request"].get("address_zip_code")
                address_city = request_data["request"].get("address_city")
                address_street = request_data["request"].get("address_street")
                address_house_number = request_data["request"].get("address_house_number")
                phone_country_code = request_data["request"].get("phone_country_code")
                phone_number = request_data["request"].get("phone_number")
                marital_status = request_data["request"].get("marital_status")

                result = db_services.save_to_sql(national_id, first_name, last_name, date_of_birth, gender,
                                                 address_country, address_zip_code, address_city, address_street,
                                                 address_house_number, phone_country_code, phone_number, marital_status)
                response = "New user saved successfully"
                client_socket_.sendall(response.encode())

            if command == "find_user":
                national_id = request_data["request"].get("national_id")
                first_name = request_data["request"].get("first_name")
                last_name = request_data["request"].get("last_name")
                date_of_birth = request_data["request"].get("date_of_birth")

                # Initialize formatted_date_of_birth to None
                formatted_date_of_birth = None

                # Reformat the date_of_birth to the SQL format (YYYY-MM-DD) if it's not None
                if date_of_birth is not None:
                    formatted_date_of_birth = datetime.datetime.strptime(date_of_birth, "%d.%m.%Y").strftime("%Y-%m-%d")

                search_results = db_services.search_personal_info(national_id, first_name, last_name,
                                                                  formatted_date_of_birth)
                if search_results is None or len(search_results) == 0:
                    response_data = {"command": "search_unsuccessful"}
                    # Convert the response data to a JSON string
                    response_message = json.dumps(response_data) + "\r\n"

                    # Send the response message to the client
                    client_socket_.sendall(response_message.encode())
                else:
                    for user in search_results:
                        limited_user_info = {
                            "national_id": user[0],
                            "first_name": user[1],
                            "last_name": user[2],
                            "date_of_birth": user[3]
                        }
                        # Append user details to the list
                        user_info_list.append(limited_user_info)
                        server_logger.log_debug(f"Result: {user_info_list}")

                    # Create the response message
                    response_data = {
                        "command": "search_successful",
                        "user_info": user_info_list
                    }

                    server_logger.log_debug(f"Response message sent to client: {response_data}")

                    # Convert the response data to a JSON string
                    response_message = json.dumps(response_data) + "\r\n"

                    # Send the response message to the client
                    client_socket_.sendall(response_message.encode())

            if command == "retrieve_user_details":
                national_id = request_data["request"].get("national_id")

                search_results = db_services.retrieve_user_details(national_id)
                if search_results is None:
                    response_data = {"command": "retrieving_unsuccessful"}

                else:
                    complete_user_info_list = []
                    for user_info in search_results:
                        complete_user_info = {
                            "national_id": user_info[0],
                            "first_name": user_info[1],
                            "last_name": user_info[2],
                            "date_of_birth": user_info[3],
                            "gender": user_info[4],
                            "address_country": user_info[6],
                            "address_zip_code": user_info[7],
                            "address_city": user_info[8],
                            "address_street": user_info[9],
                            "address_house_number": user_info[10],
                            "phone_country_code": user_info[11],
                            "phone_number": user_info[12],
                            "marital_status": user_info[14],
                            "tax_rate": user_info[15],
                            "yearly_income": user_info[16],
                            "advance_tax": user_info[17],
                            "tax_paid_this_year": user_info[18],
                            "property_value": user_info[19],
                            "loans": user_info[20],
                            "property_tax": user_info[21],
                        }
                        complete_user_info_list.append(complete_user_info)
                        server_logger.log_debug(f"Complete_user_info_list: {complete_user_info_list}")

                    response_data = {
                        "command": "retrieving_successful",
                        "user_info": complete_user_info_list
                    }

                server_logger.log_debug(f"Response message sent to client: {response_data}")

                # Convert the response data to a JSON string
                response_message = json.dumps(response_data) + "\r\n"

                # Send the response message to the client
                client_socket_.sendall(response_message.encode())

        except Exception as exception:
            server_logger.log_error(f"Unexpected exception: {exception}")
        finally:
            client_socket_.close()


if __name__ == '__main__':
    # Create a TMSLogger instance for the server
    server_logger = tms_logs.TMSLogger("server")
    if not server_logger.setup():
        sys.exit(1)
        
    # Initialize the server instance
    server = TCPServer("127.0.0.1", 65432, new_user_window_instance=None)

    while True:
        client_socket, client_address = server.server_socket.accept()
        server_logger.log_debug(f"Connected client: {client_address}")
        server.handle_request(client_socket)
    sys.exit(0)
