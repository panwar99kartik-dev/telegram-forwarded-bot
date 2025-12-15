
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Environment variables (set these in Render)
BOT_TOKEN = os.environ.get("8403795351:AAFsCY7rLCWQbPsVXhuskHwxAtjgXxG4Q8o")
TARGET_GROUP_ID = int(os.environ.get("-1003457551207"))
ALLOWED_USER_IDS = [int(os.environ.get("6575589039"))]

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USER_IDS:
        return
    await update.message.reply_text("✅ Bot is running and allowed!")

# Forward messages
async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in ALLOWED_USER_IDS:
        return

    try:
        if update.message.text:
            await context.bot.send_message(
                chat_id=TARGET_GROUP_ID,
                text=update.message.text
            )
        else:
            await update.message.copy(
                chat_id=TARGET_GROUP_ID
            )
    except Exception as e:
        print("Forward error:", e)

# Build app
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, forward))

print("Bot running...")
app.run_polling()
