# Credentials check program
# Variant 2: "While loop"

stored_username = "sergiy"
stored_password = "123456"
attempts = 0

while attempts < 5:

    username = input('Enter your username and press "Enter": ')
    password = input('Enter your password and press "Enter": ')
    if username != stored_username or password != stored_password:
        print('Incorrect credentials, please check your input!')
        attempts += 1

    else:
        print('Welcome to Tax Management System!')
        break

if attempts == 5:
    print('Oops, too many wrong attempts, please contact administrator!')
