# Credentials check program
# Variant 1: "No loops"

stored_username = 'sergiy'
stored_password = '123456'
username = input('Enter your username and press "Enter": ')
password = input('Enter your password and press "Enter": ')


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


result = username == stored_username and password == stored_password

if result is False:
    print('Incorrect credentials, please check your input!')
    username = input('Enter your username and press "Enter": ')
    password = input('Enter your password and press "Enter": ')
    # result = validate_password(password)
    result = username == stored_username and password == stored_password

    if result is False:
        print('Incorrect credentials, please check your input!')
        username = input('Enter your username and press "Enter": ')
        password = input('Enter your password and press "Enter": ')
        # result = validate_password(password)
        result = username == stored_username and password == stored_password

        if result is False:
            print('Incorrect credentials, please check your input!')
            username = input('Enter your username and press "Enter": ')
            password = input('Enter your password and press "Enter": ')
            # result = validate_password(password)
            result = username == stored_username and password == stored_password

            if result is False:
                print('Incorrect credentials, please check your input!')
                username = input('Enter your username and press "Enter": ')
                password = input('Enter your password and press "Enter": ')
                # result = validate_password(password)
                result = username == stored_username and password == stored_password

                if result is False:
                    print('Incorrect credentials, please check your input!')
                    print('Oops, too many wrong attempts, please contact administrator!')

                else:
                    print('Welcome to Tax Management System!')

            else:
                print('Welcome to Tax Management System!')

        else:
            print('Welcome to Tax Management System!')

    else:
        print('Welcome to Tax Management System!')

else:
    print('Welcome to Tax Management System!')
