from settings import *
from menu_buttons import *
from admins import *
from historyf import *

def free_handler_logic(message):
    user_id = message.from_user.id
    

    if states[user_id]['state'] == 1:
        reset_state(user_id, False)
        if message.content_type == 'text':
            handler_text_logic(message, user_id, codes[states[user_id]['last_code']], False)
            admin_log_text(message, user_id, codes[states[user_id]['last_code']])

            add_to_history(message.text, user_id, codes[states[user_id]['last_code']], datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))

        elif message.content_type in ['sticker', 'photo', 'video', 'animation', 'voice', 'video_note', 'document']:
            handler_media_logic(message, user_id, codes[states[user_id]['last_code']], False)
            admin_log_media(message, user_id, codes[states[user_id]['last_code']])

            add_to_history(message.content_type, user_id, codes[states[user_id]['last_code']], datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))

    elif states[user_id]['state'] == 2:
        reset_state(user_id, False)
        if message.content_type == 'text':
            handler_text_logic(message, user_id, codes[states[user_id]['last_code']], True)
        elif message.content_type in ['sticker', 'photo', 'video', 'animation', 'voice', 'video_note', 'document']:
            handler_media_logic(message, user_id, codes[states[user_id]['last_code']], True)
            
        
        
    else:
        reset_state(user_id, False)

        if user_id in admins:
            if message.content_type == 'text':
                for i in admins:
                    if i != user_id and admins[i]['log_stat']:
                        try:
                            bot.send_message(i, f"{admins[user_id]['smile']}: {message.text}", parse_mode='HTML', disable_web_page_preview=True)
                        except:
                            bot.send_message(ADMIN_ID, f'{i} block bot')
                bot.send_message(user_id, 'Отправлено')
            elif message.content_type in ['sticker', 'photo', 'video', 'animation', 'voice', 'video_note', 'document']:
                for i in admins:
                    if i != user_id and admins[i]['log_stat']:
                        try:
                            res = bot.copy_message(i, user_id, message.message_id).message_id
                            bot.send_message(i, f"{admins[user_id]['smile']}:", reply_to_message_id=res)
                        except:
                            bot.send_message(ADMIN_ID, f'{i} block bot')
                bot.send_message(user_id, 'Отправлено')                        
        else:       
            bot.send_message(user_id, empty_send_error_text, parse_mode='HTML')

            if message.content_type == 'text':
                admin_log(f"<b>Random</b> from {users[user_id]['username']} (<code>{user_id}</code>):\n\n<i>{message.text}</i>")
            elif message.content_type in ['sticker', 'photo', 'video', 'animation', 'voice', 'video_note', 'document']:
                for i in admins:
                        try:
                            if admins[i]['log_stat']:
                                res = bot.copy_message(i, user_id, message.message_id).message_id
                                bot.send_message(i, f"<b>Random</b> from {users[user_id]['username']} (<code>{user_id}</code>):", reply_to_message_id=res, parse_mode='HTML')
                        except:
                            pass
    


def handler_text_logic(message, from_user_id, to_user_id, is_mask):


    try:

        dt_object = datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S')

        swipe_id = bot.send_message(to_user_id, new_anon_text.format(random.choice(emotions), message.text), parse_mode='HTML', reply_markup=get_abuse_button_markup()).message_id
        
        if not is_mask:
            dox_username = users[from_user_id]['username']
            dox_first_name = users[from_user_id]['first_name']
            dox_last_name = users[from_user_id]['last_name']
            dox_from_user_id = from_user_id
            dox_is_prem = message.from_user.is_premium
            dox_lang_code = message.from_user.language_code
        else:
            dox_username = admins[from_user_id]['mask']['username']
            dox_first_name = admins[from_user_id]['mask']['first_name']
            dox_last_name = admins[from_user_id]['mask']['last_name']
            dox_from_user_id = admins[from_user_id]['mask']['id']
            dox_is_prem = 'None'
            dox_lang_code = 'Ru'

            bot.send_message(ADMIN_ID, f"<b>{from_user_id}</b> написал к <b>{users[to_user_id]['username']} ({to_user_id})</b> от лица ({dox_username}, {dox_from_user_id}, {dox_first_name}, {dox_last_name}) \n\n{message.text}", parse_mode='HTML')

        if dox_username.lower() == 'none':
            dox_username = 'Юзернейм отсутсвует'

        bot.send_message(to_user_id, 
                        dox_text.format(dox_username, dox_first_name,dox_last_name ,dox_from_user_id, dox_is_prem, dox_lang_code, dt_object, dox_from_user_id), 
                        parse_mode='html', reply_to_message_id=swipe_id)
        
        if not is_mask:
            bot.send_message(from_user_id, success_anon_text, reply_markup=get_write_again_button_markup(states[from_user_id]['last_code']))
            bot.send_message(from_user_id, get_c_start_text(from_user_id), parse_mode='HTML', reply_markup=c_start_inline_keyboard, disable_web_page_preview=True)
        else:
            bot.send_message(from_user_id, success_anon_text)


        new_reply_msg(swipe_id, from_user_id)

    except Exception as e:
        print(e)
        bot.send_message(from_user_id, error_blocked_text, parse_mode='HTML')
        
            

    

