import socket
import threading


TCP_ERROR_CODES = {
    "No error": 0,
    "TCP Client is busy": 1,
    "TCP Connection error": 2,
}


class TCPClient:

    __instance = None

    def __new__(cls, tms_logger, host, port):
        if cls.__instance is None:
            cls.__instance = super(TCPClient, cls).__new__(cls)

        return cls.__instance

    def __init__(self, tms_logger, host, port):
        self.tms_logger = tms_logger
        self.host = host  # The server's hostname or IP address
        self.port = port  # The port used by the server
        self.__busy = False  # Auxiliary flag that indicates whether TCP client is busy or free.
        self.__lock = threading.Lock()

    def send_request(self, request):
        """
        Encode request into JSON format message and send it to TMS TCP server.
        :return: response received from TMS TCP server if success, None otherwise.
        """

        # Check whether TCP Client is not used by some thread.
        if self.__busy is True:
            self.tms_logger.log_critical(f"Could not establish TCP connection. Client is busy")
            return {"error": TCP_ERROR_CODES["TCP Client is busy"], "response": None}

        # Acquire and keep the lock to be sure no one thread won't be able to use concurrently the TCP driver.

        with self.__lock:
            self.__busy = True

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((self.host, self.port))
                    # Send the JSON-formatted message over the socket
                    client_socket.sendall(request)

                    response = client_socket.recv(1024).decode().strip('')

                    self.__busy = False

                    return {"error": TCP_ERROR_CODES["No error"], "response": response}

            except socket.gaierror as error:
                self.__busy = False
                self.tms_logger.log_critical(f"Error occurred during establishing TCP socket connection: {error}")
                return {"error": TCP_ERROR_CODES["TCP Connection error"], "response": None}

    def is_busy(self):
        """
        Verify whether the driver is busy or free.
        Returns: True is the driver is busy, False otherwise

        """

        return self.__busy

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


class TCPServer:
    # TODO: Implement TCP Server
    pass


# Singleton class example
# class Singleton:
#     __instance = None
#
#     def __new__(cls, value):
#         if cls.__instance is None:
#             cls.__instance = super(Singleton, cls).__new__(cls)
#
#         return cls.__instance
#
#     def __init__(self, value):
#         self.value = value
#
#
# s1 = Singleton(1)
# s2 = Singleton(2)
# s3 = Singleton(3)
# s4 = Singleton(4)
# pass
