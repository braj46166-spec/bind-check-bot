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
MY_CHAT_ID = int(os.environ.get("MY_CHAT_ID", 0))
API_URL = "https://check-bind.onrender.com/bindinfo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != MY_CHAT_ID: return
    await update.message.reply_text("🤖 **XNITE BIND CHECKER**\n\nBas apna **Token** bhejiye, main API se fetch karke details dikha dunga. ⚡")

async def process_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != MY_CHAT_ID: return
    
    token = update.message.text.strip()
    
    # 1. Processing message
    status_msg = await update.message.reply_text("⏳ **Processing...**")

    # 2. API Call
    try:
        response = requests.get(f"{API_URL}?access_token={token}", timeout=10)
        data = response.json()
        
        # 3. Result extract karna
        if response.status_code == 200:
            # Yahan hum nested 'result' ke andar se email nikal rahe hain
            result_data = data.get("result", {})
            email = result_data.get("email", "Not Found")
            
            result_msg = (f"✅ **BIND SUCCESSFUL**\n\n"
                          f"📧 **Email:** `{email}`\n"
                          f"━━━━━━━━━━━━━━━━\n"
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
    # Bina command ke token process karega
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), process_token))
    
    app_bot.run_polling()
