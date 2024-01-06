import random
import getpass
import Code.database_services as database_services
import datetime
import os


file_name = None    
terminal = False
history = False

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
        print('The file does not exist.')
        return False
    try:
        with open(file_name, 'a') as history_file:
            history_file.write(str(interaction_timestamp).strip() + ' ' + message)
    except OSError:
        print('Error happened while accessing history file.')
        return False
    return True


# def output(message, terminal=True, history=True):
def output(message):
    if terminal is True:
        print(message)
    if history is True:
        write_history_file(message + '\n')
        

def generate_id():
    id_list = []
    user_list = database_services.read_csv()
    for user in user_list:
        id_list.append(int(user['user_id']))
    id_list.sort()
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
        output(f"User with ID {id_num} has been deleted")
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
            output(str(user) + '\n')
            found = True
            break
    if not found:
        output(f"Username {username} not found")


def find_user(user_name):
    content = database_services.read_csv()

    for user in content:
        if user['username'] == user_name:
            write_history_file(user_name)
            # output(user_name, terminal=False)
            output(user_name)
            return user_name
    return None


def show_list():
    output('The list of users is as follows:')

    content = database_services.read_csv()
    for user in content:
        output(str(user))


def validate_password(password):
    password_length = len(password)
    password_digits_only = str.isdigit(password)
    password_alphabets_only = str.isalpha(password)

    if password_length <= 7:
        output('Too short password!')
        return False
    elif password_digits_only is True:
        output('Password must contain letters!')
        return False
    elif password_alphabets_only is True:
        output('Password must contain digits!')
        return False
    elif password.islower() is True:
        output('Password must contain uppercase letters!')
        return False
    elif password.isupper() is True:
        output('Password must contain lowercase letters!')
        return False
    else:
        return True


def add_user():
    username = input('Register your username and press <Enter>: ')
    # output(f"Register your username and press <Enter> \n {username}", terminal=False)
    output(f"Register your username and press <Enter> \n {username}")
    while find_user(username) is not None:
        output(f"The username is occupied already, please register unique name")
        username = input('Register your username and press <Enter>: ')
        # output(f"Register your username and press <Enter> \n {username}", terminal=False)
        output(f"Register your username and press <Enter> \n {username}")
    password = input('Register your password and press <Enter>: ')
    # output(f"Register your password and press <Enter> \n", terminal=False)
    output(f"Register your password and press <Enter> \n")
    while not validate_password(password):
        password = input('Please enter a valid password or enter 0 to exit: ')
        # output(f"Please enter a valid password or enter 0 to exit: \n", terminal=False)
        output(f"Please enter a valid password or enter 0 to exit: \n")
        if password == '0':
            # output('0', terminal=False)
            output('0')
            output('Operation aborted.')
            return
    id_num = generate_id()
    database_services.write_csv(username, password, id_num)
    output('User added successfully!')
    user_list = database_services.read_csv()
    database_services.rewrite_csv(user_list)


def credential_check(username, password):
    # username = input('\n' + 'Enter your username and press "Enter": ')
    # # output(f"Register your username and press <Enter> \n {username}", terminal=False)
    # output(f"Register your username and press <Enter> \n {username}")
    # password_input = getpass.getpass('Enter your password and press <Enter>: ')
    # # output(f"Enter your password and press <Enter>: \n", terminal=False)
    # output(f"Enter your password and press <Enter>: \n")


    user_list = database_services.read_csv()
    for user in user_list:
        if username == user['username'] and password == user['password']:
            return True
    return False


def sign_in():  # Works only under debug mode due to implemented feature of hidden password.
    attempts = 0
    attempts_limit = 5
    for _ in range(5):
        if credential_check() is True:
            output('Login successful!')
            break
        else:
            user_input = input('Incorrect credentials, please check your input or enter 0 to exit! ')
            write_history_file(user_input + '\n')
            output(user_input)
            if user_input == '0':
                # output('0', terminal=False)
                output('0')
                output('Operation aborted.')
                return
            else:
                attempts = attempts + 1
    if attempts == attempts_limit:
        output('Oops, too many wrong attempts, please contact administrator!')


def change_password(input_username):
    user_list = database_services.read_csv()
    for user in user_list:
        if user['username'].lower() == input_username.lower():
            input_old_password = input('Hello ''' + user['username'] + ', please enter your password: ')
            # output('\n', terminal=False)
            output('\n')
            if user['password'] != input_old_password:
                # output('Incorrect password entered. Process terminated.', terminal=False)
                output('Incorrect password entered. Process terminated.')
                return False
            elif user['password'] == input_old_password:
                input_new_password1 = input('Please enter your new password: ')
                # output('Please enter your new password: \n', terminal=False)
                output('Please enter your new password: \n')
                while not validate_password(input_new_password1):
                    input_new_password1 = input('Please enter a valid password: ')
                    # output('Please enter a valid password: \n', terminal=False)
                    output('Please enter a valid password: \n')
                    input_new_password2 = input('Please re-enter your new password: ')
                # output('Please re-enter your new password: \n', terminal=False)
                output('Please re-enter your new password: \n')
                if input_new_password1 == input_new_password2:
                    user['password'] = input_new_password2
                    output('Password updated successfully!')
                    user_list = database_services.read_csv()
                    updated_users = []
                    for user in user_list:
                        if user['username'].lower() == input_username.lower():
                            user['password'] = input_new_password2
                        updated_users.append(user)
                    database_services.rewrite_csv(updated_users)
                    return True
                elif input_new_password1 != input_new_password2:
                    output('Password is not the same. Process terminated.')
                    return False
    else:
        output('User with this name is not registered. Process terminated.')
        return False


def generate_password():
    status = False
    password = ''
    while status is False:
        for number in range(8):
            selector = random.randint(0, 2)
            if selector == 0:
                password += str(random.randint(0, 9))
            elif selector == 1:
                password += chr(random.randint(65, 90))
            else:
                password += chr(random.randint(97, 122))
        # status = validate_password(password)
        # Code amended in order to prevent loop of password validation:
        if validate_password(password):
            status = True
            output('Password generated successfully!')
        else:
            continue
    return password
