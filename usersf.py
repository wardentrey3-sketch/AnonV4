from settings import *



users = {}
codes = {}
states = {}

#-----------------------------------




#-----------------------------------
def load_users():
    with open(users_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        users.clear()
        users.update({int(k) if k.isdigit() else k: v for k, v in data.items()})


def save_users():
    with open(users_file_path, 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4)

def add_user(user_id, username, first_name, last_name, reg_date = None):
    users[user_id] = {
        "username": username,
        "first_name": first_name,
        "last_name" : last_name,
        "reg_date" : reg_date
    }
    save_users()


def check_user(message):

    

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    if user_id not in states:
        add_new_user_in_states(user_id)


    flag = False

    if (users[user_id].get('username') != username):
        if username != None:
            users[user_id]['username'] = username
        else:
            if not (users[user_id]['username'].endswith('now Unknown)')):
                users[user_id]['username'] += "  (For now Unknown)"
        flag = True

    if (users[user_id].get('first_name') != first_name):
        users[user_id]['first_name'] = first_name
        flag = True
        

    if (users[user_id].get('last_name') != last_name):
        if last_name != None:
            users[user_id]['last_name'] = last_name
        else:
            if not (users[user_id]['last_name'].endswith('now Unknown)')):
                users[user_id]['last_name'] += "  (For now Unknown)"
        flag = True

    if flag:
        save_users()        


#-----------------------------------

def load_codes():
    with open(codes_file_path, 'r') as file:
        data = json.load(file)
        codes.clear()
        codes.update(data)

def save_codes():
    with open(codes_file_path, 'w') as file:
        json.dump(codes, file, indent=4)



def new_code(id):
    for code, user_id in codes.items():
        if user_id == id:
            return code

    while True:
        code = "".join(random.choices(alphabet, k=code_size))
        if code not in codes: 
            break
            
    codes[code] = id
    save_codes()
    return code

            
def del_code(id):

    code_to_delete = None

    for code, user_id in codes.items():
        if user_id == id:
            code_to_delete = code
            break
    
    if code_to_delete:
        codes.pop(code_to_delete)
        save_codes()
        return code_to_delete

    return None
                


#-----------------------------------


def load_states():
    with open(states_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        states.clear()
        states.update({int(k) if k.isdigit() else k: v for k, v in data.items()})


def save_states():
    with open(states_file_path, 'w', encoding='utf-8') as file:
        json.dump(states, file, indent=4)


def add_new_user_in_states(id):

    states[id] = {
        "state": 0,
        "last_code": None,
        "banner_id" : None
    }
    save_states()

def change_state(id, state):
    states[id]["state"] = state
    save_states()

def change_state_last_code(id, last_code):
    states[id]["last_code"] = last_code
    save_states()

def change_state_banner_id(id, banner_id):
    states[id]["banner_id"] = banner_id
    save_states()


