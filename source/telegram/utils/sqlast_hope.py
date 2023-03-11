from telegram.utils.user import User
from telegram.utils.connect_creater import connect


session = connect('telegram/assets/secure/database.db')


def create_user(chat_id):
    user = User()
    user.chat_id = chat_id
    session.add(user)
    session.commit()
    users[chat_id] = user


def set_user_attr(chat_id, attr_name, value):
    setattr(users[chat_id], attr_name, value)
    session.commit()


def get_users():
    data = session.query(User)
    response = {user.chat_id: user for user in data}
    return response


users = get_users()
