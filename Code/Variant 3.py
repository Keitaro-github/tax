# Credentials check program
# Variant 3: "Range function"

stored_username = "sergiy"
stored_password = "123456"
attempts = 0
attempts_limit = 5


def sign_in():
    username = input('Enter your username and press "Enter": ')
    password = input('Enter your password and press "Enter": ')
    if username == stored_username and password == stored_password:
        return True
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
