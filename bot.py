import telebot
from telebot import types

TOKEN = "8609961217:AAFCpQIoLkwGmaaBvo6iXWFo8MWRqTpNYmA"
ADMIN_ID = 5613451219

bot = telebot.TeleBot(TOKEN)

WHATSAPP = "https://wa.me/201227115782"
CASH_NUMBER = "01024929685"

offers = {
    "60": {"text": "🔥 60 شدّة", "price": "55"},
    "325": {"text": "⭐ 325 شدّة", "price": "230"},
    "660": {"text": "💎 660 شدّة", "price": "450"},
    "1800": {"text": "🚀 1800 شدّة", "price": "1150"},
    "3850": {"text": "👑 3850 شدّة", "price": "2250"},
    "8100": {"text": "🔥🔥 8100 شدّة", "price": "4300"}
}

user_data = {}

# 🔥 القائمة الرئيسية
@bot.message_handler(commands=['start'])
def main_menu(msg):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎮 شحن شدات", callback_data="shop"))

    bot.send_message(msg.chat.id, "🔥 أهلاً بيك\n\nاختر من القائمة:", reply_markup=markup)

# 📦 قائمة الباقات
@bot.callback_query_handler(func=lambda call: call.data == "shop")
def shop_menu(call):
    markup = types.InlineKeyboardMarkup()

    for key, value in offers.items():
        markup.add(types.InlineKeyboardButton(
            f"{value['text']} - {value['price']} ج",
            callback_data=f"offer_{key}"
        ))

    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="main"))

    bot.edit_message_text(
        "🎯 اختر الباقة:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

# 🎯 اختيار الباقة → قائمة إدخال البيانات
@bot.callback_query_handler(func=lambda call: call.data.startswith("offer_"))
def choose_offer(call):
    offer_id = call.data.split("_")[1]
    user_data[call.message.chat.id] = {"offer": offer_id}

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✍️ إدخال البيانات", callback_data="enter_data"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="shop"))

    bot.send_message(call.message.chat.id, "✅ تم اختيار الباقة", reply_markup=markup)

# 🧾 إدخال البيانات
@bot.callback_query_handler(func=lambda call: call.data == "enter_data")
def enter_data(call):
    bot.send_message(call.message.chat.id, "🎮 اكتب ID الحساب:")

# ID
@bot.message_handler(func=lambda m: m.chat.id in user_data and "id" not in user_data[m.chat.id])
def get_id(msg):
    user_data[msg.chat.id]["id"] = msg.text
    bot.send_message(msg.chat.id, "👤 اكتب اسم الحساب:")

# الاسم → قائمة المراجعة
@bot.message_handler(func=lambda m: m.chat.id in user_data and "name" not in user_data[m.chat.id])
def get_name(msg):
    user_data[msg.chat.id]["name"] = msg.text

    data = user_data[msg.chat.id]
    offer = offers[data["offer"]]

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 الدفع", callback_data="payment"))
    markup.add(types.InlineKeyboardButton("🔄 تعديل", callback_data="enter_data"))

    bot.send_message(
        msg.chat.id,
        f"📦 طلبك:\n{offer['text']} - {offer['price']} جنيه",
        reply_markup=markup
    )

# 💳 قائمة الدفع
@bot.callback_query_handler(func=lambda call: call.data == "payment")
def payment_menu(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💰 فودافون كاش", callback_data="cash"))
    markup.add(types.InlineKeyboardButton("📲 واتساب", callback_data="whatsapp"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="shop"))

    bot.edit_message_text(
        "💳 اختر طريقة الدفع:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

# 💰 الكاش (قائمة لوحدها)
@bot.callback_query_handler(func=lambda call: call.data == "cash")
def cash_menu(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📲 متابعة على واتساب", callback_data="whatsapp"))

    bot.send_message(
        call.message.chat.id,
        f"💰 حول على الرقم:\n{CASH_NUMBER}\n\n📸 بعد التحويل خد سكرين",
        reply_markup=markup
    )

# 📲 الواتساب (قائمة لوحدها)
@bot.callback_query_handler(func=lambda call: call.data == "whatsapp")
def whatsapp_menu(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📲 فتح واتساب", url=WHATSAPP))

    bot.send_message(
        call.message.chat.id,
        "📩 ابعت على الواتساب:\n"
        "- سكرين التحويل\n"
        "- رقم المحفظة",
        reply_markup=markup
    )

# 🔙 رجوع للرئيسية
@bot.callback_query_handler(func=lambda call: call.data == "main")
def back_main(call):
    main_menu(call.message)

bot.infinity_polling()
