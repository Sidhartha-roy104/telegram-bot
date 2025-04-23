import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "7966311975:AAEbrQSjP44HhUQh99rC64ljaKykoWe40IQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"{i} Sem", callback_data=f"sem_{i}")] for i in range(1, 9)
    ]
    await update.message.reply_text(
        "👋 Hello! Select your semester to continue:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle_sem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    sem = query.data.split("_")[1]
    context.user_data["sem"] = sem

    keyboard = [
        [InlineKeyboardButton("CIE1", callback_data="exam_CIE1")],
        [InlineKeyboardButton("CIE2", callback_data="exam_CIE2")],
        [InlineKeyboardButton("SEM", callback_data="exam_SEM")]
    ]
    await query.message.reply_text(
        f"📘 Selected Semester: {sem}\nNow select the type of exam:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    exam_type = query.data.split("_")[1]
    sem = context.user_data.get("sem")

    await query.message.reply_text(f"🔍 Fetching timetable for Sem {sem} - {exam_type}...")

    
    folder_path = "timetables"  
    image = None
    for ext in ['jpg', 'jpeg', 'png']:
        path = os.path.join(folder_path, f"{sem}_{exam_type}.{ext}")
        if os.path.exists(path):
            image = path
            break

    if image:
        with open(image, "rb") as img:
            await context.bot.send_photo(chat_id=query.message.chat.id, photo=img)
    else:
        await query.message.reply_text("❌ Timetable not found for this selection.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_sem, pattern="^sem_"))
    app.add_handler(CallbackQueryHandler(handle_exam, pattern="^exam_"))
    app.run_polling()

if __name__ == "__main__":
    main()
