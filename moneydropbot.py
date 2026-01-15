import telebot

TOKEN = "PASTE_TOKEN_HERE"
CHANNEL = "@moneydrop5488"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    user_id = msg.from_user.id
    markup = telebot.types.InlineKeyboardMarkup()
    join = telebot.types.InlineKeyboardButton("📢 Join MoneyDrop Channel", url="https://t.me/moneydrop5488")
    check = telebot.types.InlineKeyboardButton("✅ Joined", callback_data="check")
    markup.add(join)
    markup.add(check)

    bot.send_message(
        user_id,
        "🔐 *Free Subscribers Unlock Karne ke liye*\n\nPehle hamara channel join karo 👇",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "check")
def check(call):
    user_id = call.from_user.id
    try:
        status = bot.get_chat_member(CHANNEL, user_id).status
        if status in ["member", "administrator", "creator"]:
            bot.send_message(
                user_id,
                "✅ *Verified!*\n\n🎯 MoneyDrop Free Subscriber System Activated!\n\nApna link share karo 👇",
                parse_mode="Markdown"
            )
            bot.send_message(user_id, f"https://t.me/freesub_gain_bot?start={user_id}")
        else:
            bot.answer_callback_query(call.id, "❌ Pehle channel join karo")
    except:
        bot.answer_callback_query(call.id, "❌ Join nahi kiya")

bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
