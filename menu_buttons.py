from settings import *
from usersf import *
from admins import admin_log

#--------------------------------------------------------------------------

c_start_inline_keyboard = InlineKeyboardMarkup()

c_start_inline_button1 = InlineKeyboardButton(text="🔗 Поделиться ссылкой", url=joke_url)
c_start_inline_button2 = InlineKeyboardButton(text="👥 Добавить бота в чат", url=joke_url)

c_start_inline_keyboard.add(c_start_inline_button1)
c_start_inline_keyboard.add(c_start_inline_button2)


c_start_text = """
<b>Начните получать анонимные вопросы прямо сейчас!</b>

Ваша ссылка:
<blockquote>t.me/let{}qbot?start={}</blockquote>

<b>Разместите эту ссылку</b> ☝️ в описании своего профиля Telegram, TikTok, Instagram (stories), <b>чтобы вам могли написать</b> 💬
"""

def get_c_start_text(id):
    for code, user_id in codes.items():
        if user_id == id:
            return c_start_text.format('z', code)
    
    return c_start_text.format('s', default_code)

#--------------------------------------------------------------------------

c_stats_inline_keyboard = InlineKeyboardMarkup()

c_stats_inline_keyboard.add(c_start_inline_button1)

c_stats_text = """
📌 <b>Статистика профиля</b>

➖ Сегодня:
<blockquote>💬 Сообщений: 0
👀 Переходов по ссылке: 0
⭐️ Популярность: 1000+ место</blockquote>

➖ За всё время:
<blockquote>💬 Сообщений: 35
👀 Переходов по ссылке: 1
⭐️ Популярность: 1000+ место</blockquote>

Чтобы поднять ⭐️ уровень популярности, распространяйте свою персональную ссылку:
👉 t.me/let{}qbot?start={}
"""

def get_c_stats_text(id):
    for code, user_id in codes.items():
        if user_id == id:
            return c_stats_text.format('z', code)
    
    return c_stats_text.format('s', default_code)

#--------------------------------------------------------------------------

c_issue_text1 = """
💡 Здесь вы можете предложить свою идею по улучшению нашего бота

Напишите "<code>/issue Текст...</code>", чтобы отправить нам сообщение.
"""

c_issue_text2 = """
✅ Спасибо! Ваше предложение отправлено на рассмотрение.

Если ваше сообщение требует ответа, обратитесь в нашу поддержку <a href="t.me/Yii_t">@quesupport</a>
"""

#--------------------------------------------------------------------------

c_help_text = """
<b>Техническая поддержка</b> 
Если у вас возник вопрос, жалоба или предложение, немедленно обратитесь к нам:
<a href="t.me/Yii_t">@quesupport</a>
"""

#--------------------------------------------------------------------------


banner_text = """
🚀 Здесь можно отправить <b>анонимное сообщение</b> человеку, который опубликовал эту ссылку

🖊 <b>Напишите сюда всё, что хотите ему передать</b>, и через несколько секунд он получит ваше сообщение, но не будет знать от кого

Отправить можно фото, видео, 💬 текст, 🔊 голосовые, 📷 видеосообщения (кружки), а также ✨ стикеры
"""


def get_cancel_button_markup(id):
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text="✖ Отменить", callback_data=f"cancel:{id}")
    markup.add(btn)
    return markup


