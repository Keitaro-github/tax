import signin_services
import database_services

signin_services.create_history_file()


menu = 'Welcome to Tax Management System!'  \
       '\n\n MENU'                          \
       '\n 1. Sign in'                      \
       '\n 2. Add new user'                 \
       '\n 3. Change password'              \
       '\n 4. Generate password'            \
       '\n 5. Delete user'                  \
       '\n 6. Find user'                    \
       '\n 0. Exit operation'               \

print(menu)

signin_services.write_history_file(menu)

operations = {
      1: 'Sign in',
      2: 'Add new user',
      3: 'Change password',
      4: 'Generate password',
      5: 'Delete user',
      6: 'Find user',
      0: 'Exit operation',
}

while True:
    try:
        operation = int(input('\nChoose operation: '))
    except ValueError as error:
        print(error)
        continue

    signin_services.write_history_file('Choose operation: \n')
    signin_services.write_history_file(str(operation) + '\n')

    if operation == 1:
        result = signin_services.sign_in()
    elif operation == 2:
        signin_services.add_user()
    elif operation == 3:
        input_username = input('Please input username: ')
        signin_services.write_history_file('Please input username: \n')
        signin_services.write_history_file(input_username + '\n')
        result = signin_services.change_password(input_username)
    elif operation == 4:
        result = signin_services.generate_password()
    elif operation == 5:
        try:
            id_num = int(input('Please input ID: '))
        except ValueError as error:
            print(error)
        else:   
            signin_services.write_history_file('Please input ID: \n')
            signin_services.write_history_file(str(id_num) + '\n')
            result = signin_services.delete_user(id_num)
    elif operation == 6:
        user_name = input('Please input username: ')
        signin_services.write_history_file('Please input username: \n')
        signin_services.write_history_file(user_name + '\n')
        result = signin_services.find_user(user_name)
        if result is not None:
            print("The user has been found")
        else:
            print("The user has not been found")
    elif operation == 7:
        result = signin_services.show_list()
    elif operation == 8:
        result = signin_services.generate_id()
    elif operation == 9:
        result = signin_services.user_info_printout(username=None)
    elif operation == 10:
        result = database_services.read_csv()
    elif operation == 11:
        result = database_services.write_csv()
    elif operation == 0:
        print('You have exited the application.')
        signin_services.write_history_file('You have exited the application.\n')
        break
    else:
        print('Please choose correct operation number.')
        signin_services.write_history_file('Please choose correct operation number.\n')
