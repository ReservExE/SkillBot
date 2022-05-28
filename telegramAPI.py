import telebot

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Greetings! My purpose is to show you the popularity of skills within the vacancy you tell me\n' +
        'Try searching for a vacancy using /skills.\n' +
        'To request a new data cluster use /cluster. \n' +
        'To get help press /help.'
  )