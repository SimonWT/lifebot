from telegram.ext import Dispatcher,  CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from threading import Thread
from api.controllers import money as money_logic
from api.controllers import user as user_logic
from database.models import User

SETTING, SET_TIMER, LIVE, SPEND, EARN = range(5)

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
            SETTING: [MessageHandler(Filters.text, set)],
            LIVE: [CommandHandler("spend", spend),
                    CommandHandler("earn", earn)
                    ],
            SPEND: [MessageHandler(Filters.text, do_spend)],
            EARN: [MessageHandler(Filters.text, do_earn)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )


    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler('status', status)) 
    
    # Start the thread
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()
    logger.info("Webhook Setted Up")
    return update_queue

def start(update, context):
    # context.message.reply_text('Send me the sum on month: /set <sum>')
    context.message.reply_text('Hey! Lets start working.\nSend me how much money you got?')
    chat_id = context.message.chat_id
    try: 
        user_logic.delete_user(chat_id)
    except:
        logger.error('No user with chat id {}'.format(chat_id))
    user_logic.create_user({"chat_id": context.message.chat_id})
    return SETTING

def set(update, context):
    chat_id = context.message.chat_id
    balance = int(context.message.text)
    # data[chat_id] = {"sum": month_sum, "day_sum": month_sum / 30, "balance": month_sum / 30}
    context.message.reply_text('Your balance {}p'.format(balance))
    money_logic.create_wallet(chat_id, { "balance": balance})
    context.message.reply_text('Now, if you spend money or suddenly get money, send it: /spend or /earn')

    return LIVE

def spend(update, context):
    context.message.reply_text('Write me how much you spent')
    return SPEND

def do_spend(update, context):
    amount = int(context.message.text)
    chat_id = context.message.chat_id
    money_logic.make_transaction(chat_id, {"category": "default", "delta": -amount})
    text = 'You spent '
    context.message.reply_text(text + '{} p.\nCurrent balance: {}.p'.format(amount, money_logic.get_wallet(chat_id).balance))

    return LIVE

def earn(update, context):
    context.message.reply_text('Write me how much you earn')
    return EARN

def do_earn(update, context):
    amount = int(context.message.text)
    chat_id = context.message.chat_id
    money_logic.make_transaction(chat_id, {"category": "default", "delta": amount})
    text = 'You earn '
    context.message.reply_text(text + '{} p.\nCurrent balance: {}.p'.format(amount, money_logic.get_wallet(chat_id).balance))
    return LIVE

def status(update, context):
    chat_id = context.message.chat_id
    wallet = money_logic.get_wallet(chat_id)
    text = 'Wallet:\n\n Balance: {}\n ID: {}'.format(wallet.balance, wallet.id)
    context.message.reply_text(text)

def dialy_update_balance(context):
    job = context.job
    chat_id = job.context
    data[chat_id]["balance"] += data[chat_id]["day_sum"]
    context.bot.send_message(chat_id, text='Доброе утро!\n+{}\nСегодня вы можете потратить {}p.\n'.format(data[chat_id]["day_sum"], data[chat_id]["balance"]))

def stop(update, context):
    user_logic.delete_user(context.message.chat_id)
    context.message.reply_text('Your account is deactivated and all data is erased. Send me /start to start over.')

def do_echo(update):
    context.message.reply_text(context.message.text)