import random
import getpass
import database_services
import datetime
import os
file_name = None


def create_history_file():
    global file_name

    timestamp = datetime.datetime.now()
    file_timestamp = timestamp.strftime('%Y%m%d_%H%M%S')
    file_name = 'History_' + file_timestamp + '.txt'
    interaction_timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S\n')
    file_timestamp = timestamp.strftime('%Y%m%d_%H%M%S')

    # Get current module location.
    current_folder = os.getcwd()
    #  Create "cache" folder pathname.
    cache_folder = os.path.join(current_folder, "cache")
    # Check whether cache folder has not been created yet.
    if not os.path.isdir(cache_folder):
        # Create cache folder on PC for storing all histories.
        os.mkdir(cache_folder)
    # Create absolute history filename based on full path to cache folder
    # and history filename.
    file_name = os.path.join(cache_folder, 'History_' + file_timestamp + '.txt')

    with open(file_name, 'w') as history_file:
        history_file.write(str(interaction_timestamp).strip() + ' The program initiated.\n')


def write_history_file(message):
    global file_name

    timestamp = datetime.datetime.now()
    interaction_timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S\n')

    if file_name is None:
        print('Please create file first.')
        return False
    if not os.path.isfile(file_name):
        print('The file does not exists.')
        return False
    try:
        with open(file_name, 'a') as history_file:
            history_file.write(str(interaction_timestamp).strip() + ' ' + message)
    except OSError:
        print('Error happened while accessing history file.')
        return False
    return True


def generate_id():
    id_list = []
    user_list = database_services.read_csv()
    for user in user_list:
        id_list.append(int(user['user_id']))
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
    user_list = database_services.read_csv()
    index = None
    for i, user in enumerate(user_list):
        if int(user['user_id']) == id_num:
            index = i
            break
        else:
            continue
    if index is not None:
        user_list.pop(index)
        print(f'User with ID {id_num} has been deleted')
        write_history_file(f'User with ID {id_num} has been deleted\n')
        database_services.rewrite_csv(user_list)
        return user_list
        # How to write an updated list back to csv.file?
    else:
        print('The user with such ID was not found.')
        write_history_file('The user with such ID was not found.\n')


def user_info_printout(username=None):
    found = False
    # username = 'Ben' #Line for manual test
    user_list = database_services.read_csv()
    for user in user_list:
        if user['username'] == username:
            write_history_file(str(user) + '\n')
            found = True
            break
    if not found:
        print(f'Username {username} not found')
        write_history_file(f'Username {username} not found\n')


def find_user(user_name):
    output = database_services.read_csv()
    for user in output:
        if user['username'] == user_name:
            write_history_file(user_name)
            return user_name
    return None


result = find_user('Nikolai')


def show_list():
    print('The list of users is as follows:')
    write_history_file('The list of users is as follows:\n')
    output = database_services.read_csv()
    for user in output:
        print(user)
        write_history_file(str(user) + '\n')


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
    database_services.write_csv(username, password, id_num)
    print('User added successfully!')
    write_history_file('User added successfully!\n')
    user_list = database_services.read_csv()
    database_services.rewrite_csv(user_list)


def credential_check():
    username_input = input('\n' + 'Enter your username and press "Enter": ')
    write_history_file('Enter your username and press "Enter": \n')
    write_history_file(username_input + '\n')
    password_input = getpass.getpass('Enter your password and press "Enter": ')
    write_history_file('Enter your password and press "Enter": \n')
    write_history_file('\n')
    user_list = database_services.read_csv()
    for user in user_list:
        if username_input == user['username'] and password_input == user['password']:
            return True
    return False


def sign_in():  # Works only under debug mode due to implemented feature of hidden password.
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
    user_list = database_services.read_csv()
    for user in user_list:
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
                    user_list = database_services.read_csv()
                    updated_users = []
                    for user in user_list:
                        if user['username'].lower() == input_username.lower():
                            user['password'] = input_new_password2
                        updated_users.append(user)
                    database_services.rewrite_csv(updated_users)
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
