from typing import Final
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import definitii
import anki


TOKEN: Final = '6935360468:AAF2Gie3DY9S9e6vqSKPdQLRFdZOTq4qtDQ'
BOT_USERNAME: Final = '@roman_dic_bot'


reply_keyboard = [["/add_card", "/next"]]

keyboard_reply = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False)


# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Input the word you are searching for!", reply_markup=keyboard_reply)


async def next_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(definitii.next_entry())


async def anki_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(anki.add_card())


# responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    return definitii.search(processed)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update: {Update} caused error {context.error}')


if __name__ == '__main__':
    print('starting bot...')
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('next', next_command))
    app.add_handler(CommandHandler('add_card', anki_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    app.add_error_handler(error)

    # polls the bot
    print('poling...')
    app.run_polling(poll_interval=3)
