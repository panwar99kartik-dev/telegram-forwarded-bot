from telegram.ext import Updater, CommandHandler
from telegram import Bot
import logging

# बॉट को सही तरीके से लॉग करने के लिए
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

active = False
selected_group = None

def start(update, context):
    update.message.reply_text('Hello! Use /on to activate, /off to deactivate, /select to select a group, and /listgroups to see your groups.')

def turn_on(update, context):
    global active
    active = True
    update.message.reply_text('Bot is now active!')

def turn_off(update, context):
    global active
    active = False
    update.message.reply_text('Bot is now inactive!')

def select_group(update, context):
    global selected_group
    if context.args:
        selected_group = context.args[0]
        update.message.reply_text(f'Selected group is now: {selected_group}')
    else:
        update.message.reply_text('Please provide a group name or ID.')

def list_groups(update, context):
    bot: Bot = context.bot
    user_id = update.message.from_user.id
    groups = []

    for dialog in bot.get_updates():
        chat = dialog.effective_chat
        if chat.type in ['group', 'supergroup']:
            member = bot.get_chat_member(chat.id, user_id)
            if member.status in ['administrator', 'creator']:
                groups.append(chat.title)

    if groups:
        update.message.reply_text("Groups where I'm admin:\n" + "\n".join(groups))
    else:
        update.message.reply_text("I couldn't find any groups where I'm an admin.")

def main():
    updater = Updater("8403795351:AAFsCY7rLCWQbPsVXhuskHwxAtjgXxG4Q8o")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("on", turn_on))
    dp.add_handler(CommandHandler("off", turn_off))
    dp.add_handler(CommandHandler("select", select_group))
    dp.add_handler(CommandHandler("listgroups", list_groups))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
