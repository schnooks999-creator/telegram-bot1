import telebot
from telebot import types

TOKEN = "8609961217:AAFCpQIoLkwGmaaBvo6iXWFo8MWRqTpNYmA"
ADMIN_ID = 5613451219

bot = telebot.TeleBot(TOKEN)

WHATSAPP = "https://wa.me/201227115782"
CASH_NUMBER = "01024929685"

offers = {
    "60": {"text": "🎮 60 شدّة", "price": "55"},
    "325": {"text": "🎮 325 شدّة", "price": "230"},
    "660": {"text": "🎮 660 شدّة", "price": "450"},
    "1800": {"text": "🎮 1800 شدّة", "price": "1150"},
    "3850": {"text": "🎮 3850 شدّة", "price": "2250"},
    "8100": {"text": "🎮 8100 شدّة", "price": "4300"}
}

user_data = {}

# Start
@bot.message_handler(commands=['start'])
def start(msg):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 ابدأ الشحن", callback_data="start"))

    bot.send_message(
        msg.chat.id,
        "🔥 *مرحبًا بك في خدمة شحن شدات ببجي* 🔥\n\n"
        "💎 خدمة سريعة وآمنة\n"
        "🛡️ ضمان على كل عملية\n\n"
        "👇 اضغط وابدأ",
        parse_mode="Markdown",
        reply_markup=markup
    )

# عرض الباقات
@bot.callback_query_handler(func=lambda call: call.data == "start")
def show(call):
    markup = types.InlineKeyboardMarkup()

    for key, value in offers.items():
        markup.add(types.InlineKeyboardButton(
            f"{value['text']} - {value['price']} جنيه",
            callback_data=key
        ))

    markup.add(types.InlineKeyboardButton("❌ إلغاء", callback_data="cancel"))

    bot.edit_message_text(
        "🎯 *اختر الباقة المناسبة:*",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown",
        reply_markup=markup
    )

# اختيار
@bot.callback_query_handler(func=lambda call: call.data in offers)
def choose(call):
    user_data[call.message.chat.id] = {"offer": call.data}

    bot.send_message(
        call.message.chat.id,
        "🎮 *الخطوة 1:*\nأرسل ID الحساب:",
        parse_mode="Markdown"
    )

# ID
@bot.message_handler(func=lambda m: m.chat.id in user_data and "id" not in user_data[m.chat.id])
def get_id(msg):
    user_data[msg.chat.id]["id"] = msg.text.strip()

    bot.send_message(
        msg.chat.id,
        "👤 *الخطوة 2:*\nأرسل اسم الحساب:",
        parse_mode="Markdown"
    )

# الاسم
@bot.message_handler(func=lambda m: m.chat.id in user_data and "name" not in user_data[m.chat.id])
def get_name(msg):
    user_data[msg.chat.id]["name"] = msg.text.strip()

    data = user_data[msg.chat.id]
    offer = offers[data["offer"]]

    text = f"""
📦 *تفاصيل الطلب*

━━━━━━━━━━━━━━━
🎮 الباقة: {offer['text']}
💰 السعر: {offer['price']} جنيه

🆔 ID: {data['id']}
👤 الاسم: {data['name']}
━━━━━━━━━━━━━━━

💳 *طريقة الدفع*

📱 فودافون كاش:
{CASH_NUMBER}

💵 قم بتحويل:
*{offer['price']} جنيه*

━━━━━━━━━━━━━━━

📲 *بعد التحويل*

📸 التقط سكرين لعملية التحويل

📩 أرسل على الواتساب:
• سكرين التحويل  
• رقم المحفظة  

📲 رابط التواصل:
{WHATSAPP}

━━━━━━━━━━━━━━━

🚀 *سيتم تنفيذ الطلب خلال دقائق*
"""

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📲 تواصل واتساب الآن", url=WHATSAPP))
    markup.add(types.InlineKeyboardButton("🔄 طلب جديد", callback_data="start"))

    bot.send_message(msg.chat.id, text, parse_mode="Markdown", reply_markup=markup)

    bot.send_message(
        ADMIN_ID,
        f"""
📥 طلب جديد 🔥

{offer['text']}
💰 {offer['price']} جنيه

ID: {data['id']}
Name: {data['name']}
"""
    )

    user_data.pop(msg.chat.id)

# إلغاء
@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel(call):
    user_data.pop(call.message.chat.id, None)
    bot.send_message(call.message.chat.id, "❌ تم إلغاء العملية")

bot.infinity_polling()
