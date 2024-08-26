# TMS Project

## Description
The TMS (Task Management System) Project is a client-server application designed to manage tasks efficiently. 
The project includes a server component and a client application, both of which communicate over a network.

## Installation

### Prerequisites
- Python 3.7 or higher
- Dependencies listed in `requirements.txt`

### Steps
1. Clone the repository:
   git clone https://github.com/Keitaro-github/tax
      
2. Navigate to the project directory:

3. Install the required packages:
pip install -r requirements.txt

### Usage
#### Running the Server
1. Navigate to the Code/ directory:
cd Code
2. Run the server:
- If you are using an IDE (Integrated Development Environment), run the tms_server.py file directly:
python tms_server.py 
- If you are on Windows and have the executable (tms_server.exe), you can run it by double-clicking the file or by 
- executing it from the command line:
tms_server.exe 

#### Running the Client
1. Navigate to the Code/ directory:
cd Code
2. Run the client:
- If you are using an IDE, run the tms_client.py file directly:
python tms_client.py 
- If you are on Windows and have the executable (tms_client.exe), you can run it by double-clicking the file or 
by executing it from the command line:
tms_client.exe

### Configuration
The server listens on IP 127.0.0.1 and port 65432 by default.
Client configuration can be adjusted in tcp_config.json.

