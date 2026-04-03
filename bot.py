import telebot
from telebot import types

TOKEN = "8628975374:AAHZQQcMea7QPY9VSmnMFPYt_5F6Kev7pKU"
ADMIN_ID = 5613451219

bot = telebot.TeleBot(TOKEN, threaded=True)

# عرض يظهر أول ما العميل يعمل /start
@bot.message_handler(commands=['start'])
def start(msg):
    chat_id = msg.chat.id

    offer_text = """⚡️ وفر في تجديد باقة فليكس

📱 لو على فليكس 300  
📶 استمتع بـ 21000 فليكس  

💰 بسعر 300 جنيه فقط  
📉 بدل 450 جنيه  

⚠️ التفعيل على خطوط معينة فقط  
📩 ابعتلنا وهنقولك في ثواني ينفع ولا لا"""

    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton("✅ موافق على العرض", callback_data="yes")
    btn2 = types.InlineKeyboardButton("❌ مش مهتم", callback_data="no")

    markup.add(btn1)
    markup.add(btn2)

    bot.send_message(chat_id, offer_text, reply_markup=markup)

# التعامل مع الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id

    if call.data == "yes":
        bot.send_message(
            chat_id,
            "🔥 تمام اختيار ممتاز\n\n"
            "📞 للتفعيل السريع تواصل معنا على واتساب:\n"
            "https://wa.me/201227115782\n\n"
            "⚡️ ابعت الرسالة دي:\n"
            "عايز عرض 21000 فليكس\n\n"
            "🚀 وسيتم التفعيل فورًا"
        )

    elif call.data == "no":
        bot.send_message(
            chat_id,
            "🙏 تمام\n"
            "لو حبيت تعرف أحدث العروض ابعتلنا في أي وقت 💙"
        )

    bot.answer_callback_query(call.id)

# تشغيل البوت
bot.infinity_polling(none_stop=True, interval=0)