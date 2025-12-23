from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters
)

BOT_TOKEN = "8403795351:AAFsCY7rLCWQbPsVXhuskHwxAtjgXxG4Q8o"

forwarding_enabled = False
selected_chat_id = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot Ready\n\n"
        "/groups - Group/Channel select करें\n"
        "/on - Forwarding ON\n"
        "/off - Forwarding OFF"
    )


async def groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chats = []
    for chat in context.bot_data.get("chats", []):
        chats.append([
            InlineKeyboardButton(
                text=chat["title"],
                callback_data=str(chat["id"])
            )
        ])

    if not chats:
        await update.message.reply_text(
            "❌ कोई Group/Channel नहीं मिला\n"
            "👉 Bot को पहले Admin बनाओ"
        )
        return

    await update.message.reply_text(
        "📌 Group/Channel select करें:",
        reply_markup=InlineKeyboardMarkup(chats)
    )


async def select_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global selected_chat_id
    query = update.callback_query
    await query.answer()
    selected_chat_id = int(query.data)
    await query.edit_message_text("✅ Group/Channel Selected")


async def on_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global forwarding_enabled
    forwarding_enabled = True
    await update.message.reply_text("✅ Forwarding ON")


async def off_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global forwarding_enabled
    forwarding_enabled = False
    await update.message.reply_text("⛔ Forwarding OFF")


async def handle_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not forwarding_enabled or not selected_chat_id:
        return

    msg = update.message

    if msg.text:
        await context.bot.send_message(
            chat_id=selected_chat_id,
            text=msg.text
        )

    elif msg.photo:
        await context.bot.send_photo(
            chat_id=selected_chat_id,
            photo=msg.photo[-1].file_id,
            caption=msg.caption
        )

    elif msg.video:
        await context.bot.send_video(
            chat_id=selected_chat_id,
            video=msg.video.file_id,
            caption=msg.caption
        )


async def track_chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup", "channel"]:
        chats = context.bot_data.setdefault("chats", [])
        if not any(c["id"] == chat.id for c in chats):
            chats.append({"id": chat.id, "title": chat.title})


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("groups", groups))
    app.add_handler(CommandHandler("on", on_cmd))
    app.add_handler(CommandHandler("off", off_cmd))

    app.add_handler(CallbackQueryHandler(select_chat))
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE, handle_private_message))
    app.add_handler(MessageHandler(filters.ALL, track_chats))

    print("🤖 Bot Started")
    app.run_polling()


if __name__ == "__main__":
    main()
