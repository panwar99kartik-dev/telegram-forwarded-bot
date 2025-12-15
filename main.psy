from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8403795351:AAFsCY7rLCWQbPsVXhuskHwxAtjgXxG4Q8o"

# 🔐 PERMANENT USER LOCK (IDs)
ALLOWED_USER_IDS = {
    6575589039,     # Your user ID
    0      # Another allowed user
}

# 🎯 ONLY THIS GROUP WILL RECEIVE MESSAGES
TARGET_GROUP_ID = -1003457551207

def is_allowed(user):
    return user.id in ALLOWED_USER_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user):
        return
    await update.message.reply_text("✅ You are allowed to use this bot.")

async def on_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user):
        return
    context.user_data["enabled"] = True
    await update.message.reply_text("🔔 Forwarding ON")

async def off_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user):
        return
    context.user_data["enabled"] = False
    await update.message.reply_text("🔕 Forwarding OFF")

async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_allowed(user):
        return

    if context.user_data.get("enabled") is False:
        return

    sender = user.full_name
    uname = f"@{user.username}" if user.username else ""

    prefix = f"📨 Sent by: {sender} {uname}\n\n"

    try:
        if update.message.text:
            await context.bot.send_message(
                chat_id=TARGET_GROUP_ID,
                text=prefix + update.message.text
            )
        else:
            await update.message.copy(
                chat_id=TARGET_GROUP_ID,
                caption=prefix + (update.message.caption or "")
            )
    except:
        pass

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("on", on_cmd))
app.add_handler(CommandHandler("off", off_cmd))
app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.ALL, forward))

print("Bot running...")
app.run_polling()
