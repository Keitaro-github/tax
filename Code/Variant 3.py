# Credentials check program
# Variant 3: "Range function"

stored_username = "sergiy"
stored_password = "123456"

for _ in range(5):
    username = input('Enter your username and press "Enter": ')
    password = input('Enter your password and press "Enter": ')
    if username != stored_username or password != stored_password:
        print('Incorrect credentials, please check your input!')
    else:
        print('Welcome to Tax Management System!')
