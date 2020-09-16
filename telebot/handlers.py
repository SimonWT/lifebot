from telegram.ext import Dispatcher,  CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from threading import Thread

LOCATION, BUDGET = range(2)

def init_bot(bot, update_queue, logger_g):
    # Create bot, update queue and dispatcher instances
    dispatcher = Dispatcher(bot, update_queue)
    global logger
    logger = logger_g

    ##### Register handlers here #####

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            LOCATION: [MessageHandler(Filters.location, location)],
            BUDGET: [MessageHandler(Filters.text, budget)],
            # PLACES: [MessageHandler(Filters.text, budget)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    
    # Start the thread
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()
    logger.info("Webhook Setted Up")
    return update_queue

def start(update, context):
    # location_keyboard = KeyboardButton(text="send_location", request_location=True)
    # custom_keyboard = [[ location_keyboard]]
    # reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    # custom_keyboard = [['top-left', 'top-right'], 
    #                ['bottom-left', 'bottom-right']]

    # reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # context.bot.send_message(text='Send me the Location of place where you plan to go', reply_markup=reply_markup)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

    # return 10 #LOCATION

def location(update, context):
    user = context.message.from_user
    user_location = context.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    context.message.reply_text('Thanks, Maybe I can visit you sometime! '
                              'Tell me, what is your budget?')

    return BUDGET

def budget(update, context):
    user = context.message.from_user
    logger.info("Budget of %s: %s", user.first_name, context.message.text)
    context.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def start(update, context):
    context.message.reply_text('Send me the Location of place where you plan to go')
    return LOCATION

def cancel(update, context):
    user = context.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    context.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END