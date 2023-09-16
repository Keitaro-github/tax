import os
import csv


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
    return data


def write_csv(username=None, password=None, user_id=None):
    data = []
    current_directory = os.getcwd()
    file_name = 'users.csv'
    csv_file_path = os.path.join(current_directory, file_name)
    if os.path.isfile(csv_file_path) is False:
        print('The csv file does not exist.')
        return False
    try:
        data.append([username, password, user_id])
        with open(csv_file_path, 'a', newline='') as csv_file_obj:
            csv_writer = csv.writer(csv_file_obj)
            csv_writer.writerows(data)
    except OSError:
        print('Error happened while accessing csv file.')
        return False
    return True


def rewrite_csv(user_list=None):
    current_directory = os.getcwd()
    file_name = 'users.csv'
    csv_file_path = os.path.join(current_directory, file_name)
    if os.path.isfile(csv_file_path) is False:
        print('The csv file does not exist.')
        return False
    user_list_sorted = sorted(user_list, key=lambda x: int(x['user_id']))
    try:
        with open(csv_file_path, 'w', newline='') as csv_file_obj:
            fieldnames = ['username', 'password', 'user_id']
            csv_writer = csv.DictWriter(csv_file_obj, fieldnames=fieldnames)
            csv_writer.writeheader()

            for user_data in user_list_sorted:
                if all(key in user_data for key in fieldnames):
                    csv_writer.writerow(user_data)
    except OSError:
        print('Error happened while accessing csv file.')
        return False
    return True
