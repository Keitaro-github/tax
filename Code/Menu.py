from database import users
import signin_services
print('Welcome to Tax Management System!')
print('\n MENU'
      '\n 1. Sign in'
      '\n 2. Add new user'
      '\n 3. Change password'
      '\n 4. Generate password'
      '\n 5. Delete user'
      # '\n 6. Find user'
      # '\n 7. Show list'
      # '\n 8. Generate ID'
      # '\n 9. user infor printout'
      '\n 0. Exit operation'
      )

operations = {
      1: 'Sign in',
      2: 'Add new user',
      3: 'Change password',
      4: 'Generate password',
      5: 'Delete user',
      # 6: 'Find user',
      # 7: 'Show list',
      # 8: 'Generate ID',
      # 9: 'User info printout'
      0: 'Exit operation'
}
while True:
    operation = int(input('\nChoose operation: '))
    if operation == 1:
        result = signin_services.sign_in()
    elif operation == 2:
        signin_services.add_user()
    elif operation == 3:
        input_username = input('PLease input username: ')
        result = signin_services.change_password(input_username)
    elif operation == 4:
        result = signin_services.generate_password()
    elif operation == 5:
        id_num = int(input('PLease input ID: '))
        result = signin_services.delete_user(id_num)
    elif operation == 6:
        user_name = input('PLease input username: ')
        result = signin_services.find_user(user_name)
    elif operation == 7:
        result = signin_services.show_list()
    elif operation == 8:
        result = signin_services.generate_id()
    elif operation == 9:
        users = input('PLease input username')
        result = signin_services.user_info_printout(users)
    elif operation == 0:
        print('You have exited application.')
        break
    else:
        print('Please choose correct operation number.')

