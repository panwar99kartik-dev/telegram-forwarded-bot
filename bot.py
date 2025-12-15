from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import config

bot_status = True   # ON / OFF

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == config.OWNER_ID:
        await update.message.reply_text("✅ Bot ready hai")

async def on_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_status
    if update.effective_user.id == config.OWNER_ID:
        bot_status = True
        await update.message.reply_text("🟢 Bot ON ho gaya")

async def off_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_status
    if update.effective_user.id == config.OWNER_ID:
        bot_status = False
        await update.message.reply_text("🔴 Bot OFF ho gaya")

async def forward_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != config.OWNER_ID:
        return
    if not bot_status:
        return

    await context.bot.copy_message(
        chat_id=config.GROUP_ID,
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )

app = ApplicationBuilder().token(config.BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("on", on_cmd))
app.add_handler(CommandHandler("off", off_cmd))
app.add_handler(MessageHandler(filters.ALL & filters.ChatType.PRIVATE, forward_to_group))

print("🤖 Bot chal raha hai...")
app.run_polling()
