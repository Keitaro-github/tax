# Credentials check program
# Variant 1: "No loops"

stored_username = 'sergiy'
stored_password = '123456'
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
