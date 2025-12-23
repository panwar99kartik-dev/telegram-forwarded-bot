from telegram.ext import Updater, CommandHandler

active = False
selected_group = None

def start(update):
    update.message.reply_text('Hello! I am your bot. Use /on to activate, /off to deactivate.')

def turn_on(update):
    global active
    active = True
    update.message.reply_text('Bot is now active!')

def turn_off(update):
    global active
    active = False
    update.message.reply_text('Bot is now inactive!')

# Add other command functions similarly...

def main():
    updater = Updater("8403795351:AAFsCY7rLCWQbPsVXhuskHwxAtjgXxG4Q8o")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("on", turn_on))
    dp.add_handler(CommandHandler("off", turn_off))
    # Add other
