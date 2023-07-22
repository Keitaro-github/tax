# Credentials check program
# Variant 1: "No loops"

stored_username = 'sergiy'
stored_password = '123456'
username = input('Enter your username and press "Enter": ')
password = input('Enter your password and press "Enter": ')


def validate_password():
    password_length = len(str(password))
    password_digits_only = str.isdigit(password)
    password_alphabets_only = str.isalpha(password)

    if password_length <= 7:
        return True and print('Too short password!')
    elif password_digits_only:
        return True and print('Password must contain letters!')
    elif password_alphabets_only:
        return True and print('Password must contain digits!')


# validate_password()


result = username == stored_username and password == stored_password

if result is False:
    print('Incorrect credentials, please check your input!')
    username = input('Enter your username and press "Enter": ')
    password = input('Enter your password and press "Enter": ')
    result = username == stored_username and password == stored_password

    if result is False:
        print('Incorrect credentials, please check your input!')
        username = input('Enter your username and press "Enter": ')
        password = input('Enter your password and press "Enter": ')
        result = username == stored_username and password == stored_password

        if result is False:
            print('Incorrect credentials, please check your input!')
            username = input('Enter your username and press "Enter": ')
            password = input('Enter your password and press "Enter": ')
            result = username == stored_username and password == stored_password

            if result is False:
                print('Incorrect credentials, please check your input!')
                username = input('Enter your username and press "Enter": ')
                password = input('Enter your password and press "Enter": ')
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
