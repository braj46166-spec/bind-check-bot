import os
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Render ke liye Flask Server
app = Flask(__name__)
@app.route('/')
def home():
    return "XNITE Bot is Alive!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Configuration (Environment Variables se lein)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MY_CHAT_ID = int(os.environ.get("MY_CHAT_ID", 0))
API_URL = "https://check-bind.onrender.com/bindinfo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != MY_CHAT_ID: return
    
    welcome_text = (
        "✨ **WELCOME TO XNITE BIND CHECKER** ✨\n\n"
        "╭───────────────╮\n"
        "   🚀 FAST | SECURE | RELIABLE   \n"
        "╰───────────────╯\n\n"
        "📌 **Kaise use karein:**\n"
        "Bas apna **Token** yahan paste karein aur result payein! ⚡\n\n"
        "━━━━━━━━━━━━━━━━\n"
        "⚡ Powered by: **XNITE**"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != MY_CHAT_ID: return
    
    # Message ya Command se token nikalna
    token = context.args[0] if context.args else update.message.text.replace("/check", "").strip()
    
    status_msg = await update.message.reply_text("🔍 **Checking Bind Details...**")

    try:
        response = requests.get(f"{API_URL}?access_token={token}")
        data = response.json()
        
        if response.status_code == 200:
            email = data.get("email", "Not Found")
            msg = (f"✅ **BIND SUCCESSFUL**\n\n"
                   f"📧 **Email:** `{email}`\n"
                   f"━━━━━━━━━━━━━━━━\n"
                   f"⚡ Powered by: **XNITE**")
            await status_msg.edit_text(msg, parse_mode='Markdown')
        else:
            await status_msg.edit_text("❌ **Invalid Token!** Check karein aur phir koshish karein.")
    except Exception as e:
        await status_msg.edit_text(f"⚠️ **Error:** {str(e)}")

if __name__ == '__main__':
    # Server start
    Thread(target=run_server).start()
    
    # Bot start
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler(["start", "hi"], start))
    app_bot.add_handler(CommandHandler("check", check))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), check))
    
    app_bot.run_polling()
