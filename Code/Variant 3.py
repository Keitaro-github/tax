# Credentials check program
# Variant 3: "Range function"
import random
attempts = 0
attempts_limit = 5
users = [
    {"username": "Keitaro", "password": "123456", 'user_id': 1},
    {"username": "Ivan", "password": "654321", 'user_id': 2},
    {"username": "Ben", "password": "999999", 'user_id': 3},
    {"username": "David", "password": "888888", 'user_id': 4},
    {"username": "Chris", "password": "777777", 'user_id': 5},
    {"username": "Gregor", "password": "666666", 'user_id': 6}
]


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
            break


def user_info_printout(users):
    while True:
        print('Please enter user ID for printout:')
        try:
            user_id_input = int(input())
        except ValueError:
            print('Invalid input. Please neter a valid user ID.')
            continue
        found = False
        for user in users:
            if user['user_id'] == user_id_input:
                print(user)
                found = True
                break
        if not found:
            print(f'User with ID {user_id_input} not found')


def find_user(user_name):
    for user in users:
        if user['username'] == user_name:
            print(user_name)
            return user
    return None


result = find_user('Tom')


def show_list():
    print('The list of users is as follows:')
    for user in users:
        print(user['username'])


def validate_password(password):
    password_length = len(password)
    password_digits_only = str.isdigit(password)
    password_alphabets_only = str.isalpha(password)
    if password_length <= 7:
        print('Too short password!')
        return False
    elif password_digits_only is True:
        print('Password must contain letters!')
        return False
    elif password_alphabets_only is True:
        print('Password must contain digits!')
        return False
    elif password.islower() is True:
        print('Password must contain uppercase letters!')
        return False
    elif password.isupper() is True:
        print('Password must contain lowercase letters!')
        return False
    else:
        return True


def add_user():
    show_list()
    print('')
    username = input('Register your username and press "Enter": ')
    while find_user(username) is not None:
        print('The name with this name is already registered, please provide another name')
        username = input('Register your username and press "Enter": ')
    password = input('Register your password and press "Enter": ')
    while not validate_password(password):
        password = input('Please enter a valid password: ')
    id_num = generate_id()
    users.append({"username": username, "password": password, "ID": id_num})


def sign_in():
    print('')
    username_input = input('Enter your username and press "Enter": ')
    password_input = input('Enter your password and press "Enter": ')
    for user in users:
        if username_input == user['username'] and password_input == user['password']:
            return True
    return False


for _ in range(5):
    if sign_in() is True:
        print('Welcome to Tax Management System!')
        break
    else:
        print('Incorrect credentials, please check your input!')
        attempts = attempts + 1
if attempts == attempts_limit:
    print("Oops, too many wrong attempts, please contact administrator!")


def change_password(input_username):
    for user in users:
        if user['username'].lower() == input_username.lower():
            input_old_password = input("Hello " + user['username'] + ", please enter your password: ")
            if user['password'] != input_old_password:
                print('Incorrect password entered. Process terminated.')
                return False
            elif user['password'] == input_old_password:
                input_new_password1 = input("Please enter your new password: ")
                while not validate_password(input_new_password1):
                    input_new_password1 = input('Please enter a valid password: ')
                input_new_password2 = input("Please re-enter your new password: ")
                if input_new_password1 == input_new_password2:
                    user['password'] = input_new_password2
                    print('Password updated successfully!')
                    return True
                elif input_new_password1 != input_new_password2:
                    print('Password is not the same. Process terminated.')
                    return False
    else:
        print('User with this name is not registered. Process terminated.')
        return False


def generate_pass():
    pass_list = []
    for number in range(8):
        set_selector = random.randint(0, 2)
        if set_selector == 0:
            pass_list.append(str(random.randint(0, 9)))
        elif set_selector == 1:
            pass_list.append(chr(random.randint(65, 90)))
        else:
            pass_list.append(chr(random.randint(97, 122)))
    password = ''
    for symbol in pass_list:
        password += symbol
    while not validate_password(password):
        generate_pass()
    else:
        return password
