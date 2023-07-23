# Credentials check program
# Variant 2: "While loop"

stored_username = "sergiy"
stored_password = "123456"
attempts = 0
attempts_limit = 5


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
    username = input('Enter your username and press "Enter": ')
    password = input('Enter your password and press "Enter": ')
    # result = validate_password(password)
    # if result is False:
    #     return False
    if username == stored_username and password == stored_password:
        return True
    else:
        return False


while attempts < 5:
    result = sign_in()
    if result is True:
        print('Welcome to Tax Management System!')
        break

    else:
        print('Incorrect credentials, please check your input!')
        attempts += 1

if attempts == attempts_limit:
    print('Oops, too many wrong attempts, please contact administrator!')
