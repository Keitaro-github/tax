import os
import csv
users = [
    {"username": "Keitaro", "password": "123456", 'user_id': 1},
    {"username": "Ivan", "password": "654321", 'user_id': 2},
    {"username": "Ben", "password": "999999", 'user_id': 3},
    {"username": "David", "password": "888888", 'user_id': 4},
    {"username": "Chris", "password": "777777", 'user_id': 5},
    {"username": "Gregor", "password": "666666", 'user_id': 6}
]


def read_csv():
    current_directory = os.getcwd()
    file_name = 'users.csv'
    csv_file = os.path.join(current_directory, file_name)
    if os.path.isfile(csv_file) is False:
        print('The csv file does not exist.')
        return None
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
            data = []
            for row in csv_reader:
                record = {}
                for key, value in enumerate(row):
                    record[headers[key]] = value
                data.append(record)
    except OSError:
        print('Error happened while accessing csv file.')
        return None
    print(data)
    return data


def write_csv(username=None, password=None, user_id=None):
    data = []
    current_directory = os.getcwd()
    file_name = 'users.csv'
    csv_file = os.path.join(current_directory, file_name)
    if os.path.isfile(csv_file) is False:
        print('The csv file does not exist.')
        return False
    try:
        data.append([username, password, user_id])
        with open(csv_file, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(data)
    except OSError:
        print('Error happened while accessing csv file.')
        return False
    return True
