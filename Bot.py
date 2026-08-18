import os
import threading
from flask import Flask
import telebot
from telebot import types

# ----------------- FLASK SERVER FOR RENDER -----------------
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()
# -----------------------------------------------------------

# ----------------- CONFIGURATION -----------------
BOT_TOKEN = "8910296599:AAEV4-kVj3eUAzWlclDQzdpLQCSy40qSbqA"
ADMIN_ID = 8800158361
GROUP_INVITE_LINK = "https://t.me/+YourPrivateGroupLink"

# Images ke links
WELCOME_PHOTO_URL = "https://t.me/shjahshsbsb/4"
UPI_QR_PHOTO_URL = "https://t.me/shjahshsbsb/5"
USDT_QR_PHOTO_URL = "https://t.me/shjahshsbsb/6"

UPI_ID = "your-upi-id@oksbi"
USDT_ADDRESS = "0xb9784568555cd9b7b79178905e5581a0fde55e71"
# -------------------------------------------------

bot = telebot.TeleBot(BOT_TOKEN)
waiting_screenshot = set()

def send_safe_photo(chat_id, photo_url, caption, reply_markup=None):
    try:
        bot.send_photo(
            chat_id,
            photo=photo_url,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except Exception:
        bot.send_message(
            chat_id,
            f"{caption}\n\n🖼️ [View Image / QR Code]({photo_url})",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

# 1. /start command
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

    send_safe_photo(message.chat.id, WELCOME_PHOTO_URL, welcome_text, markup)

# 2. INR Button Handler
@bot.callback_query_handler(func=lambda call: call.data == "pay_inr")
def process_inr(call):
    markup = types.InlineKeyboardMarkup()
    btn_upload = types.InlineKeyboardButton("📤 Send Payment Screenshot", callback_data="upload_proof")
    markup.add(btn_upload)

    inr_text = (
        "🇮🇳 *INR Payment Details:*\n\n"
        "💰 *Amount:* ₹89\n"
        f"💳 *UPI ID:* `{UPI_ID}` (Tap to copy)\n\n"
        "📌 *Steps:*\n"
        "1. Upar diye QR ya UPI ID par exact amount send karein.\n"
        "2. Payment hone ke baad neeche 'Send Payment Screenshot' button dabayein."
    )

    send_safe_photo(call.message.chat.id, UPI_QR_PHOTO_URL, inr_text, markup)
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
        f"📫 *Address:* `{USDT_ADDRESS}` (Tap to copy)\n\n"
        "📌 *Steps:*\n"
        "1. Upar diye QR ya Address par exact 1 USDT bhejein.\n"
        "2. Payment ke baad neeche 'Send Payment Screenshot' button dabayein."
    )

    send_safe_photo(call.message.chat.id, USDT_QR_PHOTO_URL, usd_text, markup)
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

        user_info = f"@{message.from_user.username}" if message.from_user.username else "No Username"
        caption = f"🔔 *New Payment Submission!*\nUser: {user_info}\nUser ID: `{user_id}`"

        file_id = message.photo[-1].file_id
        bot.send_photo(ADMIN_ID, file_id, caption=caption, parse_mode="Markdown", reply_markup=admin_markup)
        bot.reply_to(message, "⏳ Screenshot received! Verification ke baad link isi chat me aa jayega.")
    else:
        bot.reply_to(message, "Pehle /start karke payment method select karein.")

# 6. Admin Approval / Rejection Trigger
@bot.callback_query_handler(func=lambda call: call.data.startswith(("app_", "rej_")))
def handle_admin_action(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Permission Denied!", show_alert=True)
        return

    action, target_user_id = call.data.split("_")
    target_user_id = int(target_user_id)

    if action == "app":
        bot.send_message(
            target_user_id,
            f"🎉 *Payment Verified!*\n\nAapka Private Access Link: {GROUP_INVITE_LINK}",
            parse_mode="Markdown"
        )
        bot.edit_message_caption(
            caption=call.message.caption + "\n\n**Status: Approved ✅**",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )
        bot.answer_callback_query(call.id, "Approved & Link Sent!")

    elif action == "rej":
        bot.send_message(target_user_id, "❌ Aapka payment reject ho gaya hai. Sahi transaction screenshot bhejein.")
        bot.edit_message_caption(
            caption=call.message.caption + "\n\n**Status: Rejected ❌**",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )
        bot.answer_callback_query(call.id, "Rejected!")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
