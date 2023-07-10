# Credentials check program
# Variant 1: "No loops"

stored_username = "sergiy"
stored_password = "123456"
username = input('Enter your username and press "Enter": ')
password = input('Enter your password and press "Enter": ')

if username != stored_username or password != stored_password:
    print('Incorrect credentials, please check your input!')
    username = input('Enter your username and press "Enter": ')
    password = input('Enter your password and press "Enter": ')

    if username != stored_username or password != stored_password:
        print('Incorrect credentials, please check your input!')
        username = input('Enter your usernC:\Users\serge\PycharmProjects\pythonProject\pet_projects\tax\CodeC:\Users\serge\PycharmProjects\pythonProject\pet_projects\tax\Codeame and press "Enter": ')
        password = input('Enter your password and press "Enter": ')

        if username != stored_username or password != stored_password:
            print('Incorrect credentials, please check your input!')
            username = input('Enter your username and press "Enter": ')
            password = input('Enter your password and press "Enter": ')

            if username != stored_username or password != stored_password:
                print('Incorrect credentials, please check your input!')
                username = input('Enter your username and press "Enter": ')
                password = input('Enter your password and press "Enter": ')

                if username != stored_username or password != stored_password:
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
