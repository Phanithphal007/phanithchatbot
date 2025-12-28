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
        # Free tier Gemini API endpoint
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
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
        
        # Check if response is valid
        if "candidates" in data and len(data["candidates"]) > 0:
            ai_reply = data["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in data:
            ai_reply = f"API Error: {data['error'].get('message', 'Unknown error')}"
        else:
            ai_reply = f"Unexpected response format: {data}"
            
    except requests.exceptions.RequestException as e:
        ai_reply = f"Network error: {str(e)}"
    except KeyError as e:
        ai_reply = f"Response parsing error: Missing key {str(e)}"
    except Exception as e:
        ai_reply = f"Unexpected error: {str(e)}"

    await update.message.reply_text(ai_reply)

# ==== MAIN ====
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("Bot is running...")
app.run_polling()