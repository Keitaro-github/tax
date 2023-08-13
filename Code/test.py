attempts = 0
attempts_limit = 5
users = [
    {"username": "Keitaro", "password": "123456", 'user_id': 1},
    {"username": "Ivan", "password": "654321", 'user_id': 2},
    {"username": "Ben", "password": "999999", 'user_id': 3},
    {"username": "David", "password": "888888", 'user_id': 4},
    {"username": "Chris", "password": "777777", 'user_id': 5},
    {"username": "Gregor", "password": "666666", 'user_id': 6}
]


def generate_id():
    id_list = []
    for user in users:
        id_list.append(user['user_id'])
    if not id_list:
        id_list.insert(0, 1)
    elif id_list[0] != 1:
         id_list.insert(0, 1)
    else:
        for i in range(len(id_list) - 1):
            if id_list[i] == (id_list[i + 1] - 1):
                continue
            else:
                id_list.insert(i + 1, id_list[i] + 1)
                break
        else:
            id_list.append(len(id_list) + 1)
    print(id_list)


generate_id()



