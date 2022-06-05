import logging

#On-demand parsing request and data display
import parse_logic as ps

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    Application,
    filters
)

import asyncio


#Exception handling: https://github.com/python-telegram-bot/v13.x-wiki/wiki/Exception-Handling
#Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# Stages
MAIN_ROUTES, END_ROUTES = range(2)
AWAITING_TEXT_REPLY = range(2)
# Callback data
ONE, TWO, THREE, FOUR = range(4)

reply_keyboard = [
    ["Skills", "Browse headhunter.ru", "Help"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    await update.message.reply_text("Greetings! My purpose is to show you the popularity\n"
                                    "of skills within the vacancy you tell me\n"
                                    "Try searching for a vacancy using /skills.\n"
                                    "To get help press /help.", reply_markup=markup)
    return MAIN_ROUTES


async def skills(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="skills_logic_here")


async def help(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=
        '1) Type /skills to receive a simple graph about top-10 in-demanded skills within the vacancy of choice\n'
        '2) If the data cluster containing you vacancy exists, you will receive an instant result\n' 
        '3) If the cluster is does not exist, I will look for the most similar ones\n' 
        '4) You can also use /cluster to request a new data cluster for better stats\n' 
        'The process of initializing a cluster may take some time, try looking fot the same vacancy in ~10 minutes\n',)


async def search_logic(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    logger.info(f"User {user.first_name} started fetching process.")
    await update.message.reply_text(f'Fetching data on {text} ...')
    user_request_object = ps.getSkillsFromPage(text=text, numpages=1)
    user_request_object.visualize_skills()
    #await update.message.reply_text(f'Data: \n'
    #                                f'{user_request_object.result}')

    await update.message.reply_photo(user_request_object.plot_path)


async def quickRequest(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await update.message.reply_text(f"Initializing a new search on headhunter.ru\n"
                                    f"Please, specify the search text...")

    return AWAITING_TEXT_REPLY


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=update.message.text)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def main() -> None:
    """Run the bot"""
    bot = Application.builder().token("5313943402:AAGDqkjcXSRDmCN2qfu8E01HNb7KC39dR2I").build()

    state_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_ROUTES: [
                MessageHandler(filters.Regex('^(Skills)$'), skills),
                MessageHandler(filters.Regex('^(Help)$'), help),
                MessageHandler(filters.Regex('^(Browse headhunter.ru)$'), quickRequest)

            ],
            AWAITING_TEXT_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND),
                    search_logic,
                )
            ]
        },
        fallbacks=[CommandHandler('start', start)],
    )

    bot.add_handler(state_handler)
    bot.run_polling()

if __name__ == '__main__':
    main()