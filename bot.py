import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# 🔐 التوكن (حط التوكن الجديد هنا)
TOKEN = "7966652318:AAHyN7iJw3HYX-eeTKJ2zqMZMeZQKmnj_0Y"

# 🧑‍💼 الايدي بتاعك
ADMIN_ID = 5613451219

# 📱 رقم واتساب
WHATSAPP_NUMBER = "201227115782"

user_data_store = {}

packages = {
    "1": "📶 40 جيجا | 1500 دقيقة | 400 جنيه",
    "2": "📶 50 جيجا | 1500 دقيقة | 470 جنيه",
    "3": "📶 60 جيجا | 1500 دقيقة | 540 جنيه",
    "4": "📶 70 جيجا | 1500 دقيقة | 600 جنيه",
}

# 💾 حفظ الطلبات
def save_order(data):
    try:
        with open("orders.json", "r") as file:
            orders = json.load(file)
    except:
        orders = []

    orders.append(data)

    with open("orders.json", "w") as file:
        json.dump(orders, file, indent=4)

# 🚀 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(packages["1"], callback_data="1")],
        [InlineKeyboardButton(packages["2"], callback_data="2")],
        [InlineKeyboardButton(packages["3"], callback_data="3")],
        [InlineKeyboardButton(packages["4"], callback_data="4")],
    ]

    await update.message.reply_text(
        "🔥 احجز باقتك الآن 🔥\n\n"
        "📅 التفعيل يوم 16\n"
        "⏳ المدة 28 يوم\n\n"
        "اختار الباقة 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 🎯 اختيار الباقة
async def choose_package(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_data_store[user_id] = {"package": packages[query.data]}

    await query.message.reply_text("👤 اكتب اسمك")
    context.user_data["step"] = "name"

# ✍️ إدخال البيانات
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_data_store:
        user_data_store[user_id] = {}

    if context.user_data.get("step") == "name":
        user_data_store[user_id]["name"] = text
        await update.message.reply_text("📱 اكتب رقمك")
        context.user_data["step"] = "phone"

    elif context.user_data.get("step") == "phone":
        user_data_store[user_id]["phone"] = text

        data = user_data_store[user_id]

        order = {
            "name": data.get("name", ""),
            "phone": data.get("phone", ""),
            "package": data.get("package", ""),
            "status": "جديد",
            "user_id": str(user_id),
            "date": str(datetime.now())
        }

        save_order(order)

        # إرسال للأدمن
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"""📥 طلب جديد

👤 {data['name']}
📱 {data['phone']}
{data['package']}"""
            )
        except:
            pass

        # أزرار
        whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}"
        keyboard = [
            [InlineKeyboardButton("📩 تواصل واتساب", url=whatsapp_url)],
            [InlineKeyboardButton("✔️ تم الدفع", callback_data="paid")]
        ]

        await update.message.reply_text(
            "✅ تم تسجيل طلبك بنجاح\n\n"
            "💵 حول الكاش على الرقم:\n01024929685\n\n"
            "📸 ابعت صورة التحويل على واتساب\n\n"
            "✔️ وبعدها اضغط تم الدفع",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        context.user_data.clear()

# 💰 تم الدفع
async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user

    keyboard = [
        [InlineKeyboardButton("✅ تأكيد الدفع", callback_data=f"confirm_{user.id}")]
    ]

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"""💰 طلب تأكيد دفع

👤 {user.first_name}
🆔 {user.id}""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except:
        pass

    await query.message.reply_text("⏳ تم إرسال طلبك للمراجعة")

# 🔒 تأكيد الدفع
async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.data.split("_")[1]

    try:
        with open("orders.json", "r") as file:
            orders = json.load(file)
    except:
        orders = []

    for order in orders:
        if order.get("user_id") == user_id:
            order["status"] = "مدفوع"

    with open("orders.json", "w") as file:
        json.dump(orders, file, indent=4)

    await query.message.reply_text("✅ تم تأكيد الدفع")

    await context.bot.send_message(
        chat_id=int(user_id),
        text="🎉 تم تأكيد الدفع بنجاح\n\n📅 التفعيل يوم 16\n⏳ المدة 28 يوم\n🙏 شكراً ليك"
    )

# ▶️ تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(choose_package, pattern="^[1-4]$"))
    app.add_handler(CallbackQueryHandler(handle_payment, pattern="paid"))
    app.add_handler(CallbackQueryHandler(confirm_payment, pattern="^confirm_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 البوت شغال...")
    app.run_polling()
