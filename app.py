from flask import Flask, request, Response
import telegram
from telebot.credentials import bot_token, bot_user_name, URL
from telebot.mastermind import get_response
from database.db import initialize_db
from database.models import Place
import json


global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://root:root@cluster0.ro0oy.mongodb.net/test'
}
initialize_db(app)

@app.route('/telegram{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

    response = get_response(text)
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}/telegram{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'

@app.route('/places')
def get_movies():
    places = Places.objects().to_json()
    return Response(places, mimetype="application/json", status=200)

@app.route('/place', methods=['POST'])
    body = request.get_json()
    place =  Place(**body).save()
    id = place.id
    return {'id': str(id)}, 200


if __name__ == '__main__':
    app.run(threaded=True)