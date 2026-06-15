import os
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Flask Server for Render
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Live!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Bot Config
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_URL = "https://check-bind.onrender.com/bindinfo"
OWNER_HANDLE = "@xnitehere"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "🚀 **WELCOME TO XNITE BIND CHECKER** 🚀\n\n"
        "✨ *Main aapke account ki bind details nikalne mein expert hoon.*\n\n"
        "🔹 **Action:** Apna **ACCESS TOKEN** yahan bhejiye.\n"
        "🔹 **Support:** Koi dikkat ho toh contact karein: " + OWNER_HANDLE + "\n\n"
        "━━━━━━━━━━━━━━━━\n"
        "⚡ Powered by: **XNITE**"
    )
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def process_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = update.message.text.strip()
    status_msg = await update.message.reply_text("⏳ **Processing request...**")

    try:
        response = requests.get(f"{API_URL}?access_token={token}", timeout=30)
        data = response.json()
        
        if response.status_code == 200:
            result_data = data.get("result", {})
            current_email = result_data.get("email", "Not Found")
            new_email = result_data.get("email_to_be", "None")
            
            result_msg = (f"✅ **GMAIL CHECK SUCCESSFUL**\n\n"
                          f"📧 **Current Email:** `{current_email}`\n"
                          f"📧 **Pending/New Email:** `{new_email if new_email else 'None'}`\n"
                          f"━━━━━━━━━━━━━━━━\n"
                          f"👤 Owner: {OWNER_HANDLE}\n"
                          f"⚡ Powered by: **XNITE**")
            await status_msg.edit_text(result_msg, parse_mode='Markdown')
        else:
            await status_msg.edit_text("❌ **Invalid Token!** Dubara koshish karein.")
            
    except Exception as e:
        await status_msg.edit_text(f"⚠️ **Error:** {str(e)}")

if __name__ == '__main__':
    Thread(target=run_server).start()
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), process_token))
    app_bot.run_polling()

