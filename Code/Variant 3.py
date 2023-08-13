# Credentials check program
# Variant 3: "Range function"
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


generate_id()


def delete_user(id_num):
    for user in users:
        if user['user_id'] == id_num:
            users.remove(user)
            print(f'User with ID {id_num} has been deleted')
            break


# delete_user(6)
#
#
# def user_info_printout(users):
#     while True:
#         print('Please enter user ID for printout:')
#         try:
#             user_id_input = int(input())
#         except ValueError:
#             print('Invalid input. Please neter a valid user ID.')
#             continue
#         found = False
#         for user in users:
#             if user['user_id'] == user_id_input:
#                 print(user)
#                 found = True
#                 break
#         if not found:
#             print(f'User with ID {user_id_input} not found')
#
#
# user_info_printout(users)

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


add_user()
show_list()


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
