# Credentials check program
# Variant 2: "While loop"

stored_username = "sergiy"
stored_password = "123456"
attempts = 0
attempts_limit = 5

while attempts < 5:

    username = input('Enter your username and press "Enter": ')
    password = input('Enter your password and press "Enter": ')
    result = username == stored_username and password == stored_password

    if result is False:
        print('Incorrect credentials, please check your input!')
        attempts += 1

    else:
        print('Welcome to Tax Management System!')
        break

if attempts == attempts_limit:
    print('Oops, too many wrong attempts, please contact administrator!')
