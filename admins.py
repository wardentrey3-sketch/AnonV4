from settings import *
from usersf import *
from time import perf_counter
from messages import *
import menu_buttons
from historyf import *



from telebot.apihelper import ApiTelegramException


admins = {}

log_text = """
<b>admin_log:</b>

<i>ОТ:</i> <code>{}</code>\t\t(<code>{}</code>)
<i>К:</i> <code>{}</code>\t\t(<code>{}</code>)

<blockquote><b>{}</b></blockquote>
"""

log_media = """
<b>admin_log:</b>

<i>ОТ:</i> <code>{}</code>\t\t(<code>{}</code>)
<i>К:</i> <code>{}</code>\t\t(<code>{}</code>)
"""


def reset_state(id, is_cancel = True):
    if states[id]['banner_id'] != None:
        bot.delete_message(id, states[id]['banner_id'])
        change_state_banner_id(id, None)
        if is_cancel:
            if states[id]['state'] != 2:
                admin_log(f"<b>{users[id]['username']}</b> (<code>{id}</code>) ОТМЕНА для <b>{users[codes[states[id]['last_code']]]['username']}</b> (<code>{codes[states[id]['last_code']]}</code>)")
            else:
                main_admin_log(f"{id} cancel start_mask")

    change_state(id, 0)


def load_admins():
    with open(admins_file_path, 'r') as file:
        data = json.load(file)
        admins.clear()
        admins.update({int(k): v for k, v in data.items()})

def save_admins():
    with open(admins_file_path, 'w') as file:
        json.dump(admins, file, indent=4)

def new_admin(id, smile):
    admins[id] = {'smile' : smile, 'mask' : {'username' : None, 'id' : None, 'first_name' : None, 'last_name' : None}, 'log_stat' : True}
    save_admins()

def admin_log_text(message,ot_id ,to_id):
    text = log_text.format(users[ot_id]['username'], ot_id, users[to_id]['username'], to_id,message.text)

    for i in admins:
        try:
            if admins[i]['log_stat']:
                bot.send_message(i, text, parse_mode='HTML')
        except:
            print(i)


def admin_log_media(message,ot_id ,to_id):
    text = log_media.format(users[ot_id]['username'], ot_id, users[to_id]['username'], to_id)

    for i in admins:
        try:
            if admins[i]['log_stat']:
                res = bot.copy_message(
                    chat_id = i,
                    from_chat_id=message.from_user.id,
                    message_id=message.message_id
                )
                bot.send_message(i, text, parse_mode='HTML', reply_to_message_id=res.message_id)
        except:
            print(i)

def admin_log(text):
    for i in admins:
        if admins[i]['log_stat']:
            try:
                bot.send_message(i, text, parse_mode='HTML')
            except:
                pass

def main_admin_log(text):
    if admins[ADMIN_ID]['log_stat']:
        try:
            bot.send_message(ADMIN_ID, text, parse_mode='HTML')
        except:
            pass


