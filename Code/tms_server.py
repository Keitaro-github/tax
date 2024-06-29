from Code.tcp_ip.tcp_driver import TCPServer
from Code.utils import tms_logs
import sys
import threading

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
        multiple_client_connection_thread = threading.Thread(target=server.handle_request, args=(client_socket,))
        multiple_client_connection_thread.start()
    sys.exit(0)