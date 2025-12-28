import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# ==== CONFIGURE KEYS FROM ENVIRONMENT ====
TELEGRAM_TOKEN = "8590602701:AAGDf0QKrZq3RgKbE1PSNuF_wSohCIM1igQ"
GEMINI_API_KEY = "AIzaSyDy3nTs68uMdlS-g5of5HQoxEZ4fu0LGVY"

# ==== FUNCTIONS ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your AI chatbot powered by Gemini. Type anything!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        # Correct Gemini API endpoint
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {
                        "parts": [
                            {"text": user_message}
                        ]
                    }
                ]
            }
        )
        data = response.json()
        ai_reply = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        ai_reply = f"Sorry, I couldn't get a response from AI. Error: {str(e)}"

    await update.message.reply_text(ai_reply)

# ==== MAIN ====
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("Bot is running...")
app.run_polling()