@bot.message_handler(commands=['get'])
def get_users(message):
    adm_id = message.from_user.id


    if adm_id in admins:
        colvo = len(message.text.split())
        if colvo == 1:
            current_message = ""

            for user_id, info in users.items():
                
                user_line = (
                    f"<code>{user_id}</code>: @{info.get('username', 'None')}\n"
                )

                
                if len(current_message) + len(user_line) > MAX_LENGTH:
                    
                    bot.send_message(adm_id, current_message, parse_mode='HTML')
                    current_message = user_line  
                else:
                    current_message += user_line

            
            if current_message:
                bot.send_message(adm_id, current_message, parse_mode="HTML")

            bot.send_message(adm_id, len(users))
        elif colvo == 2:
            user_id = message.text.split()[1]
            try:
                if int(user_id) in users:
                    user_id = int(user_id)

                    for k, v in codes.items():
                        if v == user_id:
                            code = k
                            break
                        code = None

                    is_blocked = "Не известно"
                    try:
                        bot.send_chat_action(user_id, 'typing')
                        is_blocked = "Бот разблокирован"
                    except ApiTelegramException as e:
                        if e.error_code == 403:
                            is_blocked = "Бот заблокирован"
                    except:
                        pass


                    ref = f"tg://user?id={user_id}"

                    user_line = (
                    f"<code>{user_id}</code>:\n\n"
                    f"<i>Username</i>: @{users[user_id].get('username', 'None')}\n"
                    f"<i>First_name</i>: <code>{users[user_id].get('first_name', 'None')}</code>\n"
                    f"<i>Last_name</i>: <code>{users[user_id].get('last_name', 'None')}</code>\n"
                    f"<i>ANON code</i>: {f't.me/letzqbot?start={code}' if code else 'None'}\n"
                    f"<i>Reg date</i>: {users[user_id].get('reg_date', 'none')}\n"
                    f"<i>Is blocked?</i>: {is_blocked}\n\n"
                    f"<i>Ref</i>: {ref}"
                    )
                    

                    bot.send_message(adm_id, user_line, parse_mode= 'HTML', disable_web_page_preview=True)
                else:
                    bot.send_message(adm_id, 'Не найдено')
            except:
                bot.send_message(adm_id, 'Не верный ввод')
            
        else:
            bot.send_message(adm_id, '<b>Error</b>\n\n/admhelp', parse_mode='HTML')

        if adm_id != ADMIN_ID:
            main_admin_log(f"{adm_id} - <code>{message.text}</code>")
    else:
        bot.send_message(adm_id, empty_send_error_text, parse_mode='HTML')

@bot.message_handler(commands=['codes'])
def get_codes(message):
    adm_id = message.from_user.id


    if adm_id in admins:
        colvo = len(message.text.split())
        if colvo == 1:
            current_message = ""

            for code, id in codes.items():
                ref = f"t.me/letzqbot?start={code}"
                user_line = (
                    f"<code>{id}</code>: <a href=\"{ref}\">{users[id]['username'] if id in users else 'None'}</a>\n"
                )

                
                if len(current_message) + len(user_line) > MAX_LENGTH:
                    
                    bot.send_message(adm_id, current_message, parse_mode='HTML', disable_web_page_preview=True)
                    current_message = user_line  
                else:
                    current_message += user_line

            
            if current_message:
                bot.send_message(adm_id, current_message, parse_mode="HTML", disable_web_page_preview=True)
            
            bot.send_message(adm_id, len(codes))

        elif colvo == 2:
            code = message.text.split()[1]
            if code in codes:
                bot.send_message(adm_id, f"<code>{codes[code]}</code>", parse_mode='HTML')
            else:
                bot.send_message(adm_id, "Не найдено")

        else:
            bot.send_message(adm_id, '<b>Error</b>\n\n/admhelp', parse_mode='HTML')

        if adm_id != ADMIN_ID:
            main_admin_log(f"{adm_id} - <code>{message.text}</code>")
    else:
        bot.send_message(adm_id, empty_send_error_text, parse_mode='HTML')

@bot.message_handler(commands=['new'])
def get_new_code(message):
    adm_id = message.from_user.id
    if adm_id in admins:
        if len(message.text.split()) == 2:
            user_id = message.text.split()[1]
            try:
                ref = (
                f"t.me/letzqbot?start={new_code(int(user_id))}\n\n"
                f"<i>Is in users</i>: <b>{"Yes" if int(user_id) in users else "No"}</b>"
                )
                bot.send_message(adm_id, ref, disable_web_page_preview=True, parse_mode='HTML')
                main_admin_log(f"{adm_id} new ref for {user_id}")
            except:
                bot.send_message(adm_id, 'Error')
        else:
                bot.send_message(adm_id, "<b>Введи ID Пользователя после команды /new</b>\n\n<code>/new 1927309382</code>", parse_mode='HTML')
        if adm_id != ADMIN_ID:
            main_admin_log(f"{adm_id} - <code>{message.text}</code>")
    else:
        bot.send_message(adm_id, empty_send_error_text, parse_mode='HTML')


