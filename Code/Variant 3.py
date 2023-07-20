# Credentials check program
# Variant 3: "Range function"

stored_username = "sergiy"
stored_password = "123456"
attempts = 0

"""
for _ in range(5):
    username = input('Enter your username and press "Enter": ')
    password = input('Enter your password and press "Enter": ')
    result = username == stored_username and password == stored_password
    if result is False < 5:
        attempts = attempts + 1
        print('Incorrect credentials, please check your input!')

    if result is True:
        print('Welcome to Tax Management System!')
        quit()

    elif attempts == 5:
        print('Oops, too many wrong attempts, please contact administrator!')
        quit()
"""

result = False

for _ in range(5):
    username = input('Enter your username and press "Enter": ')
    password = input('Enter your password and press "Enter": ')
    
    if username != stored_username or password != stored_password:
        print('Incorrect credentials, please check your input!')
    else:
        print('Welcome to Tax Management System!')
        result = True
        break

if result is False:
    print ("Oops, too many wrong attempts, please contact administrator!")
