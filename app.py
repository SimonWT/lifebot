from flask import Flask, request, Response
import telegram

from telebot.credentials import bot_token, bot_user_name, URL
from telebot.mastermind import get_response
# from telebot import handlers as tghandlers
from telebot.moneybot import handlers as tghandlers

from database.db import initialize_db
from database.models import Place
import json
import logging

from queue import Queue  # in python 2 it should be "from Queue"
from telegram.ext import Dispatcher, CommandHandler

from api.money import money as money_api
from api.places import places as places_api
from api.user import user as user_api


global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
update_queue = Queue()

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'LifeBot',
    'host': 'mongodb+srv://root:root@cluster0.ro0oy.mongodb.net/test'
}

initialize_db(app)

app.register_blueprint(money_api)
app.register_blueprint(places_api)
app.register_blueprint(user_api)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

@app.route('/telegram{}'.format(TOKEN), methods=['POST'])
def respond():
    # # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    update_queue.put(update)

    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    logger.info("Setting webhook... URL:{}   TOKEN:{}".format(URL=URL, HOOK=TOKEN))
    s = bot.setWebhook('{URL}/telegram{HOOK}'.format(URL=URL, HOOK=TOKEN))
    tghandlers.init_bot(bot, update_queue, logger)
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(threaded=True)

set_webhook()
print(app.url_map)