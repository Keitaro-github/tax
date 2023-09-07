import random
import getpass
from database_services import users
import datetime
import os
import csv
file_name = None
csv_file = None


def create_history_file():
    global file_name
    timestamp = datetime.datetime.now()
    file_timestamp = timestamp.strftime('%Y%m%d_%H%M%S')
    file_name = 'History_' + file_timestamp + '.txt'
    interaction_timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S\n')
    with open(file_name, 'w') as history_file:
        history_file.write(str(interaction_timestamp).strip() + ' The program initiated.\n')


def write_history_file(message):
    global file_name
    timestamp = datetime.datetime.now()
    interaction_timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S\n')
    folder_name = '__pycache__'
    file_path = os.path.join(folder_name, file_name)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    if file_name is None:
        print('Please create file first.')
        return False
    if os.path.isfile(file_name) is False:
        print('The file does not exists.')
        return False
    try:
        with open(file_path, 'a') as history_file:
            history_file.write(str(interaction_timestamp).strip() + ' ' + message)
    except OSError:
        print('Error happened while accessing history file.')
        return False
    return True


def generate_id():
    id_list = []
    for user in users:
        id_list.append(user['user_id'])
    if not id_list:
        return 1
    elif id_list[0] != 1:
        return 1
    else:
        for i in range(len(id_list) - 1):
            if id_list[i] == (id_list[i + 1] - 1):
                continue
            else:
                return i + 2
        else:
            list_number = len(id_list)
            return list_number + 1


def delete_user(id_num):
    for user in users:
        if user['user_id'] == id_num:
            users.remove(user)
            print(f'User with ID {id_num} has been deleted')
            write_history_file(f'User with ID {id_num} has been deleted\n')
            break
        else:
            continue
    else:
        print('The user with such ID was not found.')
        write_history_file('The user with such ID was not found.\n')


def user_info_printout(users):
    while True:
        print('Please enter user ID for printout: ')
        write_history_file('Please enter user ID for printout: \n')
        try:
            user_id_input = int(input())
        except ValueError:
            print('Invalid input. Please enter a valid user ID.')
            write_history_file('Invalid input. Please enter a valid user ID.\n')
            continue
        found = False
        for user in users:
            if user['user_id'] == user_id_input:
                print(user)
                write_history_file(user)
                found = True
                break
        if not found:
            print(f'User with ID {user_id_input} not found')
            write_history_file(f'User with ID {user_id_input} not found\n')


def find_user(user_name):
    for user in users:
        if user['username'] == user_name:
            print(user_name)
            write_history_file(user_name)
            return user
    return None


result = find_user('Tom')


def show_list():
    print('The list of users is as follows:')
    write_history_file('The list of users is as follows:\n')
    for user in users:
        print(user['username'])
        write_history_file(user['username\n'])


def validate_password(password):
    password_length = len(password)
    password_digits_only = str.isdigit(password)
    password_alphabets_only = str.isalpha(password)
    if password_length <= 7:
        print('Too short password!')
        write_history_file('Too short password!\n')
        return False
    elif password_digits_only is True:
        print('Password must contain letters!')
        write_history_file('Password must contain letters!\n')
        return False
    elif password_alphabets_only is True:
        print('Password must contain digits!')
        write_history_file('Password must contain digits!\n')
        return False
    elif password.islower() is True:
        print('Password must contain uppercase letters!')
        write_history_file('Password must contain uppercase letters!\n')
        return False
    elif password.isupper() is True:
        print('Password must contain lowercase letters!')
        write_history_file('Password must contain lowercase letters!\n')
        return False
    else:
        return True


def add_user():
    username = input('Register your username and press "Enter": ')
    write_history_file('Register your username and press "Enter": \n')
    write_history_file(username + '\n')
    while find_user(username) is not None:
        print('The username is occupied already, please register unique name')
        write_history_file('The username is occupied already, please register unique name\n')
        username = input('Register your username and press "Enter": ')
        write_history_file('Register your username and press "Enter": \n')
        write_history_file(username + '\n')
    password = input('Register your password and press "Enter": ')
    write_history_file('Register your password and press "Enter": \n')
    write_history_file('\n')
    while not validate_password(password):
        password = input('Please enter a valid password or enter 0 to exit: ')
        write_history_file('Please enter a valid password or enter 0 to exit: \n')
        write_history_file('\n')
        if password == '0':
            write_history_file('0' + '.\n')
            print('Operation aborted.')
            write_history_file('Operation aborted.\n')
            return
    id_num = generate_id()
    users.append({'username': username, 'password': password, 'ID': id_num})
    print('User added successfully!')
    write_history_file('User added successfully!\n')


