# can't upload big chunks of text to Telegram
# anki button works only for the last search (because of list deleting)

import asyncio
from typing import Final

import telegram.error
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import definitii
import sinteza
import anki

TOKEN: Final = '6935360468:AAF2Gie3DY9S9e6vqSKPdQLRFdZOTq4qtDQ'
BOT_USERNAME: Final = '@roman_dic_bot'


# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''
    looking for dictionary entries on dexonline.ro
    
ℹ️ type ‹login› for authorization on anki web

️ℹ️ symbol «🧩» stands for 'Definitii' entry

ℹ️ symbol «🔎» stands for 'Sinteza' entry
    ''')


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("add 2 anki", callback_data="1"),
            InlineKeyboardButton("next entry", callback_data="2"),
        ]
    ]
    error_keyboard = [
        [
            InlineKeyboardButton("next entry", callback_data="2"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    error_reply_markup = InlineKeyboardMarkup(error_keyboard)

    query = update.callback_query
    await query.answer()
    if query.data == '1':
        await query.message.reply_text(anki.add_card())
    if query.data == '2':
        try:
            await query.message.reply_text(definitii.next_entry(), reply_markup=reply_markup)
        except telegram.error.BadRequest:
            return await query.message.reply_text('Sorry! Entry is too long (Try next one!)', reply_markup=error_reply_markup)


# responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    return sinteza.sinteza_search(processed)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message_type: str = update.message.chat.type
    text: str = update.message.text

    keyboard = [
        [
            InlineKeyboardButton("add 2 anki", callback_data="1"),
            InlineKeyboardButton("next entry", callback_data="2"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return

    if anki.login_mode is False and update.message.text.lower() != 'login':
        response: str = handle_response(text)
        print('Bot:', response)
        await update.message.reply_text(response, reply_markup=reply_markup)

    if anki.login_mode is True:
        anki.tries += 1
        user_info = open('user_info', 'a')
        x = update.message.text
        user_info.write(f'{x}\n')
        if anki.tries == 2:
            anki.login_mode = False
            await update.message.reply_text('Saved!')
        else:
            await update.message.reply_text('Please enter your password:')

    if update.message.text.lower() == 'login':
        anki.login_mode = True
        user_info = open('user_info', 'w')
        user_info.flush()
        anki.tries = 0
        await update.message.reply_text('Please enter your login:')


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update: {Update} caused error {context.error}')
    x = str(context.error)
    if "#no-such-element-exception" in x:
        await update.message.reply_text('No such entry!')


if __name__ == '__main__':
    print('starting bot...')
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CallbackQueryHandler(button))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    app.add_error_handler(error)

    # polls the bot
    print('poling...')
    app.run_polling(poll_interval=3)
