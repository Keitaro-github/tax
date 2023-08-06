# Credentials check program
# Variant 3: "Range function"

# stored_username = "sergiy"
# stored_password = "123456"
attempts = 0
attempts_limit = 5
users = [
    {"username": "Keitaro", "password": "123456", 'ID': 1},
    {"username": "Ivan", "password": "654321", 'ID': 2},
    {"username": "Ben", "password": "999999", 'ID': 3},
    {"username": "David", "password": "888888", 'ID': 4},
    {"username": "Chris", "password": "777777", 'ID': 5},
    {"username": "Gregor", "password": "666666", 'ID': 6}
]


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


def sign_in():
    username_input = input('Enter your username and press "Enter": ')
    password_input = input('Enter your password and press "Enter": ')
    for user in users:
        if username_input == user['username'] and password_input == user['password']:
            return True
        elif username_input != user['username'] or password_input != user['password']:
            continue
        else:
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
