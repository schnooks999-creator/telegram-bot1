import telebot
from telebot import types

TOKEN = "8609961217:AAFCpQIoLkwGmaaBvo6iXWFo8MWRqTpNYmA"
ADMIN_ID = 5613451219

bot = telebot.TeleBot(TOKEN)

WHATSAPP = "https://wa.me/201227115782"
CASH = "01024929685"

offers = {
    "1": ("60 شدّة", "55"),
    "2": ("325 شدّة", "230"),
    "3": ("660 شدّة", "450"),
    "4": ("1800 شدّة", "1150"),
    "5": ("3850 شدّة", "2250"),
    "6": ("8100 شدّة", "4300")
}

user = {}

# البداية
@bot.message_handler(commands=['start'])
def start(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("شحن شدات", callback_data="shop"))
    bot.send_message(m.chat.id, "اختر الخدمة:", reply_markup=kb)

# قائمة الأسعار
@bot.callback_query_handler(func=lambda c: c.data == "shop")
def shop(c):
    kb = types.InlineKeyboardMarkup()
    for k, v in offers.items():
        kb.add(types.InlineKeyboardButton(f"{v[0]} - {v[1]} ج", callback_data=k))
    bot.edit_message_text("اختر الباقة:", c.message.chat.id, c.message.message_id, reply_markup=kb)

# اختيار باقة
@bot.callback_query_handler(func=lambda c: c.data in offers)
def choose(c):
    user[c.message.chat.id] = {"offer": c.data}
    bot.send_message(c.message.chat.id, "اكتب ID:")

# ID
@bot.message_handler(func=lambda m: m.chat.id in user and "id" not in user[m.chat.id])
def get_id(m):
    user[m.chat.id]["id"] = m.text
    bot.send_message(m.chat.id, "اكتب الاسم:")

# الاسم → قائمة الدفع
@bot.message_handler(func=lambda m: m.chat.id in user and "name" not in user[m.chat.id])
def get_name(m):
    user[m.chat.id]["name"] = m.text

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("الدفع", callback_data="pay"))

    bot.send_message(m.chat.id, "اضغط للدفع:", reply_markup=kb)

# قائمة الدفع
@bot.callback_query_handler(func=lambda c: c.data == "pay")
def pay(c):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("فودافون كاش", callback_data="cash"))
    kb.add(types.InlineKeyboardButton("واتساب", callback_data="wa"))

    bot.edit_message_text("اختار:", c.message.chat.id, c.message.message_id, reply_markup=kb)

# قائمة الكاش
@bot.callback_query_handler(func=lambda c: c.data == "cash")
def cash(c):
    bot.send_message(
        c.message.chat.id,
        f"""طريقة الدفع: فودافون كاش

رقم التحويل:
{CASH}

بعد التحويل مباشرة:
- ابعت صورة التحويل
- اكتب الرقم اللي تم التحويل منه
"""
    )

# قائمة الواتساب
@bot.callback_query_handler(func=lambda c: c.data == "wa")
def wa(c):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("فتح واتساب", url=WHATSAPP))

    bot.send_message(
        c.message.chat.id,
        f"""ابعت كل التفاصيل على واتساب لتأكيد الطلب:

{WHATSAPP}
""",
        reply_markup=kb
    )

bot.infinity_polling()
