import telebot
import os
from telebot import types

TOKEN = os.environ.get("TOKEN")
CHANNEL = "@moneydrop5488"
REQUIRED_INVITES = 2

bot = telebot.TeleBot(TOKEN)

# user_id -> {"invites": set(), "unlocked": False}
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
        users[user_id] = {"invites": set(), "unlocked": False}

    # Referral detect
    if len(args) > 1:
        ref_id = args[1]
        if ref_id.isdigit():
            ref_id = int(ref_id)
            if ref_id != user_id and ref_id in users:
                if user_id not in users[ref_id]["invites"] and is_joined(user_id):
                    users[ref_id]["invites"].add(user_id)
                    inviter_name = msg.from_user.first_name
                    bot.send_message(
                        ref_id,
                        f"✅ {inviter_name} successfully invited by you\n🎯 {len(users[ref_id]['invites'])}/{REQUIRED_INVITES} completed"
                    )

    if not is_joined(user_id):
        markup = types.InlineKeyboardMarkup()
        join = types.InlineKeyboardButton("📢 Join MoneyDrop Channel", url="https://t.me/moneydrop5488")
        check = types.InlineKeyboardButton("✅ Joined", callback_data="check")
        markup.add(join)
        markup.add(check)

        bot.send_message(
            user_id,
            "🔐 *Free Subscribers Unlock Karne ke liye*\n\nPehle hamara channel join karo 👇",
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
    invited = len(users[user_id]["invites"])
    remaining = REQUIRED_INVITES - invited
    names = "\n".join([str(uid) for uid in users[user_id]["invites"]]) if invited > 0 else "None"

    bot.send_message(
        user_id,
        f"📊 *Your Referral Status*\n\nInvited: {invited}\nRemaining: {remaining}\n\nUser IDs:\n{names}",
        parse_mode="Markdown"
    )

def send_referral_panel(user_id):
    invited = len(users[user_id]["invites"])

    if invited >= REQUIRED_INVITES:
        bot.send_message(
            user_id,
            "🎉 *Unlocked!*\n\nYou have completed 2 invites.\n\n🎁 Reward unlocked — Contact Admin or Claim Reward.",
            parse_mode="Markdown"
        )
        return

    link = f"https://t.me/freesubgainbot?start={user_id}"

    markup = types.InlineKeyboardMarkup()
    status = types.InlineKeyboardButton("📊 How many invites", callback_data="status")
    markup.add(status)

    bot.send_message(
        user_id,
        f"🎯 *Invite 2 Friends to Unlock*\n\n🔗 Your Link:\n{link}\n\nInvited: {invited}/{REQUIRED_INVITES}",
        reply_markup=markup,
        parse_mode="Markdown"
    )

bot.polling(none_stop=True)
