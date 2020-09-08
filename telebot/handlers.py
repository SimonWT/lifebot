from telegram.ext import Dispatcher,  CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

LOCATION, BUDGET = range(2)


def init_bot(bot, update_queue):
    # Create bot, update queue and dispatcher instances
    dispatcher = Dispatcher(bot, update_queue)

    ##### Register handlers here #####
    
    # start_handler = CommandHandler('start', tghandlers.startCommand)
    # dispatcher.add_handler(start_handler)

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            LOCATION: [MessageHandler(Filters.location, location)],

            BUDGET: [MessageHandler(Filters.text & ~Filters.command, budget)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    
    # Start the thread
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()
    
    return update_queue

def start(update, context):
    context.message.reply_text('Send me the Location of place where you plan to go')

    return LOCATION

def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Thanks, Maybe I can visit you sometime! '
                              'Tell me, what is your budget?')

    return BUDGET


def budget(update, context):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def start(update, context):
    context.message.reply_text('Send me the Location of place where you plan to go')

    return LOCATION

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END