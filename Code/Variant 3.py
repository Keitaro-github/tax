# Credentials check program
# Variant 3: "Range function"

stored_username = "sergiy"
stored_password = "123456"
attempts = 0
attempts_limit = 5

for _ in range(5):
    username = input('Enter your username and press "Enter": ')
    password = input('Enter your password and press "Enter": ')
    if username != stored_username or password != stored_password and attempts < 5:
        attempts = attempts + 1
        print('Incorrect credentials, please check your input!')

    if username == stored_username and password == stored_password:
        print('Welcome to Tax Management System!')
        quit()

    elif attempts == 5:
        print('Oops, too many wrong attempts, please contact administrator!')
        quit()
        