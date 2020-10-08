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
    
    # Start the thread
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()
    logger.info("Webhook Setted Up")
    return update_queue

def start(update, context):
    # context.message.reply_text('Send me the sum on month: /set <sum>')
    context.message.reply_text('Привет! Давай начнём работу.\nОтправь мне сколько у тебя сейчас денег')
    chat_id = context.message.chat_id
    try: 
        user = User.objects().get(chat_id=chat_id)
        user.delete()
    except:
        logger.error('No user with chat id {}'.format(chat_id))
    user_logic.create_user({"chat_id": context.message.chat_id})
    return SETTING

def set(update, context):
    chat_id = context.message.chat_id
    balance = int(context.message.text)
    # data[chat_id] = {"sum": month_sum, "day_sum": month_sum / 30, "balance": month_sum / 30}
    context.message.reply_text('Ваш баланс {}p'.format(balance))
    money_logic.create_wallet(chat_id, { "balance": balance})
    context.message.reply_text('Теперь, если будешь тратить или внезапно получишь деньги отправляй: /spend или /earn')

    return LIVE

def spend(update, context):
    context.message.reply_text('Напишите мне сколько вы потратили')
    return SPEND

def do_spend(update, context):
    amount = int(context.message.text)
    chat_id = context.message.chat_id
    money_logic.make_transaction(chat_id, {"category": "default", "delta": -amount})
    text = 'Вы потратили '
    context.message.reply_text(text + '{} p.\nВаш баланс: {}.p'.format(amount, money_logic.get_wallet(chat_id).balance))

    return LIVE

def earn(update, context):
    context.message.reply_text('Напишите мне сколько вы заработали')
    return EARN

def do_earn(update, context):
    amount = int(context.message.text)
    chat_id = context.message.chat_id
    money_logic.make_transaction(chat_id, {"category": "default", "delta": amount})
    text = 'Вы заработали '
    context.message.reply_text(text + '{} p.\nВаш баланс: {}.p'.format(amount, money_logic.get_wallet(chat_id).balance))
    return LIVE

def status(update, context):
    context.message.reply_text(data[context.message.chat_id])

def dialy_update_balance(context):
    job = context.job
    chat_id = job.context
    data[chat_id]["balance"] += data[chat_id]["day_sum"]
    context.bot.send_message(chat_id, text='Доброе утро!\n+{}\nСегодня вы можете потратить {}p.\n'.format(data[chat_id]["day_sum"], data[chat_id]["balance"]))

def stop(update, context):

    if 'job' not in context.chat_data:
        context.message.reply_text('У вас нет активных аккаунтов. Отправь мне /start чтобы начать заново.')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    context.message.reply_text('Ваш аккаунт диактивирован. Отправь мне /start чтобы начать заново.')

def do_echo(update):
    context.message.reply_text(context.message.text)