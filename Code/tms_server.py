import os
import sys
import database_services
import socket
import json
import csv
from PyQt6.QtCore import QDate


class Server:
    def __init__(self, host, port, new_user_window_instance):
        self.host = host  # The server's hostname or IP address
        self.port = port  # The port used by the server
        self.__username = None
        self.__password = None
        self.new_user_window_instance = new_user_window_instance  # Store the instance of NewUserWindow

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

    def recv_until(self, client_socket, delimiter):
        data = b''
        while not data.endswith(delimiter):
            chunk = client_socket.recv(1024)
            if not chunk:
                # Handle case where client disconnects unexpectedly
                break
            data += chunk
        return data

    def __search_csv(self, national_id=None, first_name=None, last_name=None, date_of_birth=None):
        csv_file_path = os.path.join(os.getcwd(), "users.csv")

        search_results = []

        with open(csv_file_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (
                        (national_id == row["national_id"]) or
                        (first_name and first_name.lower() == row["first_name"].lower()) or
                        (last_name and last_name.lower() == row["last_name"].lower()) or
                        (date_of_birth != QDate.currentDate().toString("dd.MM.yyyy") and
                         date_of_birth == row["date_of_birth"])):
                        search_results.append(row)

        print("Search from csv:", search_results)
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

                search_results = self.__search_csv(national_id, first_name, last_name, date_of_birth)
                if search_results is None:
                       response_data = {"command": "search_unsuccessful"}

                else:
                    user_info_list = []

                    for user in search_results:
                        limited_user_info = {
                            "national_id": user["national_id"],
                            "first_name": user["first_name"],
                            "last_name": user["last_name"],
                            "date_of_birth": user["date_of_birth"]
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

                search_results = self.__search_csv(national_id)
                if search_results is None:
                    # If no user found, send an unsuccessful search response
                    response_data = {"command": "retrieving_unsuccessful"}

                else:
                    complete_user_info_list = []

                    for user_info in search_results:
                        complete_user_info = {
                            "national_id": user_info["national_id"],
                            "first_name": user_info["first_name"],
                            "last_name": user_info["last_name"],
                            "date_of_birth": user_info["date_of_birth"],
                            "gender": user_info["gender"],
                            "address_country": user_info["address_country"],
                            "address_zip_code": user_info["address_zip_code"],
                            "address_city": user_info["address_city"],
                            "address_street": user_info["address_street"],
                            "address_house_number": user_info["address_house_number"],
                            "phone_country_code": user_info["phone_country"],
                            "phone_number": user_info["phone_number"],
                            "marital_status": user_info["marital_status"],
                            "tax_rate": user_info["tax_rate"],
                            "yearly_income": user_info["yearly_income"],
                            "advance_tax": user_info["advance_tax"],
                            "tax_paid_this_year": user_info["tax_paid_this_year"],
                            "property_value": user_info["property_value"],
                            "loans": user_info["loans"],
                            "property_tax": user_info["property_tax"]
                        }
                        complete_user_info_list.append(complete_user_info)

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
            print("Error processing request:", e)
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

    sign_in_services = Server(host, port, new_user_window_instance=None)

    while True:
        client_socket, client_address = sign_in_services.server_socket.accept()
        print("Connected client:", client_address)
        sign_in_services.handle_request(client_socket)
        sys.exit(0)