def credential_check():
    username_input = input('\n' + 'Enter your username and press "Enter": ')
    write_history_file('Enter your username and press "Enter": \n')
    write_history_file(username_input + '\n')
    password_input = getpass.getpass('Enter your password and press "Enter": ')
    write_history_file('Enter your password and press "Enter": \n')
    write_history_file('\n')
    for user in users:
        if username_input == user['username'] and password_input == user['password']:
            return True
    return False


def sign_in():
    attempts = 0
    attempts_limit = 5
    for _ in range(5):
        if credential_check() is True:
            print('Login successful!')
            write_history_file('Login successful!\n')
            break
        else:
            user_input = input('Incorrect credentials, please check your input or enter 0 to exit! ')
            write_history_file(user_input + '\n')
            if user_input == '0':
                write_history_file('0' + '\n')
                print('Operation aborted.')
                write_history_file('Operation aborted.\n')
                return
            else:
                attempts = attempts + 1
    if attempts == attempts_limit:
        print('Oops, too many wrong attempts, please contact administrator!')
        write_history_file('Oops, too many wrong attempts, please contact administrator!\n')


def change_password(input_username):
    for user in users:
        if user['username'].lower() == input_username.lower():
            input_old_password = input('Hello ''' + user['username'] + ', please enter your password: ')
            write_history_file('\n')
            if user['password'] != input_old_password:
                print('Incorrect password entered. Process terminated.')
                write_history_file('Incorrect password entered. Process terminated.\n')
                return False
            elif user['password'] == input_old_password:
                input_new_password1 = input('Please enter your new password: ')
                write_history_file('Please enter your new password: \n')
                write_history_file('\n')
                while not validate_password(input_new_password1):
                    input_new_password1 = input('Please enter a valid password: ')
                    write_history_file('Please enter a valid password: \n')
                    write_history_file('\n')
                input_new_password2 = input('Please re-enter your new password: ')
                write_history_file('Please re-enter your new password: \n')
                write_history_file('\n')
                if input_new_password1 == input_new_password2:
                    user['password'] = input_new_password2
                    print('Password updated successfully!')
                    write_history_file('Password updated successfully!\n')
                    return True
                elif input_new_password1 != input_new_password2:
                    print('Password is not the same. Process terminated.')
                    write_history_file('Password is not the same. Process terminated.\n')
                    return False
    else:
        print('User with this name is not registered. Process terminated.')
        write_history_file('User with this name is not registered. Process terminated.\n')
        return False


def generate_password():
    status = False
    password = ''
    while status is False:
        # password = ""
        for number in range(8):
            selector = random.randint(0, 2)
            if selector == 0:
                password += str(random.randint(0, 9))
            elif selector == 1:
                password += chr(random.randint(65, 90))
            else:
                password += chr(random.randint(97, 122))
        status = validate_password(password)
    print('Password generated successfully!')
    write_history_file('Password generated successfully!\n')
    return password


def read_csv():
    current_directory = os.getcwd()
    file_name = 'users.csv'
    csv_file = os.path.join(current_directory, file_name)
    if csv_file is None:
        print('Please create csv file first.')
        return None
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
        return False
    print(data)
    return data


def write_csv():
    data = []
    current_directory = os.getcwd()
    file_name = 'users.csv'
    csv_file = os.path.join(current_directory, file_name)
    if csv_file is None:
        print('Please create csv file first.')
        return False
    if os.path.isfile(csv_file) is False:
        print('The csv file does not exist.')
        return False
    try:
        while True:
            username = input('Please enter username or press "Enter" to quit: ')
            if not username:
                print('Registration interrupted.')
                break
            password = input('Please enter password: ')
            while not validate_password(password):
                password = input('Please enter a valid password or press "Enter" to quit: ')
                if not password:
                    print('Registration interrupted.')
                    break
            user_ID = input('Please enter user ID: ')
            data.append([username, password, user_ID])
        with open(csv_file, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(data)
    except OSError:
        print('Error happened while accessing csv file.')
        return False
    return True