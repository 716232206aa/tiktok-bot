import os
import re
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('أرسل لي رابط فيديو تيك توك وأنا بحمله لك بدون علامة مائية 🎥')

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    if 'tiktok.com' not in url:
        await update.message.reply_text('هذا مو رابط تيك توك صحيح ❌')
        return
    
    msg = await update.message.reply_text('جاري التحميل... ⏳')
    
    try:
        api_url = f'https://api.tiklydown.eu.org/api/download?url={url}'
        response = requests.get(api_url)
        data = response.json()
        
        if data['status'] == 'success':
            video_url = data['video']['noWatermark']
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=video_url,
                caption='تم التحميل ✅ @YourBotName'
            )
            await msg.delete()
        else:
            await msg.edit_text('فشل التحميل، تأكد من الرابط 😢')
            
    except Exception as e:
        await msg.edit_text('صار خطأ أثناء التحميل ❌')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))
    app.run_polling()

if __name__ == '__main__':
    main()
