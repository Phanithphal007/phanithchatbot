import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# ==== CONFIGURE KEYS FROM ENVIRONMENT ====
TELEGRAM_TOKEN = os.environ.get("8590602701:AAGDf0QKrZq3RgKbE1PSNuF_wSohCIM1igQ")
GEMINI_API_KEY = os.environ.get("AIzaSyBIrtiBy5Mfua0R_5jxW1PQZWXjR09uXZM")

# Model for free-tier Google Generative API
MODEL_NAME = "models/text-bison-001"

# ==== FUNCTIONS ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm your AI chatbot powered by Google's Generative API. Type anything!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    ai_reply = "Sorry, I couldn't get a response from AI."

    try:
        # Call Google Generative API
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1/{MODEL_NAME}:generateText?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "prompt": user_message,
                "temperature": 0.7,
                "candidate_count": 1,
                "max_output_tokens": 256
            }
        )
        data = response.json()
        if "candidates" in data and len(data["candidates"]) > 0:
            ai_reply = data["candidates"][0]["output"]
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
