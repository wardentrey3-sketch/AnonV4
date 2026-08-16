from settings import *
from handlers import *
from usersf import *
from messages import *
from admins import *




if __name__ == "__main__":

    load_users()
    load_codes()
    load_states()
    load_reply_msgs()
    load_admins()
    load_history()

    try:
        bot.send_message(ADMIN_ID, f"BOT START")
    except Exception as e:
        print('err start sms', e)

    print('ANON_V4.1: Bot start', datetime.now().time()) 
    bot.infinity_polling()