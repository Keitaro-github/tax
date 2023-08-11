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


def delete_user_by_id(users):
    while True:
        print('Please enter user ID for deletion:')
        try:
            user_id_input = int(input())
        except ValueError:
            print('Invalid input. Please neter a valid user ID.')
            continue
        for user in users:
            if user['user_id'] == user_id_input:
                users.remove(user)
                print(f'User with ID {user_id_input} has been deleted')
                break
            else:
                print(f'User with ID {user_id_input} not found')
                break


delete_user_by_id(users)


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


user_info_printout(users)


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
    else:
        return True


def add_user():
    show_list()
    while True:
        print('')
        username = input('Register your username and press "Enter": ')
        password = input('Register your password and press "Enter": ')
        while not validate_password(password):
            password = input('Please enter a valid password: ')
        id_num = input('Register your ID and press "Enter": ')
        if users.append({"username": username, "password": password, "ID": id_num}):
            add_user()


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
