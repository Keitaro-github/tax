import socket
import json
import datetime
import threading
from Code.utils import tms_logs
from Code.database.database import DatabaseServices

TCP_ERROR_CODES = {
    "No error": 0,
    "TCP Client is busy": 1,
    "TCP Connection error": 2,
}

db_services = DatabaseServices("taxpayers.db")
db_lock = threading.Lock()

class TCPClient:
    __instance = None

    def __new__(cls, tms_logger, host, port):
        if cls.__instance is None:
            cls.__instance = super(TCPClient, cls).__new__(cls)
        return cls.__instance

    def __init__(self, tms_logger, host, port):
        self.tms_logger = tms_logger
        self.host = host
        self.port = port
        self.__busy = False
        self.__lock = threading.Lock()

    def send_request(self, request):
        """
        Sends a request to the TCP server and returns the response.
        Args:
            request (bytes): The request data to be sent.
        Returns:
            dict: A dictionary containing the error code and response data.
        """
        if self.__busy:
            self.tms_logger.log_critical("Could not establish TCP connection. Client is busy")
            return {"error": TCP_ERROR_CODES["TCP Client is busy"], "response": None}

        with self.__lock:
            self.__busy = True
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((self.host, self.port))
                    client_socket.sendall(request)
                    response = client_socket.recv(1024).decode().strip()
                    self.__busy = False
                    return {"error": TCP_ERROR_CODES["No error"], "response": response}
            except socket.gaierror as error:
                self.__busy = False
                self.tms_logger.log_critical(f"Error occurred during establishing TCP socket connection: {error}")
                return {"error": TCP_ERROR_CODES["TCP Connection error"], "response": None}

    def is_busy(self):
        """
        Checks if the TCP client is currently busy.
        Returns:
            bool: True if the client is busy, False otherwise.
        """
        return self.__busy

    def set_port(self, number):
        """
        Sets the port number for the TCP client.
        Args:
            number (int): The port number to be set.
        Returns:
            bool: True if the port number is valid and set, False otherwise.
        """
        if isinstance(number, int):
            self.port = number
            return True
        return False

    def set_host(self, address):
        """
        Sets the host address for the TCP client.
        Args:
            address (str): The host address to be set.
        Returns:
            bool: True if the host address is valid and set, False otherwise.
        """
        if isinstance(address, str):
            self.host = address
            return True
        return False

class TCPServer:
    def __init__(self, host, port, new_user_window_instance):
        """
        Initializes the TCP server with the specified host and port.
        Args:
            host (str): The host address.
            port (int): The port number.
            new_user_window_instance: An instance of the new user window.
        """
        self.host = host
        self.port = port
        self.new_user_window_instance = new_user_window_instance
        self.__username = None
        self.__password = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.server_logger = tms_logs.TMSLogger("server")
        if not self.server_logger.setup():
            raise Exception("Failed to set up server logger")
        self.server_logger.log_debug(f"Server is listening on: {self.host, self.port}")

    def __del__(self):
        """
        Closes the server socket when the TCP server instance is destroyed.
        """
        if hasattr(self, 'server_socket'):
            self.server_socket.close()

    @staticmethod
    def parse_header(header_data):
        """
        Parses the header data from JSON format.
        Args:
            header_data (str): The header data in JSON format.
        Returns:
            dict: The parsed header data.
        """
        return json.loads(header_data)

    @staticmethod
    def recv_until(client_socket_, delimiter):
        """
        Receives data from the client socket until the specified delimiter is encountered.
        Args:
            client_socket_ (socket.socket): The client socket.
            delimiter (bytes): The delimiter to stop receiving data.
        Returns:
            bytes: The received data.
        """
        data = b''
        while not data.endswith(delimiter):
            chunk = client_socket_.recv(1024)
            if not chunk:
                break
            data += chunk
        return data

    def handle_request(self, client_socket_):
        """
        Handles incoming requests from the client socket.
        Args:
            client_socket_ (socket.socket): The client socket.
        """
        user_info_list = []
        try:
            message_data = self.recv_until(client_socket_, b'\r\n').decode().strip()
            self.server_logger.log_debug(f"Received message: {message_data}")
            request_data = json.loads(message_data)
            self.server_logger.log_debug(f"Parsed request data: {request_data}")
            command = request_data["request"].get("command")
            with db_lock:
                if command == "login_request":
                    username = request_data["request"].get("username")
                    password = request_data["request"].get("password")
                    if not username or not password:
                        response = "Username and password must be provided"
                        client_socket_.sendall(response.encode())
                        self.server_logger.log_debug("Sent response: 'Username and password must be provided'")
                        return
                    result = db_services.check_credentials(username, password)
                    if result:
                        response = "User logged in successfully"
                        client_socket_.sendall(response.encode())
                        self.server_logger.log_debug("Sent response: 'User logged in successfully'")
                    else:
                        response = "Invalid username or password"
                        client_socket_.sendall(response.encode())
                        self.server_logger.log_debug("Sent response: 'Invalid username or password'")
                elif command == "save_new_user":
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
                elif command == "find_user":
                    national_id = request_data["request"].get("national_id")
                    first_name = request_data["request"].get("first_name")
                    last_name = request_data["request"].get("last_name")
                    date_of_birth = request_data["request"].get("date_of_birth")
                    formatted_date_of_birth = None
                    if date_of_birth:
                        formatted_date_of_birth = datetime.datetime.strptime(date_of_birth, "%d.%m.%Y").strftime("%Y-%m-%d")
                    search_results = db_services.search_personal_info(national_id, first_name, last_name, formatted_date_of_birth)
                    if not search_results:
                        response_data = {"command": "search_unsuccessful"}
                        response_message = json.dumps(response_data) + "\r\n"
                        client_socket_.sendall(response_message.encode())
                    else:
                        for user in search_results:
                            limited_user_info = {
                                "national_id": user[0],
                                "first_name": user[1],
                                "last_name": user[2],
                                "date_of_birth": user[3]
                            }
                            user_info_list.append(limited_user_info)
                            self.server_logger.log_debug(f"Result: {user_info_list}")
                        response_data = {"command": "search_successful", "user_info": user_info_list}
                        self.server_logger.log_debug(f"Response message sent to client: {response_data}")
                        response_message = json.dumps(response_data) + "\r\n"
                        client_socket_.sendall(response_message.encode())
                elif command == "retrieve_user_details":
                    national_id = request_data["request"].get("national_id")
                    search_results = db_services.retrieve_user_details(national_id)
                    if not search_results:
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
                                "property_tax": user_info[21]
                            }
                            complete_user_info_list.append(complete_user_info)
                            self.server_logger.log_debug(f"Complete_user_info_list: {complete_user_info_list}")
                        response_data = {"command": "retrieving_successful", "user_info": complete_user_info_list}
                    self.server_logger.log_debug(f"Response message sent to client: {response_data}")
                    response_message = json.dumps(response_data) + "\r\n"
                    client_socket_.sendall(response_message.encode())
        except Exception as exception:
            self.server_logger.log_error(f"Unexpected exception: {exception}")
        finally:
            client_socket_.close()
