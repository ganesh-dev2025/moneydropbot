import telebot
import os
from telebot import types

TOKEN = os.environ.get("TOKEN")
CHANNEL = "@moneydrop5488"
REQUIRED_INVITES = 2

bot = telebot.TeleBot(TOKEN)

# user_id -> {"invites": set()}
users = {}

def is_joined(user_id):
    try:
        status = bot.get_chat_member(CHANNEL, user_id).status
        return status in ["member", "administrator", "creator"]
    except:
        return False

@bot.message_handler(commands=['start'])
def start(msg):
    user_id = msg.from_user.id
    args = msg.text.split()

    if user_id not in users:
        users[user_id] = {"invites": set()}

    # -------- Referral Detect --------
    if len(args) > 1 and args[1].isdigit():
        ref_id = int(args[1])

        if ref_id != user_id:
            if ref_id not in users:
                users[ref_id] = {"invites": set()}

            if (
                user_id not in users[ref_id]["invites"]
                and is_joined(user_id)
            ):
                users[ref_id]["invites"].add(user_id)

                inviter_name = msg.from_user.first_name or "User"
                bot.send_message(
                    ref_id,
                    f"✅ {inviter_name} successfully invited\n"
                    f"🎯 {len(users[ref_id]['invites'])}/{REQUIRED_INVITES} completed"
                )

    # -------- Force Channel Join --------
    if not is_joined(user_id):
        markup = types.InlineKeyboardMarkup()
        join = types.InlineKeyboardButton(
            "📢 Join MoneyDrop Channel",
            url="https://t.me/moneydrop5488"
        )
        check = types.InlineKeyboardButton(
            "✅ Joined",
            callback_data="check"
        )
        markup.add(join)
        markup.add(check)

        bot.send_message(
            user_id,
            "🔐 *Free Subscribers Unlock Karne ke liye*\n\n"
            "Pehle hamara channel join karo 👇",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return

    send_referral_panel(user_id)

@bot.callback_query_handler(func=lambda call: call.data == "check")
def check(call):
    user_id = call.from_user.id
    if is_joined(user_id):
        send_referral_panel(user_id)
    else:
        bot.answer_callback_query(call.id, "❌ Pehle channel join karo")

@bot.callback_query_handler(func=lambda call: call.data == "status")
def status(call):
    user_id = call.from_user.id
    invited = len(users.get(user_id, {"invites": set()})["invites"])
    remaining = REQUIRED_INVITES - invited

    bot.send_message(
        user_id,
        f"📊 *Your Referral Status*\n\n"
        f"Invited: {invited}\n"
        f"Remaining: {remaining}",
        parse_mode="Markdown"
    )

def send_referral_panel(user_id):
    invited = len(users[user_id]["invites"])

    if invited >= REQUIRED_INVITES:
        bot.send_message(
            user_id,
            "🎉 *Unlocked!*\n\n"
            "You have completed 2 invites.\n\n"
            "🎁 Reward unlocked!",
            parse_mode="Markdown"
        )
        return

    bot_username = bot.get_me().username
    link = f"https://t.me/{bot_username}?start={user_id}"

    markup = types.InlineKeyboardMarkup()
    status_btn = types.InlineKeyboardButton(
        "📊 How many invites",
        callback_data="status"
    )
    markup.add(status_btn)

    bot.send_message(
        user_id,
        f"🎯 *Invite 2 Friends to Unlock*\n\n"
        f"🔗 Your Link:\n{link}\n\n"
        f"Invited: {invited}/{REQUIRED_INVITES}",
        reply_markup=markup,
        parse_mode="Markdown"
    )

bot.polling(none_stop=True)
