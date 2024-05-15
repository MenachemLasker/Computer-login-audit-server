from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import *
from botTelegram import *
YOUR_TOKEN= "6906120319:AAGcdv8JCg5zjWgksXk7pCNm-VfqPP3mw7Q"
USERNAME, PASSWORD, BTN = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("follow", callback_data='follow'),
         InlineKeyboardButton("unfollow", callback_data='unfollow')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('בחר אופציה:', reply_markup=reply_markup)
    return BTN

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    # בדיקת ה- callback_data והפעלת הפונקציה המתאימה
    if query.data == 'follow':
        await follow(update, context)
    elif query.data == 'unfollow':
        await unfollow(update, context)
async def follow(update: Update, context: CallbackContext) -> int:
    # בדיקה אם זה CallbackQuery ולא הודעה רגילה
    if update.callback_query:
        query = update.callback_query
        # עריכת ההודעה המקורית או שליחת הודעה חדשה
        #await query.message.edit_text("אנא הזן שם משתמש:")
        # או
        await context.bot.send_message(chat_id=query.message.chat_id, text="אנא הזן שם משתמש:")
    else:
        # אם זו הודעה רגילה, ניתן להשיב כרגיל
        await update.message.reply_text("אנא הזן שם משתמש:")
    return USERNAME


async def get_user_data(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if context.user_data.get('username') is None:
        if has_user(text):
            context.user_data['username'] = text
            await update.message.reply_text("אנא הזן סיסמה:")
            return PASSWORD  # ממשיך לשלב הבא שהוא קבלת הסיסמה
        else:
            await update.message.reply_text("שם המשתמש לא קיים, אנא נסה שוב:")
            return USERNAME  # חוזר לשלב קבלת שם המשתמש
    else:
        if verify_user(context.user_data['username'], text):
            follow_user(context.user_data['username'], update.message.chat_id)
            await update.message.reply_text("עקבת אחרי המשתמש בהצלחה.")
        else:
            await update.message.reply_text("err")
        context.user_data.clear()  # ניקוי הנתונים לפני סיום השיחה
        return ConversationHandler.END  # סיום השיחה

def main() -> None:
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            BTN: [CallbackQueryHandler(button)],
            USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_user_data)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_user_data)],
        },
        fallbacks=[CommandHandler('cancel', lambda update, context: ConversationHandler.END)],
    )

    application = Application.builder().token(YOUR_TOKEN).build()
    application.add_handler(conv_handler)
    #application.add_handler(CommandHandler('start', start))
    #application.add_handler(CallbackQueryHandler(button))
    application.run_polling()

if __name__ == '__main__':
    main()




