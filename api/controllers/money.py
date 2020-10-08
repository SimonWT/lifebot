from database.models import Wallet, Transaction, User
import datetime

def get_wallet(chat_id):
    user = User.objects().get(chat_id=chat_id)
    wallet = Wallet.objects().get(user=user)
    return wallet

def create_wallet(chat_id, params):
    wallet = Wallet(**params)
    wallet.user = User.objects().get(chat_id=chat_id)
    wallet.save()
    id = wallet.id
    return id

def make_transaction(chat_id, params):
    transaction = Transaction(**params)
    user = User.objects().get(chat_id=chat_id)
    wallet = Wallet.objects().get(user=user)
    wallet.balance = wallet.balance + transaction.delta
    wallet.save()
    transaction.wallet = wallet
    transaction.time = datetime.datetime.utcnow()
    transaction.save()
    id = transaction.id
    return id

def get_transactions(chat_id):
    user = User.objects().get(chat_id=chat_id)
    wallet = Wallet.objects().get(user=user)
    transactions = Transaction.objects().filter(wallet=wallet)
    return transactions