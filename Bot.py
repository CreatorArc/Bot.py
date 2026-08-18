import os
import threading
from flask import Flask
import telebot
from telebot import types

# ----------------- FLASK SERVER FOR RENDER -----------------
app = Flask('')

@app.route('/')
def home():
    return "Viral Hamster Bot is running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()
# -----------------------------------------------------------

# ----------------- CONFIGURATION -----------------
BOT_TOKEN = "8818467580:AAEDJPd20gPQHULPXDex_NBH6p-giiDXU1g"
ADMIN_ID = 8800158361

# Channel Links
MAIN_CHANNEL_LINK = "https://t.me/Bl4ck_hamster"
PRIVATE_CHANNEL_LINK = "https://t.me/+c_tXyHANcaczZWE9"
DEMO_VIDEO_LINK = "https://t.me/shjahshsbsb/10"

# Photos ke link
WELCOME_PHOTO_URL = "https://t.me/shjahshsbsb/4"
UPI_QR_PHOTO_URL = "https://t.me/shjahshsbsb/5"
USDT_QR_PHOTO_URL = "https://t.me/shjahshsbsb/6"

UPI_ID = "paytmqr2810050501011gv6cueh16my@paytm"
USDT_ADDRESS = "0xb9784568555cd9b7b79178905e5581a0fde55e71"
# -------------------------------------------------

bot = telebot.TeleBot(BOT_TOKEN)
bot.remove_webhook()
waiting_screenshot = set()

def add_user(user_id):
    try:
        if not os.path.exists("users.txt"):
            with open("users.txt", "w") as f:
                f.write("")
        with open("users.txt", "r") as f:
            users = f.read().splitlines()
        if str(user_id) not in users:
            with open("users.txt", "a") as f:
                f.write(str(user_id) + "\n")
    except Exception as e:
        print(f"Error saving user: {e}")

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
    add_user(message.chat.id)
    user_name = message.from_user.first_name

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_inr = types.InlineKeyboardButton("🖼️ Buy Access (₹)", callback_data="pay_inr")
    btn_usd = types.InlineKeyboardButton("🖼️ Buy Access ($)", callback_data="pay_usd")
    btn_demo = types.InlineKeyboardButton("📺 Demo video", url=DEMO_VIDEO_LINK)
    btn_channel = types.InlineKeyboardButton("📢 Main Channel", url=MAIN_CHANNEL_LINK)
    
    markup.add(btn_inr, btn_usd)
    markup.add(btn_demo)
    markup.add(btn_channel)

    welcome_text = (
        f"👋 *Welcome {user_name}*\n\n"
        "*Viral hamster bot* is ready!\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "✈️ *What You Get:*\n\n"
        "• 🔥 Unlimited daily new videos\n"
        "• 🌛 Viral famous videos\n"
        "• 🛡️ Secure & private\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "👇 _Click below to buy access_"
    )

    send_safe_photo(message.chat.id, WELCOME_PHOTO_URL, welcome_text, markup)

# Broadcast Command
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return
    text = message.text.replace("/broadcast", "").strip()
    if not text:
        bot.reply_to(message, "Usage: `/broadcast Aapka message yahan`", parse_mode="Markdown")
        return
    if not os.path.exists("users.txt"):
        bot.reply_to(message, "Koi user database me nahi hai.")
        return
    with open("users.txt", "r") as f:
        users = f.read().splitlines()
    count = 0
    for u_id in users:
        try:
            bot.send_message(u_id, text)
            count += 1
        except Exception:
            pass
    bot.reply_to(message, f"✅ Broadcast sent to {count} users!")

# 2. INR Button Handler
@bot.callback_query_handler(func=lambda call: call.data == "pay_inr")
def process_inr(call):
    markup = types.InlineKeyboardMarkup()
    btn_upload = types.InlineKeyboardButton("📤 Send Payment Screenshot", callback_data="upload_proof")
    markup.add(btn_upload)

    inr_text = (
        "🇮🇳 *INR Payment Details:*\n\n"
        "💰 Pay 59₹ to get Premium 999+ Videos\n\n"
        "🐾 Pay 89₹ to get Animal Pack 1500+ Videos\n\n"
        f"💳 *UPI ID:* `{UPI_ID}`\n(Tap to copy)\n\n"
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

    action, target_user_id_str = call.data.split("_")
    target_user_id = int(target_user_id_str)

    if action == "app":
        try:
            join_btn = types.InlineKeyboardMarkup()
            join_btn.add(types.InlineKeyboardButton("📢 Main Channel", url=MAIN_CHANNEL_LINK))
            
            bot.send_message(
                target_user_id,
                f"🎉 *Payment Verified!*\n\nAapka Private Access Link:\n{PRIVATE_CHANNEL_LINK}",
                parse_mode="Markdown",
                reply_markup=join_btn
            )
        except Exception as e:
            print(f"Error sending link to user: {e}")

        try:
            bot.edit_message_caption(
                caption=call.message.caption + "\n\nStatus: Approved ✅",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
        except Exception:
            pass

        bot.answer_callback_query(call.id, "Approved & Link Sent Successfully!")

    elif action == "rej":
        try:
            bot.send_message(target_user_id, "❌ Aapka payment reject ho gaya hai. Sahi transaction screenshot bhejein.")
        except Exception as e:
            print(f"Error sending reject notice: {e}")

        try:
            bot.edit_message_caption(
                caption=call.message.caption + "\n\nStatus: Rejected ❌",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
        except Exception:
            pass

        bot.answer_callback_query(call.id, "Payment Rejected!")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
