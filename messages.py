from settings import *


new_anon_text = """
{} <b>У тебя новое сообщение!</b>

<blockquote>{}</blockquote>

↩️ <i>Свайпни для ответа.</i>
"""

error_blocked_text = """
⚠️ <b>Сообщение не доставлено</b>

Скорее всего, получатель <b>заблокировал бота</b> или ограничил возможность получения сообщений.

Попробуйте связаться с пользователем другим способом или отправьте сообщение позже.

Если ничего не помогает напишите в нашу поддержку - /help
"""



def get_abuse_button_markup():
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text="🚮 Пожаловаться", callback_data=f"abuse")
    markup.add(btn)
    return markup

#----------------------------------------------------

def get_write_again_button_markup(code):
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text="✍️ Написать еще", callback_data=f"start:{code}")
    markup.add(btn)
    return markup

success_anon_text = "Сообщение отправлено, ожидайте ответ!"

#----------------------------------------------------

reply_msgs = {}

def load_reply_msgs():
    with open(reply_msgs_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        reply_msgs.clear()
        reply_msgs.update({int(k): v for k, v in data.items()})

def save_reply_msgs():
    with open(reply_msgs_file_path, 'w', encoding='utf-8') as file:
        json.dump(reply_msgs, file, indent=4, ensure_ascii=False)

def new_reply_msg(banner_id, user_id):

    if banner_id in reply_msgs:
        reply_msgs[banner_id] = user_id
        save_reply_msgs()
        return

    if len(reply_msgs) >= reply_msgs_limit:
        
        first_key = next(iter(reply_msgs)) 
        del reply_msgs[first_key]
    
    
    reply_msgs[banner_id] = user_id
    save_reply_msgs()


reply_success_text = """✅ <b>Ответ успешно отправлен</b>"""

#---------------

empty_send_error_text = """
❌ <b>Сообщение не доставлено</b>

Похоже, вы не перешли по активной ссылке получателя.

<b>Чтобы отправить сообщение:</b>
1. Нажмите на персональную ссылку нужного человека.
2. Дождитесь уведомления 🚀 <code>Напишите сюда всё, что хотите передать...</code>
3. 🖊 <b>Только после этого</b> отправляйте свое сообщение.

<i>Попробуйте перейти по ссылке еще раз!</i>
"""

#----------------------------------

dox_text = """
Новое <b>"Анонимное"</b> сообщение от:

<i>Username:</i> @{}
<i>First_name:</i> <b>{}</b>
<i>Last_name:</i> <b>{}</b>
<i>ID:</i> <code>{}</code>
<i>Is premium?:</i> <b>{}</b>
<i>Language code:</i> <b>{}</b>
<i>Date:</i> <b>{}</b>

tg://user?id={}
<i>👆 Ссылка сработает только если
вы до этого как то <b>контактировали</b> с этим человеком
(Подписчик, общий чат, личный чат и тд)</i>

<blockquote>ANON V4.1
made by ABCtv
wardentrey3@gmail.com
</blockquote>
"""

