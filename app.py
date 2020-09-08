from flask import Flask, request, Response
import telegram
from telebot.credentials import bot_token, bot_user_name, URL
from telebot.mastermind import get_response
from database.db import initialize_db
from database.models import Place
import json
import logging

from queue import Queue  # in python 2 it should be "from Queue"
from threading import Thread
from telegram.ext import Dispatcher, CommandHandler


global bot
global TOKEN
global updateQueue
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://root:root@cluster0.ro0oy.mongodb.net/test'
}
initialize_db(app)

@app.route('/telegram{}'.format(TOKEN), methods=['POST'])
def respond():
    # # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    updateQueue.put(update)

    # chat_id = update.message.chat.id
    # msg_id = update.message.message_id

    # # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

    # response = get_response(text)
    # bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)


    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}/telegram{HOOK}'.format(URL=URL, HOOK=TOKEN))
    updateQueue = setup_tg_bot()
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

def setup_tg_bot():
    # Create bot, update queue and dispatcher instances
    update_queue = Queue()
    dispatcher = Dispatcher(bot, update_queue)

    ##### Register handlers here #####
    
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    # Start the thread
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()
    
    return update_queue
    # you might want to return dispatcher as well, 
    # to stop it at server shutdown, or to register more handlers:
    # return (update_queue, dispatcher)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

if __name__ == '__main__':
    app.run(threaded=True)