from settings import *
from usersf import *
from menu_buttons import *
from admins import *
from free_handler_logics import *

@bot.middleware_handler(update_types=['message'])
def simple_mw(bot, message):

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    if (user_id not in users):
        add_user(user_id, username, first_name, last_name, datetime.fromtimestamp(message.date).strftime("%d.%m.%Y %H:%M"))
        add_new_user_in_states(user_id)
        log_line = f"NEW USER <code>{username}</code> <code>{user_id}</code>\n\n<code>/get {user_id}</code>"
        admin_log(log_line)
    else:
        check_user(message)

@bot.message_handler(commands=['start'])
def c_start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    reset_state(user_id)

    if len(message.text.split()) == 2:
        code = message.text.split()[1]
        if code in codes:
            change_state(user_id, 1)
            change_state_last_code(user_id, code)
            banner_id = bot.send_message(user_id, banner_text, parse_mode='HTML', reply_markup=get_cancel_button_markup(user_id)).message_id
            change_state_banner_id(user_id, banner_id)
            admin_log(f"<b>{username}</b> (<code>{user_id}</code>) Нажал старт для <b>{users[codes[code]]['username']}</b> (<code>{codes[code]}</code>)")
        else:
            bot.send_message(user_id, get_c_start_text(user_id), parse_mode='HTML', reply_markup=c_start_inline_keyboard, disable_web_page_preview=True)
            main_admin_log(f"<code>{user_id}</code> - {message.text}")
    else:
        bot.send_message(user_id, get_c_start_text(user_id), parse_mode='HTML', reply_markup=c_start_inline_keyboard, disable_web_page_preview=True)



#-----------------------------------------------



@bot.message_handler(commands=['stats'])
def c_stats(message):
    user_id = message.from_user.id

    reset_state(user_id)

    bot.send_message(user_id, get_c_stats_text(user_id), parse_mode='HTML', reply_markup=c_stats_inline_keyboard, disable_web_page_preview=True)



#-----------------------------------------------




@bot.message_handler(commands=['issue'])
def c_issue(message):
    
    user_id = message.from_user.id

    reset_state(user_id)

    if len(message.text.split()) > 1:
        bot.send_message(user_id, c_issue_text2, parse_mode='HTML', disable_web_page_preview=True)
        main_admin_log(f"<code>{user_id}</code> ISSUE: \n<blockquote>{message.text[7:]}</blockquote>")
    else:
        bot.send_message(user_id, c_issue_text1, parse_mode='HTML')



#-----------------------------------------------



@bot.message_handler(commands=['help'])
def c_help(message):

    user_id = message.from_user.id

    reset_state(user_id)

    bot.send_message(user_id, c_help_text, parse_mode='HTML', disable_web_page_preview=True)



#-----------------------------------------------


@bot.callback_query_handler(func=lambda call: call.data.startswith('cancel:'))
def cancel_button(call):
    bot.answer_callback_query(call.id)
    action, target_id = call.data.split(':')
    target_id = int(target_id)

    if states[target_id]['banner_id'] != None:
        
        reset_state(target_id)
        
        bot.send_message(target_id, get_c_start_text(target_id), parse_mode='HTML', reply_markup=c_start_inline_keyboard, disable_web_page_preview=True)



#-----------------------------------------------


@bot.callback_query_handler(func=lambda call: call.data.startswith('start:'))
def write_again_button(call):
    bot.answer_callback_query(call.id)
    action, code = call.data.split(':')
    user_id = call.from_user.id
    

    reset_state(user_id)

    change_state(user_id, 1)
    change_state_last_code(user_id, code)
    banner_id = bot.send_message(user_id, banner_text, parse_mode='HTML', reply_markup=get_cancel_button_markup(user_id)).message_id
    change_state_banner_id(user_id, banner_id)

    admin_log(f"<b>{users[user_id]['username']}</b> (<code>{user_id}</code>) Нажал старт для <b>{users[codes[code]]['username']}</b> (<code>{codes[code]}</code>)")




#-----------------------------------------------



@bot.callback_query_handler(func=lambda call: call.data == "abuse")
def handle_abuse(call):

    bot.answer_callback_query(
        callback_query_id=call.id, 
        text=f"Спасибо. Ваша жалоба отправлена на рассмотрение", 
        show_alert=True
    )

    admin_log(f"<code>{call.message.chat.id}</code> press abuse")

#-----------------------------------------------

@bot.my_chat_member_handler()
def handle_chat_member_update(update):
    status = update.new_chat_member.status
    if status == "kicked":
        for i in admins:
            try:
                bot.send_message(i, f"Пользователь {update.from_user.id} заблокировал бота")
            except:
                pass
    elif status == "member":
        for i in admins:
            try:
                bot.send_message(i, f"Пользователь {update.from_user.id} разблокировал бота")
            except:
                pass

#-----------------------------------------------


@bot.message_handler(content_types=['text', 'sticker', 'photo', 'video', 'animation', 'voice', 'video_note', 'document'])
def universal_handler(message):
    
    if message.reply_to_message:
        handler_reply_logic(message)
    else:
        free_handler_logic(message)

