from database.models import User

def get_user(chat_id):
    user = User.objects().get(chat_id=chat_id).to_json()
    return Response(user, mimetype="application/json", status=200)

def create_user(params):
    user = User(**params).save({"upsert": True})
    id = user.id
    return id

def edit_user(chat_id, params):
   user = User.objects().get(chat_id=chat_id)
   user.update(**params)
   return user