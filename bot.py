import telebot
from telebot import types

TOKEN = "8609961217:AAFCpQIoLkwGmaaBvo6iXWFo8MWRqTpNYmA"
ADMIN_ID = 5613451219

bot = telebot.TeleBot(TOKEN)

WHATSAPP = "201227115782"

offers = {
    "60": {"text": "🎮 60 شدّة", "price": "55"},
    "325": {"text": "🎮 325 شدّة", "price": "230"},
    "660": {"text": "🎮 660 شدّة", "price": "450"},
    "1800": {"text": "🎮 1800 شدّة", "price": "1150"},
    "3850": {"text": "🎮 3850 شدّة", "price": "2250"},
    "8100": {"text": "🎮 8100 شدّة", "price": "4300"}
}

user_data = {}

# 🔥 بداية البوت
@bot.message_handler(commands=['start'])
def start(msg):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 ابدأ الشحن", callback_data="start"))

    bot.send_message(
        msg.chat.id,
        "🔥 أهلاً بيك في شحن شدات ببجي 🔥\n\n"
        "⚡ شحن فوري\n💯 مضمون 100%\n\n"
        "👇 اضغط وابدأ",
        reply_markup=markup
    )

# 📦 عرض الباقات
@bot.callback_query_handler(func=lambda call: call.data == "start")
def show_offers(call):
    markup = types.InlineKeyboardMarkup()

    for key in offers:
        text = f"{offers[key]['text']} - {offers[key]['price']} جنيه"
        markup.add(types.InlineKeyboardButton(text, callback_data=key))

    bot.edit_message_text(
        "🎯 اختر الباقة المناسبة:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

# 🎯 اختيار الباقة
@bot.callback_query_handler(func=lambda call: call.data in offers)
def choose(call):
    user_data[call.message.chat.id] = {"offer": call.data}

    bot.send_message(call.message.chat.id, "🎮 ابعت ID ببجي:")

# 🎮 استقبال ID
@bot.message_handler(func=lambda m: m.chat.id in user_data and "id" not in user_data[m.chat.id])
def get_id(msg):
    user_data[msg.chat.id]["id"] = msg.text

    bot.send_message(msg.chat.id, "👤 ابعت اسم الحساب:")

# 👤 استقبال الاسم
@bot.message_handler(func=lambda m: m.chat.id in user_data and "name" not in user_data[m.chat.id])
def get_name(msg):
    user_data[msg.chat.id]["name"] = msg.text

    data = user_data[msg.chat.id]
    offer = offers[data["offer"]]

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ تأكيد الطلب", callback_data="confirm"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="start"))

    bot.send_message(
        msg.chat.id,
        f"📦 تفاصيل الطلب:\n\n"
        f"{offer['text']}\n"
        f"💰 السعر: {offer['price']} جنيه\n"
        f"🎮 ID: {data['id']}\n"
        f"👤 الاسم: {data['name']}\n\n"
        "👇 اضغط تأكيد لإكمال الطلب",
        reply_markup=markup
    )

# ✅ تأكيد الطلب
@bot.callback_query_handler(func=lambda call: call.data == "confirm")
def confirm(call):
    data = user_data.get(call.message.chat.id)
    offer = offers[data["offer"]]

    # 📩 ارسال الطلب ليك
    bot.send_message(
        ADMIN_ID,
        f"📩 طلب جديد 🔥\n\n"
        f"{offer['text']}\n"
        f"💰 {offer['price']} جنيه\n"
        f"🎮 ID: {data['id']}\n"
        f"👤 الاسم: {data['name']}"
    )

    # 📲 رسالة واتساب جاهزة
    text = f"عايز اشحن {offer['text']} - ID:{data['id']} - الاسم:{data['name']}"

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "📲 تواصل واتساب",
            url=f"https://wa.me/{WHATSAPP}?text={text}"
        )
    )

    bot.send_message(
        call.message.chat.id,
        f"💰 طريقة الدفع:\n\n"
        f"📲 فودافون كاش / أورنج كاش:\n01227115782\n\n"
        f"💵 حول {offer['price']} جنيه\n\n"
        "📸 بعد التحويل:\n"
        "ابعت سكرين على واتساب بنفس الرقم 👇",
        reply_markup=markup
    )

bot.infinity_polling()
