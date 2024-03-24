import sys
import os
import database_services
import socket
import json
import csv
import sqlite3
import bcrypt
import sys
from PyQt6.QtCore import QDate


class Server:
    def __init__(self, host, port, new_user_window_instance):
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
        print("Server is listening on", (self.host, self.port))

    def __del__(self):
        """
        Close server socket when server object is deleted.
        :return: None
        """
        if hasattr(self, 'server_socket'):
            self.server_socket.close()

    def parse_header(self, header_data):
        return json.loads(header_data)

    def connect_to_database(self, db_file):
        # Get the absolute path to the directory containing the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the absolute path to the database file using the script directory
        db_path = os.path.join(script_dir, 'database', db_file)
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        return conn, cursor

    def __check_credentials(self, username, password):
        conn, cursor = self.connect_to_database("taxpayers.db")

        # Retrieve the hashed password from the database for the given username
        cursor.execute("SELECT password FROM tms_users WHERE username = ?", (username,))
        stored_hashed_password = cursor.fetchone()
        print("Stored hashed password:", stored_hashed_password)
        print("Password:", password.encode('utf-8'))

        if stored_hashed_password is not None:
            # Retrieve the stored hashed password
            stored_hashed_password = stored_hashed_password[0]

            # Check if the entered password matches the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                # Passwords match
                return True
            else:
                # Passwords don't match
                return False
        else:
            # No user found with the given username
            return False

        conn.close()

    def recv_until(self, client_socket, delimiter):
        data = b''
        while not data.endswith(delimiter):
            chunk = client_socket.recv(1024)
            if not chunk:
                # Handle case where client disconnects unexpectedly
                break
            data += chunk
        return data

    def __retrieve_user_details(self, national_id):
        conn, cursor = self.connect_to_database("taxpayers.db")
        cursor.execute("""
            SELECT * 
            FROM personal_info 
            JOIN contact_info ON personal_info.national_id = contact_info.national_id 
            JOIN tax_info ON personal_info.national_id = tax_info.national_id 
            WHERE personal_info.national_id = ?
            """, (national_id,))
        search_results = cursor.fetchall()
        print("Retrieve_user_details:", search_results)
        conn.close()
        return search_results

    def __search_personal_info(self, national_id, first_name, last_name, date_of_birth):
        conn, cursor = self.connect_to_database("taxpayers.db")

        # Search for user match in personal_info table
        cursor.execute("SELECT * FROM personal_info WHERE national_id = ? OR first_name = ? OR last_name "
                       "= ? OR date_of_birth = ?", (national_id, first_name, last_name, date_of_birth))
        search_results = cursor.fetchall()
        print("Search_results:", search_results)
        conn.close()
        return search_results

    def handle_request(self, client_socket):
        try:
            # Receive header
            message_data = self.recv_until(client_socket, b'\r\n').decode().strip()
            print("Received message:", message_data)

            # Process the request
            request_data = json.loads(message_data)
            print("Parsed request data:", request_data)  # Debugging statement

            try:
                command = request_data["request"].get("command")
            except KeyError:
                print("Could not handle request.")
                client_socket.close()
                return

            if command == "login_request":
                username = request_data["request"].get("username")
                password = request_data["request"].get("password")

                result = self.__check_credentials(username, password)
                if result is True:
                    # Create response using the same username and password divided by | symbol
                    response = "User logged in successfully"
                    client_socket.sendall(response.encode())
                    print(response)
                else:
                    response = "User was not logged in :-("
                    client_socket.sendall(response.encode())
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

                result = self.__save_to_csv(national_id, first_name, last_name,date_of_birth, gender, address_country,
                                            address_zip_code, address_city, address_street, address_house_number,
                                            phone_country_code, phone_number, marital_status)
                response = "User saved successfully"
                print('all saved?...')
                client_socket.sendall(response.encode())
                print('all sent?..')
            if command == "find_user":
                national_id = request_data["request"].get("national_id")
                first_name = request_data["request"].get("first_name")
                last_name = request_data["request"].get("last_name")
                date_of_birth = request_data["request"].get("date_of_birth")

                search_results = self.__search_personal_info(national_id, first_name, last_name, date_of_birth)
                if search_results is None or len(search_results) == 0:
                       response_data = {"command": "search_unsuccessful"}

                else:
                    user_info_list = []

                    for user in search_results:
                        limited_user_info = {
                            "national_id": user[0],
                            "first_name": user[1],
                            "last_name": user[2],
                            "date_of_birth": user[3]
                        }
                        # Append user details to the list
                        user_info_list.append(limited_user_info)
                    print("result 1", user_info_list)

                # Create the response message
                response_data = {
                    "command": "search_successful",
                    "user_info": user_info_list
                }

                # Print the message before sending it to the client
                print("Response message sent to client:", response_data)

                # Convert the response data to a JSON string
                response_message = json.dumps(response_data) + "\r\n"

                # Send the response message to the client
                client_socket.sendall(response_message.encode())

            if command == "retrieve_user_details":
                national_id = request_data["request"].get("national_id")

                search_results = self.__retrieve_user_details(national_id)
                if search_results is None:
                    # If no user found, send an unsuccessful search response
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
                        print("Complete_user_info_list", complete_user_info_list)

                    response_data = {
                        "command": "retrieving_successful",
                        "user_info": complete_user_info_list
                    }

                # Print the message before sending it to the client
                print("Response message sent to client:", response_data)

                # Convert the response data to a JSON string
                response_message = json.dumps(response_data) + "\r\n"

                # Send the response message to the client
                client_socket.sendall(response_message.encode())
                
        except Exception as e:
            print(" Error processing request:", e)
        finally:
            client_socket.close()

    def __save_to_csv(self, national_id, first_name, last_name,
                      date_of_birth, gender, address_country,
                      address_zip_code, address_city, address_street,
                      address_house_number, phone_country_code,
                      phone_number, marital_status):
        """
        Save user info
        """

        columns = ["national_id", "username", "password", "user_id", "first_name", "last_name", "date_of_birth",
                   "gender", "address_country", "address_zip_code", "address_city", "address_street",
                   "address_house_number", "phone_country_code", "phone_number", "marital_status"]

        default_values = {"username": "", "password": "", "user_id": ""}
        data_dict = {"national_id": national_id,
                     "first_name": first_name,
                     "last_name": last_name,
                     "date_of_birth": date_of_birth,
                     "gender": gender,
                     "address_country": address_country,
                     "address_zip_code": '*'+address_zip_code,
                     "address_city": address_city,
                     "address_street": address_street,
                     "address_house_number": address_house_number,
                     "phone_country_code": self.__extract_numeric_code(phone_country_code),
                     "phone_number": phone_number,
                     "marital_status": marital_status}
        data_dict.update(default_values)
        data = [data_dict[column] for column in columns]

        csv_file_path = os.path.join(os.getcwd(), "users.csv")
        if os.path.isfile(csv_file_path) is False:
            print("CSV file does not exist.")
            return False

        try:
            with open(csv_file_path, mode='a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(data)
        except OSError:
            print("Could not open CSV file.")
            return False

        return True

    def __extract_numeric_code(self, country_code):
        # Extract the numeric part from the country code
        numeric_code = country_code.split()[1]
        return numeric_code


if __name__ == '__main__':
    try:
        with open("configs/tcp_config.json", 'r') as tcp_config_file:
            tcp_configs = json.loads(tcp_config_file.read())
    except OSError:
        print("Could not get TCP configs. Please, check Code/configs/tcp_config.json file")
        sys.exit(1)

    try:
        host = tcp_configs["host"]
        port = tcp_configs["port"]
    except KeyError as exception:
        print(exception)
        sys.exit(1)

    tms_server = Server(host, port, new_user_window_instance=None)

    while True:
        client_socket, client_address = tms_server.server_socket.accept()
        print("Connected TMS client:", client_address)
        tms_server.handle_request(client_socket)
    sys.exit(0)