@bot.message_handler(commands=['change_mask'])
def change_mask(message):
    adm_id = message.from_user.id

    if adm_id in admins:
        colvo = len(message.text.split())

        if colvo == 2:
            try:
                mask_id = int(message.text.split()[1])
                if mask_id in users:
                    if mask_id != ADMIN_ID:
                        admins[adm_id]['mask']['id'] = mask_id
                        admins[adm_id]['mask']['username'] = users[mask_id]['username']
                        admins[adm_id]['mask']['first_name'] = users[mask_id]['first_name']
                        admins[adm_id]['mask']['last_name'] = users[mask_id]['last_name']
                    else:
                        admins[adm_id]['mask']['id'] = adm_id
                        admins[adm_id]['mask']['username'] = users[adm_id]['username']
                        admins[adm_id]['mask']['first_name'] = users[adm_id]['first_name']
                        admins[adm_id]['mask']['last_name'] = users[adm_id]['last_name']   
                        main_admin_log(f"{adm_id} Попытался замаскироваться под {ADMIN_ID}")           
                    save_admins()
                    bot.send_message(adm_id, 'Готово')
                else:
                    bot.send_message(adm_id, 'Такой пользователь не найден')
            except:
                    bot.send_message(adm_id, 'Error')
        elif colvo == 5:
            try:
                mask_id = int(message.text.split()[1])
                mask_username = message.text.split()[2]
                mask_first_name = message.text.split()[3]
                mask_last_name = message.text.split()[4]
                if mask_id == ADMIN_ID or mask_username.lower() in ['yii_t', '@yii_t']:
                    admins[adm_id]['mask']['id'] = adm_id
                    admins[adm_id]['mask']['username'] = users[adm_id]['username']
                    admins[adm_id]['mask']['first_name'] = users[adm_id]['first_name']
                    admins[adm_id]['mask']['last_name'] = users[adm_id]['last_name']   
                    main_admin_log(f"{adm_id} Попытался замаскироваться под {ADMIN_ID} (custom)")                 
                else:
                    admins[adm_id]['mask']['id'] = mask_id
                    admins[adm_id]['mask']['username'] = mask_username
                    admins[adm_id]['mask']['first_name'] = mask_first_name
                    admins[adm_id]['mask']['last_name'] = mask_last_name
                save_admins()
                bot.send_message(adm_id, 'Готово')
            except:
                bot.send_message(adm_id, 'Error')
        elif colvo == 1:
            line = (
                f"<b>Маска</b> {admins[adm_id]['smile']}\n\n"
                f"<i>ID:</i> {admins[adm_id]['mask']['id']}\n"
                f"<i>Username:</i> {admins[adm_id]['mask']['username']}\n"
                f"<i>First name:</i> {admins[adm_id]['mask']['first_name']}\n"
                f"<i>Last_name:</i> {admins[adm_id]['mask']['last_name']}\n"
                f"<i>Is prem?:</i> None\n"
                f"<i>Lang code:</i> ru\n"
            )

            bot.send_message(adm_id, line, parse_mode='HTML')
    
        else:
                bot.send_message(adm_id, '<b>Error</b>\n\n/admhelp', parse_mode='HTML')
        
        if adm_id != ADMIN_ID:
            main_admin_log(f"{adm_id} - <code>{message.text}</code>")
    else:
        bot.send_message(adm_id, empty_send_error_text, parse_mode='HTML')