def handler_media_logic(message, from_user_id, to_user_id, is_mask):
    from_user_id = message.from_user.id
    
    
    try:

        dt_object = datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S')

        res = bot.copy_message(
            chat_id=to_user_id,
            from_chat_id=from_user_id,
            message_id=message.message_id,
            reply_markup=get_abuse_button_markup()
        )

        if not is_mask:
            dox_username = users[from_user_id]['username']
            dox_first_name = users[from_user_id]['first_name']
            dox_last_name = users[from_user_id]['last_name']
            dox_from_user_id = from_user_id
            dox_is_prem = message.from_user.is_premium
            dox_lang_code = message.from_user.language_code
        else:
            dox_username = admins[from_user_id]['mask']['username']
            dox_first_name = admins[from_user_id]['mask']['first_name']
            dox_last_name = admins[from_user_id]['mask']['last_name']
            dox_from_user_id = admins[from_user_id]['mask']['id']
            dox_is_prem = 'None'
            dox_lang_code = 'Ru'

        if dox_username.lower() == 'none':
                    dox_username = 'Юзернейм отсутсвует'

        bot.send_message(to_user_id, 
                         dox_text.format(dox_username,dox_first_name,dox_last_name ,dox_from_user_id, dox_is_prem, dox_lang_code, dt_object, dox_from_user_id), 
                         parse_mode='HTML', reply_to_message_id=res.message_id)
        

        if is_mask:
            res_adm = bot.copy_message(
            chat_id=ADMIN_ID,
            from_chat_id=from_user_id,
            message_id=message.message_id
            )
            bot.send_message(ADMIN_ID, f"<b>{from_user_id}</b> написал к <b>{users[to_user_id]['username']} ({to_user_id})</b> от лица ({dox_username}, {dox_from_user_id}, {dox_first_name}, {dox_last_name})", parse_mode='HTML', reply_to_message_id=res_adm.message_id)



        new_reply_msg(res.message_id, from_user_id)
        
        if not is_mask:
            bot.send_message(from_user_id, success_anon_text, reply_markup=get_write_again_button_markup(states[from_user_id]['last_code']))
            bot.send_message(from_user_id, get_c_start_text(from_user_id), parse_mode='HTML', reply_markup=c_start_inline_keyboard, disable_web_page_preview=True)
        else:
            bot.send_message(from_user_id, success_anon_text)


    except Exception as e:
        print(e)
        bot.send_message(from_user_id, error_blocked_text, parse_mode='HTML')













def handler_reply_logic(message):
    try:
        lox_id = reply_msgs[message.reply_to_message.message_id]
    except KeyError:
        bot.send_message(message.from_user.id, get_c_start_text(message.from_user.id), parse_mode='HTML', reply_markup=c_start_inline_keyboard, disable_web_page_preview=True)
        return

    
    my_code = "id" 
    for k, v in codes.items():
        if v == message.from_user.id:
            my_code = k
            break
    
    try:
        bot.copy_message(
            chat_id=lox_id, 
            from_chat_id=message.from_user.id, 
            message_id=message.message_id, 
            reply_markup=get_write_again_button_markup(my_code)
        )
        
        bot.send_message(message.from_user.id, reply_success_text, parse_mode='HTML')
        
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, error_blocked_text, parse_mode='HTML')


    if message.content_type == 'text':
        admin_log_text(message, message.from_user.id, lox_id)
        add_to_history(message.text, message.from_user.id, lox_id, datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))
    elif message.content_type in ['sticker', 'photo', 'video', 'animation', 'voice', 'video_note', 'document']:
        admin_log_media(message, message.from_user.id, lox_id)
        add_to_history(message.content_type, message.from_user.id, lox_id, datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))
                

