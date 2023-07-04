# Credential check program
# Variant 3: "Range function"

stored_username = "sergiy"
stored_password = "123456"

for x in range(5):
    username = input('Enter your username and press "Enter": ')
    password = input('Enter your password and press "Enter": ')
    if username == stored_username and password == stored_password:
        print('Welcome to Tax Management System!')
        quit()
    else:
        print('Incorrect credentials, please check your input!')
