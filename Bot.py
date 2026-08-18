import telebot
from telebot import types

# ----------------- CONFIGURATION -----------------
BOT_TOKEN = "8910296599:AAEV4-kVj3eUAzWlclDQzdpLQCSy40qSbqA"
ADMIN_ID = 8800158361  # Apna numeric Telegram ID daalein
GROUP_INVITE_LINK = "https://t.me/+YourPrivateGroupLink"

# Images ke Direct Links (.jpg/.png URL)
WELCOME_PHOTO_URL = "https://t.me/shjahshsbsb/4"
UPI_QR_PHOTO_URL = "https://t.me/shjahshsbsb/5"
USDT_QR_PHOTO_URL = "https://t.me/shjahshsbsb/6"

UPI_ID = "your-upi-id@oksbi"
USDT_ADDRESS = "0xb9784568555cd9b7b79178905e5581a0fde55e71"
# -------------------------------------------------

bot = telebot.TeleBot(BOT_TOKEN)
waiting_screenshot = set()

# 1. /start command: Welcome Photo + Message + Pricing Buttons
@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_inr = types.InlineKeyboardButton("🇮🇳 Buy Premium (INR)", callback_data="pay_inr")
    btn_usd = types.InlineKeyboardButton("💵 Buy Premium ($)", callback_data="pay_usd")
    markup.add(btn_inr, btn_usd)

    welcome_text = (
        "🎬 *Welcome to Premium Access!*\n\n"
        "🔥 Direct Unlimited Premium Videos\n"
        "⚡ Viral & Exclusive Content\n"
        "🔒 Secure & Instant Access\n\n"
        "👇 *Neeche diye gaye option se currency select karein:*"
    )

    bot.send_photo(
        message.chat.id,
        photo=WELCOME_PHOTO_URL,
        caption=welcome_text,
        parse_mode="Markdown",
        reply_markup=markup
    )

# 2. INR Button Handler
@bot.callback_query_handler(func=lambda call: call.data == "pay_inr")
def process_inr(call):
    markup = types.InlineKeyboardMarkup()
    btn_upload = types.InlineKeyboardButton("📤 Send Payment Screenshot", callback_data="upload_proof")
    markup.add(btn_upload)

    inr_text = (
        "🇮🇳 *INR Payment Details:*\n\n"
        "💰 *Amount:* ₹89\n"
        f"💳 *UPI ID:* {UPI_ID} (Tap to copy)\n\n"
        "📌 *Steps:*\n"
        "1. Upar diye QR ya UPI ID par exact amount send karein.\n"
        "2. Payment hone ke baad neeche 'Send Payment Screenshot' button dabayein."
    )

    bot.send_photo(
        call.message.chat.id,
        photo=UPI_QR_PHOTO_URL,
        caption=inr_text,
        parse_mode="Markdown",
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

# 3. USD ($) Button Handler
@bot.callback_query_handler(func=lambda call: call.data == "pay_usd")
def process_usd(call):
    markup = types.InlineKeyboardMarkup()
    btn_upload = types.InlineKeyboardButton("📤 Send Payment Screenshot", callback_data="upload_proof")
    markup.add(btn_upload)

    usd_text = (
        "💵 *Crypto / USDT Payment Details:*\n\n"
        "💰 *Amount:* 1 USDT (BEP20)\n"
        f"📫 *Address:* {USDT_ADDRESS} (Tap to copy)\n\n"
        "📌 *Steps:*\n"
        "1. Upar diye QR ya Address par exact 1 USDT bhejein.\n"
        "2. Payment ke baad neeche 'Send Payment Screenshot' button dabayein."
    )

    bot.send_photo(
        call.message.chat.id,
        photo=USDT_QR_PHOTO_URL,
        caption=usd_text,
        parse_mode="Markdown",
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

# 4. Request Screenshot Handler
@bot.callback_query_handler(func=lambda call: call.data == "upload_proof")
def ask_proof(call):
    waiting_screenshot.add(call.from_user.id)
    bot.send_message(call.message.chat.id, "Kripya apne payment ka screenshot yahan send karein 👇")
    bot.answer_callback_query(call.id)

# 5. Handle Screenshot Upload & Forward to Admin
@bot.message_handler(content_types=['photo'])
def handle_payment_photo(message):
    user_id = message.chat.id
    if user_id in waiting_screenshot:
        waiting_screenshot.remove(user_id)

        admin_markup = types.InlineKeyboardMarkup()
        btn_approve = types.InlineKeyboardButton("Approve ✅", callback_data=f"app_{user_id}")
        btn_reject = types.InlineKeyboardButton("Reject ❌", callback_data=f"rej_{user_id}")
        admin_markup.row(btn_approve, btn_reject)
