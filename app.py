from flask import Flask, request, Response
import telegram

from telebot.credentials import bot_token, bot_user_name, URL
from telebot.mastermind import get_response
from telebot import handlers as tghandlers

from database.db import initialize_db
from database.models import Place
import json
import logging

from queue import Queue  # in python 2 it should be "from Queue"
from telegram.ext import Dispatcher, CommandHandler


global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
update_queue = Queue()

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://root:root@cluster0.ro0oy.mongodb.net/test'
}

initialize_db(app)

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
    s = bot.setWebhook('{URL}/telegram{HOOK}'.format(URL=URL, HOOK=TOKEN))
    tghandlers.init_bot(bot, update_queue, logger)
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'

@app.route('/places', methods=['GET'])
def get_places():
    places = Place.objects().to_json()
    return Response(places, mimetype="application/json", status=200)

@app.route('/place', methods=['POST'])
def add_place():
    body = request.get_json()
    place = Place(**body).save()
    id = place.id
    return {'id': str(id)}, 200

if __name__ == '__main__':
    app.run(threaded=True)