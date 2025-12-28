import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# ==== CONFIGURE KEYS ====
TELEGRAM_TOKEN = "8590602701:AAGDf0QKrZq3RgKbE1PSNuF_wSohCIM1igQ"
GEMINI_API_KEY = "AIzaSyDy3nTs68uMdlS-g5of5HQoxEZ4fu0LGVY"

# ==== FUNCTIONS ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm your AI chatbot powered by Gemini. Type anything!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Call Gemini API
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",  # Gemini endpoint is similar
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
            json={
                "model": "gemini-1.5",  # Replace with your available model
                "messages": [{"role": "user", "content": user_message}]
            }
        )
        data = response.json()
        ai_reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        ai_reply = "Sorry, I couldn't get a response from AI."

    await update.message.reply_text(ai_reply)

# ==== MAIN ====
app = ApplicationBuilder().token(8590602701:AAGDf0QKrZq3RgKbE1PSNuF_wSohCIM1igQ).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
