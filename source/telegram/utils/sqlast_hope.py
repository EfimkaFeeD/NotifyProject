import sqlite3
from telegram.utils.user import User


conn = sqlite3.connect('telegram/assets/secure/database.db', check_same_thread=False)
cur = conn.cursor()


def create_user(chat_id):
    cur.execute("""INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)""", (chat_id, -1, '', '', -1, ''))
    users[chat_id] = User(chat_id)
    conn.commit()


def set_user_attr(chat_id, attr_name, value):
    setattr(users[chat_id], attr_name, value)
    cur.execute(f"""UPDATE users SET {attr_name} = ? WHERE chat_id = ?""", (value, chat_id))
    conn.commit()


def get_users():
    data = cur.execute("""SELECT chat_id, message_id, liked, playlists, player_id, language FROM users""").fetchall()
    response = {elem[0]: User(chat_id=elem[0], message_id=elem[1], liked=elem[2], playlists=elem[3], player_id=elem[4],
                              language=elem[5]) for elem in data}
    return response


users = get_users()
