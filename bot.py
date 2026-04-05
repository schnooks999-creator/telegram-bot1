import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# 🔐 التوكن
TOKEN = "7966652318:AAHyN7iJw3HYX-eeTKJ2zqMZMeZQKmnj_0Y"

# 🧑‍💼 الايدي
ADMIN_ID = "5613451219"

# 📱 رقم واتساب
WHATSAPP_NUMBER = "201227115782"

user_data_store = {}

packages = {
    "1": "📶 40 جيجا | 1500 دقيقة | 400 جنيه",
    "2": "📶 50 جيجا | 1500 دقيقة | 470 جنيه",
    "3": "📶 60 جيجا | 1500 دقيقة | 540 جنيه",
    "4": "📶 70 جيجا | 1500 دقيقة | 600 جنيه",
}

def save_order(data):
    try:
        with open("orders.json", "r") as file:
            orders = json.load(file)
    except:
        orders = []

    orders.append(data)

    with open("orders.json", "w") as file:
        json.dump(orders, file, indent=4)

# 🚀 بداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(packages["1"], callback_data="1")],
        [InlineKeyboardButton(packages["2"], callback_data="2")],
        [InlineKeyboardButton(packages["3"], callback_data="3")],
        [InlineKeyboardButton(packages["4"], callback_data="4")],
    ]

    await update.message.reply_text(
        "🔥 احجز باقتك الآن 🔥\n\n"
        "📌 التفعيل يوم 16\n\n"
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

    if context.user_data.get("step") == "name":
        user_data_store[user_id]["name"] = text
        await update.message.reply_text("📱 اكتب رقمك")
        context.user_data["step"] = "phone"

    elif context.user_data.get("step") == "phone":
        user_data_store[user_id]["phone"] = text

        data = user_data_store[user_id]

        order = {
            "name": data["name"],
            "phone": data["phone"],
            "package": data["package"],
            "status": "جديد",
            "user_id": str(user_id),
            "date": str(datetime.now())
        }

        save_order(order)

        # 📩 إرسال الطلب ليك
        if ADMIN_ID != "ID":
            await context.bot.send_message(
                chat_id=int(ADMIN_ID),
                text=f"""📥 طلب جديد

👤 {data['name']}

📱 {data['phone']}

{data['package']}"""
            )

        # 🔗 أزرار
        whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}"
        keyboard = [
            [InlineKeyboardButton("📩 تواصل واتساب", url=whatsapp_url)],
            [InlineKeyboardButton("✔️ تم الدفع", callback_data="paid")]
        ]

        # 💬 رسالة العميل
        await update.message.reply_text(
            "✅ تم تسجيل طلبك بنجاح\n\n"
            "⏳ احجز مكانك قبل اكتمال العدد\n\n"
            "💵 حول الكاش على الرقم ده\n"
            "01024929685\n\n"
            "📱 ابعت على واتساب\n"
            "📸 صورة التحويل والرقم اللي تم التحويل منه\n\n"
            "\n"
            "📋 وابعت كل التفاصيل على واتساب لتأكيد الطلب\n\n"
            "✔️ بعد التحويل اضغط تم الدفع",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        context.user_data.clear()

# 💰 العميل ضغط تم الدفع
async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user

    keyboard = [
        [InlineKeyboardButton("✅ تأكيد الدفع", callback_data=f"confirm_{user.id}")]
    ]

    if ADMIN_ID != "ID":
        await context.bot.send_message(
            chat_id=int(ADMIN_ID),
            text=f"""💰 عميل طلب تأكيد الدفع

👤 {user.first_name}

🆔 {user.id}""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    await query.message.reply_text("⏳ تم إرسال طلبك وجاري المراجعة")

# 🔒 تأكيد الأدمن
async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.data.split("_")[1]

    try:
        with open("orders.json", "r") as file:
            orders = json.load(file)
    except:
        orders = []

    user_order = None

    for order in orders:
        if order.get("user_id") == user_id:
            order["status"] = "مدفوع"
            user_order = order

    with open("orders.json", "w") as file:
        json.dump(orders, file, indent=4)

    await query.message.reply_text("✅ تم تأكيد الدفع وتحديث الحالة")

    # 📲 رسالة العميل (التعديل الجديد)
    if user_order:
        await context.bot.send_message(
            chat_id=int(user_id),
            text=f"""🎉 تم تأكيد الدفع بنجاح

{user_order['package']}

📅 موعد التفعيل يوم 16

⏱️ المدة 28 يوم

🙏 شكراً ليك وثقتك بينا"""
        )

# ⚙️ تشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(choose_package, pattern="^[1-4]$"))
app.add_handler(CallbackQueryHandler(handle_payment, pattern="paid"))
app.add_handler(CallbackQueryHandler(confirm_payment, pattern="^confirm_"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🚀 البوت شغال...")
app.run_polling()
