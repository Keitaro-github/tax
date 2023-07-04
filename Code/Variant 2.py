# Credential check program
# Variant 2: "While loop"

stored_username = "sergiy"
stored_password = "123456"
attempts = 0

while attempts < 5:

    username = input('Enter your username and press "Enter": ')
    password = input('Enter your password and press "Enter": ')
    if username == stored_username and password == stored_password:

        print('Welcome to Tax Management System!')
        break

    else:
        print('Incorrect credentials, please check your input!')
        attempts += 1
        continue