@bot.message_handler(commands=['show_active_states'])
def show_active_states(message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        for i in states:
            if states[i]['state']:
                main_admin_log(f"<code>{i}</code> - <code>{codes[states[i]['last_code']] if states[i]['last_code'] in codes else None}</code>")
        main_admin_log('done')
    else:
        bot.send_message(user_id, empty_send_error_text, parse_mode='HTML')

@bot.message_handler(commands=['reset_mask'])
def reset_mask(message):
    adm_id = message.from_user.id

    if adm_id in admins:
        admins[adm_id]['mask']['id'] = adm_id
        admins[adm_id]['mask']['username'] = users[adm_id]['username']
        admins[adm_id]['mask']['first_name'] = users[adm_id]['first_name']
        admins[adm_id]['mask']['last_name'] = users[adm_id]['last_name']
        save_admins()
        bot.send_message(adm_id, 'Готово')

        if adm_id != ADMIN_ID:
            main_admin_log(f"{adm_id} reset mask")

    else:
        bot.send_message(adm_id, empty_send_error_text, parse_mode='HTML')


@bot.message_handler(commands=['start_mask'])
def start_mask(message):
    adm_id = message.from_user.id

    if adm_id in admins:

        reset_state(adm_id)

        if len(message.text.split()) == 2:
            try:
                lox_code = int(message.text.split()[1])
                is_in_codes = False

                for k, v in codes.items():
                    if v == lox_code:
                        is_in_codes = True
                        lox_code = k
                        break
                
                if is_in_codes:
                    change_state(adm_id, 2)
                    change_state_last_code(adm_id, lox_code)
                    
                    banner_id = bot.send_message(adm_id, menu_buttons.banner_text, parse_mode='HTML', reply_markup=menu_buttons.get_cancel_button_markup(adm_id)).message_id
                    change_state_banner_id(adm_id, banner_id)
                else:
                    bot.send_message(adm_id, 'Нельзя написать человеку у которого нету ссылки')

                    
            except Exception as e:
                bot.send_message(adm_id, e)
        
        else:
            bot.send_message(adm_id, '<b>Error</b>\n\n/admhelp', parse_mode='HTML')

        if adm_id != ADMIN_ID:
            main_admin_log(f"{adm_id} - {message.text}")

    else:
        bot.send_message(adm_id, empty_send_error_text, parse_mode='HTML')


@bot.message_handler(commands=['h'])
def hide_logs(message):
    adm_id = message.from_user.id
    if adm_id in admins:
        admins[adm_id]['log_stat'] = False
        save_admins()
        if adm_id != ADMIN_ID:
            main_admin_log(f"{adm_id} - hide")
    else:
        bot.send_message(adm_id, empty_send_error_text, parse_mode='HTML')

@bot.message_handler(commands=['s'])
def hide_logs(message):
    adm_id = message.from_user.id
    if adm_id in admins:
        admins[adm_id]['log_stat'] = True
        save_admins()
        if adm_id != ADMIN_ID:
            main_admin_log(f"{adm_id} - show")
    else:
        bot.send_message(adm_id, empty_send_error_text, parse_mode='HTML')


@bot.message_handler(commands=['ping'])
def ping(message):
    if message.from_user.id == ADMIN_ID:
        start_time = perf_counter()
        sent_msg = bot.send_message(message.chat.id, ".")
        end_time = perf_counter()
        duration = (end_time - start_time) * 1000
        bot.send_message(message.from_user.id, duration)
    else:
        bot.send_message(message.from_user.id, empty_send_error_text, parse_mode='HTML')


@bot.message_handler(commands=['h_all'])
def hide_all_logs(message):
    adm_id = message.from_user.id
    if adm_id == ADMIN_ID:
        for i in admins:
            admins[i]['log_stat'] = False
        save_admins()
    else:
        bot.send_message(adm_id, empty_send_error_text, parse_mode='HTML')

@bot.message_handler(commands=['s_all'])
def show_all_logs(message):
    adm_id = message.from_user.id
    if adm_id == ADMIN_ID:
        for i in admins:
            admins[i]['log_stat'] = True
        save_admins()
    else:
        bot.send_message(adm_id, empty_send_error_text, parse_mode='HTML')

@bot.message_handler(commands=['new_adm'])
def add_new_admin(message):
    adm_id = message.from_user.id
    if adm_id == ADMIN_ID:
        if len(message.text.split()) == 3:
            try:
                new_adm_id = int(message.text.split()[1])
                smile = message.text.split()[2]
                new_admin(new_adm_id, smile)
                bot.send_message(ADMIN_ID, 'done')
            except:
                bot.send_message(ADMIN_ID, 'error')
        else:
            bot.send_message(ADMIN_ID, 'error')
    else:
        bot.send_message(message.from_user.id, empty_send_error_text, parse_mode='HTML')


@bot.message_handler(commands=['del_adm'])
def del_admin(message):
    adm_id = message.from_user.id
    if adm_id == ADMIN_ID:
        if len(message.text.split()) == 2:
            try:
                del_adm_id = int(message.text.split()[1])
                admins.pop(del_adm_id)
                save_admins()
                bot.send_message(ADMIN_ID, 'done')
            except:
                bot.send_message(ADMIN_ID, 'error')
        else:
            bot.send_message(ADMIN_ID, 'error')
    else:
        bot.send_message(message.from_user.id, empty_send_error_text, parse_mode='HTML')


@bot.message_handler(commands=['get_adm'])
def get_adm(message):
    if message.from_user.id == ADMIN_ID:

        for i in admins:
            arr = admins[i]
            user_line = (
            f"<code>{i}</code>: {arr['smile']}\n\n"
            f"<b>Mask:</b>\n"
            f"<i>ID</i>: <code>{arr['mask']['id']}</code>\n"
            f"<i>Username</i>: <code>{arr['mask']['username']}</code>\n"
            f"<i>First_name</i>: <code>{arr['mask']['first_name']}</code>\n"
            f"<i>Last_name</i>: <code>{arr['mask']['last_name']}</code>\n\n"
            f"<i>log stat</i>: <code>{arr['log_stat']}</code>"
            )
            bot.send_message(ADMIN_ID, user_line, parse_mode='HTML')
    else:
        bot.send_message(message.from_user.id, empty_send_error_text, parse_mode='HTML')


@bot.message_handler(commands=['smile'])
def smile(message):
    adm_id = message.from_user.id
    if adm_id in admins:
        if len(message.text.split()) == 2:
            if message.text.split()[1] !=  admins[ADMIN_ID]['smile']:
                admins[adm_id]['smile'] = message.text.split()[1]
                save_admins()
                bot.send_message(adm_id, 'Done')
            else:
                bot.send_message(adm_id, 'error')
        elif len(message.text.split()) == 3 and adm_id == ADMIN_ID:
            try:
                user_id = int(message.text.split()[1])
                admins[user_id]['smile'] = message.text.split()[2]
                save_admins()
                bot.send_message(adm_id, 'Done')
            except:
                bot.send_message(adm_id, 'error')

        else:
            bot.send_message(adm_id, 'error')
        
        if adm_id != ADMIN_ID:
            main_admin_log(f"{adm_id} - {message.text}")
    else:
        bot.send_message(message.from_user.id, empty_send_error_text, parse_mode='HTML')

@bot.message_handler(commands=['del_code'])
def del_code(message):
    adm_id = message.from_user.id
    if adm_id == ADMIN_ID:
        if len(message.text.split()) == 2:
            try:
                code_to_del_id = int(message.text.split()[1])
                for k, v in codes.items():
                    if v == code_to_del_id:
                        codes.pop(k)
                        save_codes()
                        break
                bot.send_message(ADMIN_ID, 'done')
            except:
                bot.send_message(ADMIN_ID, 'error')
        else:
            bot.send_message(ADMIN_ID, 'error')
    else:
        bot.send_message(message.from_user.id, empty_send_error_text, parse_mode='HTML')


@bot.message_handler(commands=['check_act'])
def check_act(message):
    adm_id = message.from_user.id
    if adm_id in admins:
        if len(message.text.split()) == 2:
            bot.send_message(adm_id, 'Ожидайте')
            try:
                user_id = int(message.text.split()[1])
                bot.send_chat_action(user_id, 'typing')
                bot.send_message(adm_id, 'Разблокирован')
            except ApiTelegramException as e:
                if e.error_code == 403:
                    bot.send_message(adm_id, 'Заблокирован')
                elif e.error_code == 400:
                    bot.send_message(adm_id, f'Пользователь никогда не общался с ботом.')
            except:
                bot.send_message(adm_id, 'error')
        else:
            bot.send_message(adm_id, 'error\n\n/adm')
        
        if adm_id != ADMIN_ID:
            main_admin_log(f"{adm_id} - {message.text}")
    else:
        bot.send_message(message.from_user.id, empty_send_error_text, parse_mode='HTML')

@bot.message_handler(commands=['check_all_act'])
def check_all_act(message):
    if message.from_user.id == ADMIN_ID:
        main_admin_log('loading...')
        colvo = 0
        colvo_block = 0
        colvo_unknown = 0
        for i in users:
            try:
                bot.send_chat_action(i, 'typing')
                colvo += 1
            except ApiTelegramException as e:
                if e.error_code == 403:
                    colvo_block += 1
                elif e.error_code == 400:
                    colvo_unknown += 1
                else:
                    pass
            except:
                bot.send_message(ADMIN_ID, 'error')  
        main_admin_log(colvo) 
        main_admin_log(colvo_block) 
        main_admin_log(colvo_unknown) 
        main_admin_log(len(users)) 
    else:
        bot.send_message(message.from_user.id, empty_send_error_text, parse_mode='HTML')


@bot.message_handler(commands=['history'])
def get_history(message):
    if message.from_user.id == ADMIN_ID:
        if len(message.text.split()) == 1:

            all_messages = []

            for sender_id, messages in history.items():
                for msg in messages:
                    receiver_id, text, date = msg
                    all_messages.append({
                        'date': date,
                        'sender': sender_id,
                        'receiver': receiver_id,
                        'text': text
                    })


            all_messages.sort(key=lambda x: x['date'])

            output_text = ""
            for m in all_messages:
                line = f"{m['date']}\n<code>{m['sender']}</code> - <code>{m['receiver']}</code>\n<i>{m['text']}</i>\n\n"
                
                if len(output_text) + len(line) > MAX_LENGTH:
                    main_admin_log(output_text)
                    output_text = line
                else:
                    output_text += line

            if output_text:
                main_admin_log(output_text)


        elif len(message.text.split()) == 2:
            try:
                user_id = int(message.text.split()[1])

                if user_id in history:

                    current_message = ""

                    for i in history[user_id]:
                        
                        user_line = (
                            f"({i[2]})--><code>{i[0]}</code>:  {i[1]}\n"
                        )

                        
                        if len(current_message) + len(user_line) > MAX_LENGTH:
                            
                            main_admin_log(current_message)
                            current_message = user_line  
                        else:
                            current_message += user_line

                    
                    if current_message:
                        main_admin_log(current_message)
                else:
                    main_admin_log('Not mentioned')




            except:
                main_admin_log('error')
        else:
                main_admin_log('error')
    else:
        bot.send_message(message.from_user.id, empty_send_error_text, parse_mode='HTML')


@bot.message_handler(commands=['update_users'])
def update_users(message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        load_users()
        main_admin_log('done')
    else:
        bot.send_message(message.from_user.id, empty_send_error_text, parse_mode='HTML')

@bot.message_handler(commands=['update_codes'])
def update_codes(message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        load_codes()
        main_admin_log('done')
    else:
        bot.send_message(message.from_user.id, empty_send_error_text, parse_mode='HTML')

@bot.message_handler(commands=['add_user'])
def add_to_users(message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        if len(message.text.split()) == 2:
            try:
                new_user_id = int(message.text.split()[1])
                add_user(new_user_id, 'None', 'None', 'None', datetime.fromtimestamp(message.date).strftime("%d.%m.%Y %H:%M"))
                main_admin_log('done')
            except:
                main_admin_log('err')
        elif len(message.text.split()) == 3:
            try:
                new_user_id = int(message.text.split()[1])
                new_user_name = message.text.split()[2]
                add_user(new_user_id, new_user_name, 'None', 'None', datetime.fromtimestamp(message.date).strftime("%d.%m.%Y %H:%M"))
                main_admin_log('done')
            except:
                main_admin_log('err')   
        else:
            main_admin_log('err')
    else:
        bot.send_message(message.from_user.id, empty_send_error_text, parse_mode='HTML')

@bot.message_handler(commands=['del_user'])
def del_from_users(message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        try:
            del_user_id = int(message.text.split()[1])
            if del_user_id in users:
                users.pop(del_user_id)
                save_users()
                main_admin_log('done')
            else:
                main_admin_log('not found')
        except:
            main_adm_help('err')


admins_help = """
<blockquote><b>ANON V4.1 by ABCtv</b></blockquote>

Ваш смайлик - {}

<b>Список пользователей:</b>
<blockquote>/get</blockquote>

<b>Информация об отдельном пользователе:</b>
<blockquote>/get <u>ID-пользователя</u></blockquote>

<b>Список ссылок:</b>
<blockquote>/codes</blockquote>

<b>Узнать ID человека по его коду:</b>
<blockquote>/codes <u>sHr5t</u></blockquote>

<b>Сгенерировать новую ссылку:</b>
<blockquote>/new <u>ID-Пользователя</u></blockquote>

<code>>>></code>

<b>Посмотреть данные своей маски:</b>
<blockquote>/change_mask</blockquote>

<b>Замаскироваться под пользователя:</b>
<blockquote>/change_mask <u>ID-Пользователя</u></blockquote>

<b>Кастомная маскировка (USERNAME без собаки!):</b>
<b>В указанном порядке; First_name и ID обязательно; Остальные можно - None</b>
<blockquote>/change_mask <u>ID</u> <u>USERNAME</u> <u>FIRST_NAME</u> <u>LAST_NAME</u></blockquote>

<b>Сбросить маску:</b>
<blockquote>/reset_mask</blockquote>

<b>Написать используя маскировку:</b>
<blockquote>/start_mask <u>ID-пользователя</u></blockquote>
‼️После отправки не использовать кнокпу <b>\"написать еще\"</b>, иначе сообщение улетит без маскировки‼️
‼️Каждое новое замаскировонное сообщение отправлять отдельной командой‼️

<code>>>></code>

<b>Установить смайл:</b>
<blockquote>/smile <u>EMODJI</u></blockquote>

<code>>>></code>

<b>Проверить заблокировал ли пользователь бота:</b>
<blockquote>/check_act <u>ID-пользователя</u></blockquote>

<code>>>></code>

<b>Скрыть админские сообщения (например чтобы доказать кому нибудь что админы не видят чужие сообщение):</b>
<blockquote>/h</blockquote>

<b>Вернуть админские сообщения обратно:</b>
<blockquote>/s</blockquote>
"""

main_adm_help = """
<b>ANON V4.1</b>

/ping

/new_adm id smile
/del_adm id
/get_adm

/smile id smile

/del_code id
/del_user id

/check_all_act

/history id

/h_all
/s_all

/update_users
/update_codes

/add_user id username

/show_active_states
"""

@bot.message_handler(commands=['adm'])
def get_adm_help(message):
    adm_id = message.from_user.id
    if adm_id in admins:
        bot.send_message(adm_id, admins_help.format(admins[adm_id]['smile']), parse_mode="HTML")
        main_admin_log(f"{adm_id} checks adm")
    if adm_id == ADMIN_ID:
        main_admin_log(main_adm_help)



