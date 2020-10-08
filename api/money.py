from flask import Blueprint, Response,request
from database.models import Wallet, Transaction, User
import datetime

money = Blueprint('money', __name__)

@money.route('/api/user/<chat_id>/money', methods=['GET'])
def get_wallet(chat_id):
    user = User.objects().get(chat_id=chat_id)
    wallet = Wallet.objects().get(user=user)
    return Response(wallet.to_json(), mimetype="application/json", status=200)

@money.route('/api/user/<chat_id>/money', methods=['POST'])
def create_wallet(chat_id):
    body = request.get_json()
    wallet = Wallet(**body)
    wallet.user = User.objects().get(chat_id=chat_id)
    wallet.save()
    id = wallet.id
    return {'id': str(id)}, 200

@money.route('/api/user/<chat_id>/transactions', methods=['POST'])
def make_transaction(chat_id):
    body = request.get_json()
    transaction = Transaction(**body)
    user = User.objects().get(chat_id=chat_id)
    wallet = Wallet.objects().get(user=user)
    wallet.balance = wallet.balance + transaction.delta
    wallet.save()
    transaction.wallet = wallet
    transaction.time = datetime.datetime.utcnow()
    transaction.save()
    id = transaction.id
    return {'id': str(id)}, 200

@money.route('/api/user/<chat_id>/transactions', methods=['GET'])
def get_transactions(chat_id):
    user = User.objects().get(chat_id=chat_id)
    wallet = Wallet.objects().get(user=user)
    transactions = Transaction.objects().filter(wallet=wallet)
    json_data = transactions.to_json()
    return json_data, 200