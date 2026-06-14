import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# CONFIGURATION
BOT_TOKEN = "8951887268:AAFilwp2BhsGgIDNXmWVYhJAR7jkRVSE80Y"
MY_CHAT_ID = 7293041159
API_URL = "https://check-bind.onrender.com/bindinfo"

# Function for /start and /hi
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != MY_CHAT_ID:
        await update.message.reply_text("❌ Access Denied!")
        return

    welcome_msg = (
        "🤖 **Welcome to XNITE Bind Checker**\n\n"
        "Main aapki bind gmail check karne mein madad kar sakta hoon.\n\n"
        "👉 Use: `/check [TOKEN]`\n\n"
        "━━━━━━━━━━━━━━\n"
        "⚡ Powered by: **XNITE**"
    )
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

# Function for /check
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != MY_CHAT_ID:
        return

    if not context.args:
        await update.message.reply_text("⚠️ **Invalid!**\nSahi format: `/check [TOKEN]`")
        return

    token = context.args[0]
    status_msg = await update.message.reply_text("⏳ Fetching data...")

    try:
        response = requests.get(f"{API_URL}?access_token={token}")
        data = response.json()

        if response.status_code == 200:
            email = data.get("email", "Email nahi mila")
            msg = (f"✅ **Bind Details Found:**\n\n"
                   f"📧 Gmail: `{email}`\n\n"
                   f"━━━━━━━━━━━━━━\n"
                   f"⚡ Powered by: **XNITE**")
            await status_msg.edit_text(msg, parse_mode='Markdown')
        else:
            await status_msg.edit_text("❌ Token invalid hai ya API error hai.")
    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Teeno commands register ki gayi
    app.add_handler(CommandHandler("start", welcome))
    app.add_handler(CommandHandler("hi", welcome))
    app.add_handler(CommandHandler("check", check))
    
    print("Bot is ready and running with XNITE branding...")
    app.run_polling()
