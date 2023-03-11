import telebot
from telebot import types
from telegram.utils import config, get_languages, sqlast_hope, music_api


TE = 'Error: text of this message not found in current language pack'
bot = telebot.TeleBot(token=config.TOKEN)

languages = get_languages.get()


@bot.message_handler(commands=['start'])
def start(message):
    bot.delete_message(message_id=message.id, chat_id=message.chat.id)
    markup = types.InlineKeyboardMarkup()
    for elem in languages.keys():
        markup.row(types.InlineKeyboardButton(elem, callback_data=f'lang:{elem}'))
    mid = bot.send_message(message.chat.id, text='Hello and welcome!<3. Please, choose preferred language to continue:',
                           reply_markup=markup).id
    if message.chat.id not in sqlast_hope.users:
        sqlast_hope.create_user(chat_id=message.chat.id)
    else:
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=sqlast_hope.users[message.chat.id].message_id)
            bot.delete_message(chat_id=message.chat.id, message_id=sqlast_hope.users[message.chat.id].player_id)
        except telebot.apihelper.ApiTelegramException:
            pass
    sqlast_hope.set_user_attr(chat_id=message.chat.id, attr_name='message_id', value=mid)


@bot.callback_query_handler(func=lambda call: call.data.startswith('lang:'))
def language_handler(call):
    language = call.data.split(':')[1]
    sqlast_hope.set_user_attr(chat_id=call.message.chat.id, attr_name='language', value=language)
    markup = types.InlineKeyboardMarkup()
    b_home = types.InlineKeyboardButton(languages[language].get('home', TE),
                                        callback_data='home')
    markup.row(b_home)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                          text=languages[language].get('welcome', TE), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'home')
def main_menu(call):
    markup = types.InlineKeyboardMarkup()
    user = sqlast_hope.users[call.message.chat.id]
    markup.row(types.InlineKeyboardButton(languages[user.language].get('music', TE),
                                          callback_data='music'))
    markup.row(types.InlineKeyboardButton(languages[user.language].get('settings', TE),
                                          callback_data='settings'))
    bot.edit_message_text(chat_id=user.chat_id, message_id=call.message.id,
                          text=languages[user.language].get('home_text', TE), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'settings')
def settings(call):
    user = sqlast_hope.users[call.message.chat.id]
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(languages[user.language].get('language', TE), callback_data='set_lang'))
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE), callback_data='home'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                          text=languages[user.language].get('settings_text', TE), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'set_lang')
def set_language(call):
    user = sqlast_hope.users[call.message.chat.id]
    markup = types.InlineKeyboardMarkup()
    for elem in languages.keys():
        markup.row(types.InlineKeyboardButton(elem, callback_data=f'lang:{elem}'))
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE), callback_data='settings'),
               types.InlineKeyboardButton(languages[user.language].get('home', TE), callback_data='home'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                          text=languages[user.language].get('set_lang_text', TE), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'music')
def music(call):
    user = sqlast_hope.users[call.message.chat.id]
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(languages[user.language].get('search', TE), callback_data='search'))
    markup.row(types.InlineKeyboardButton(languages[user.language].get('liked', TE), callback_data='liked'))
    markup.row(types.InlineKeyboardButton(languages[user.language].get('playlists', TE), callback_data='playlists'))
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE), callback_data='home'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                          text=languages[user.language].get('music_main_text', TE), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'playlists')
def playlists_view(call):
    user = sqlast_hope.users[call.message.chat.id]
    markup = types.InlineKeyboardMarkup()
    u = False
    for elem in user.get_playlists().keys():
        text = elem if elem != "sysdata--lsr" else languages[user.language].get("lsr", TE)
        markup.row(types.InlineKeyboardButton(text + '🎶', callback_data=f'pl:{elem}'))
        u = True
    markup.row(types.InlineKeyboardButton(languages[user.language].get('new_pl', TE), callback_data='new_pl'))
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE), callback_data='music'),
               types.InlineKeyboardButton(languages[user.language].get('home', TE), callback_data='home'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup,
                          text=languages[user.language].get('playlists_text' if u else 'empty_playlists', TE))


@bot.callback_query_handler(func=lambda call: call.data.startswith('pl:'))
def playlist_view(call):
    user = sqlast_hope.users[call.message.chat.id]
    markup = types.InlineKeyboardMarkup()
    pl_name = ":".join(call.data.split(':')[1:])
    for track in user.get_playlists()[pl_name]:
        markup.row(types.InlineKeyboardButton(music_api.get_metadata(track), callback_data=f"play:{track}::{pl_name}"))
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE),
                                          callback_data='playlists'),
               types.InlineKeyboardButton(languages[user.language].get('home', TE), callback_data='home'))
    text = pl_name if pl_name != 'sysdata--lsr' else languages[user.language].get("lsr", TE)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup,
                          text=languages[user.language].get("playlist_text", TE) + text)


@bot.callback_query_handler(func=lambda call: call.data == 'search')
def search(call):
    user = sqlast_hope.users[call.message.chat.id]
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE), callback_data='music'),
               types.InlineKeyboardButton(languages[user.language].get('home', TE), callback_data='home'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup,
                          text=languages[user.language].get('search_text', TE))
    bot.register_next_step_handler(message=call.message, callback=handle_search)


def handle_search(message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    except telebot.apihelper.ApiTelegramException:
        pass
    user = sqlast_hope.users[message.chat.id]
    markup = types.InlineKeyboardMarkup()
    response = music_api.search(message.text)
    u = False
    for elem in response:
        u = True
        markup.row(types.InlineKeyboardButton(elem['name'], callback_data=f"play:{elem['id']}::sysdata--lsr"))
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE),
                                          callback_data='search'),
               types.InlineKeyboardButton(languages[user.language].get('home', TE), callback_data='home'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=user.message_id, reply_markup=markup,
                          text=languages[user.language].get('search_response_text' if u else "empty_response", TE))
    if u:
        playlist = user.get_playlists()
        playlist['sysdata--lsr'] = [track['id'] for track in response]
        sqlast_hope.set_user_attr(chat_id=message.chat.id, attr_name='playlists', value=user.pack_playlists(playlist))


@bot.callback_query_handler(func=lambda call: call.data.startswith('play:'))
def play(call):
    track_id, playlist = ':'.join(call.data.split(':')[1:]).split('::')
    link = music_api.get_link(track_id)
    user = sqlast_hope.users[call.message.chat.id]
    meta = music_api.get_metadata(track_id)
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(languages[user.language].get('close', TE), callback_data='del'))
    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=user.player_id)
    except telebot.apihelper.ApiTelegramException:
        pass
    finally:
        pid = bot.send_audio(audio=link, chat_id=call.message.chat.id, caption=meta, reply_markup=markup).id
        sqlast_hope.set_user_attr(chat_id=call.message.chat.id, attr_name='player_id', value=pid)
        bot.answer_callback_query(callback_query_id=call.id, text=languages[user.language].get('downloaded', TE))


@bot.message_handler(content_types=['text', 'audio', 'photo', 'video', 'media', 'file', 'voice', 'video_note'])
def deleter(message):
    bot.delete_message(message.chat.id, message.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('del'))
def del_player(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)


if __name__ == '__main__':
    bot.remove_webhook()
    print('initialize completed')
    bot.infinity_polling()
