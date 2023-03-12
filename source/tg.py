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
    sqlast_hope.set_user_attr(chat_id=call.message.chat.id, attr_name='script', value='home')


@bot.callback_query_handler(func=lambda call: call.data == 'settings')
def settings(call):
    user = sqlast_hope.users[call.message.chat.id]
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(languages[user.language].get('language', TE), callback_data='set_lang'))
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE), callback_data='home'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                          text=languages[user.language].get('settings_text', TE), reply_markup=markup)
    sqlast_hope.set_user_attr(chat_id=call.message.chat.id, attr_name='script', value='settings')


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
    sqlast_hope.set_user_attr(chat_id=call.message.chat.id, attr_name='script', value='lang')


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
    sqlast_hope.set_user_attr(chat_id=call.message.chat.id, attr_name='script', value='music')


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
    sqlast_hope.set_user_attr(chat_id=call.message.chat.id, attr_name='script', value='playlists')


@bot.callback_query_handler(func=lambda call: call.data.startswith('pl:'))
def playlist_view(call):
    user = sqlast_hope.users[call.message.chat.id]
    markup = types.InlineKeyboardMarkup()
    pl_name = ":".join(call.data.split(':')[1:])
    u = False
    for row, track in enumerate(user.get_playlists()[pl_name]):
        u = True
        like_b = types.InlineKeyboardButton('❤️' if track in user.get_liked() else '🤍',
                                            callback_data=f'like:{track}:{row},1')
        markup.row(types.InlineKeyboardButton(music_api.get_metadata(track), callback_data=f"play:{track}::{pl_name}"),
                   like_b)
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE),
                                          callback_data='playlists'),
               types.InlineKeyboardButton(languages[user.language].get('home', TE), callback_data='home'))
    text = pl_name if pl_name != 'sysdata--lsr' else languages[user.language].get("lsr", TE)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup,
                          text=(languages[user.language].get("playlist_text", TE) + text) if u else
                          languages[user.language].get("empty_playlist", TE))
    sqlast_hope.set_user_attr(chat_id=call.message.chat.id, attr_name='script', value=f'playlist_view::{pl_name}::s')


@bot.callback_query_handler(func=lambda call: call.data == 'liked')
def liked_view(call):
    user = sqlast_hope.users[call.message.chat.id]
    markup = types.InlineKeyboardMarkup()
    u = False
    for row, elem in enumerate(user.get_liked()):
        like_b = types.InlineKeyboardButton('❤️', callback_data=f'like:{elem}:{row},1')
        markup.row(types.InlineKeyboardButton(music_api.get_metadata(elem), callback_data=f'play:{elem}::liked'),
                   like_b)
        u = True
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE), callback_data='music'),
               types.InlineKeyboardButton(languages[user.language].get('home', TE), callback_data='home'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup,
                          text=languages[user.language].get('liked_text' if u else 'empty_liked', TE))
    sqlast_hope.set_user_attr(chat_id=call.message.chat.id, attr_name='script', value='liked')


@bot.callback_query_handler(func=lambda call: call.data == 'search')
def search(call):
    user = sqlast_hope.users[call.message.chat.id]
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE), callback_data='music'),
               types.InlineKeyboardButton(languages[user.language].get('home', TE), callback_data='home'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup,
                          text=languages[user.language].get('search_text', TE))
    bot.register_next_step_handler(message=call.message, callback=handle_search)
    sqlast_hope.set_user_attr(chat_id=call.message.chat.id, attr_name='script', value='search')


def handle_search(message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    except telebot.apihelper.ApiTelegramException:
        pass
    user = sqlast_hope.users[message.chat.id]
    markup = types.InlineKeyboardMarkup()
    response = music_api.search(message.text)
    u = False
    for row, elem in enumerate(response):
        u = True
        like_b = types.InlineKeyboardButton('❤️' if str(elem['id']) in user.get_liked() else '🤍',
                                            callback_data=f'like:{elem["id"]}:{row},1')
        markup.row(types.InlineKeyboardButton(elem['name'], callback_data=f"play:{elem['id']}::sysdata--lsr"), like_b)
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE),
                                          callback_data='search'),
               types.InlineKeyboardButton(languages[user.language].get('home', TE), callback_data='home'))
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=user.message_id, reply_markup=markup,
                              text=languages[user.language].get('search_response_text' if u else "empty_response", TE))
    except telebot.apihelper.ApiTelegramException:
        pass
    if u:
        playlist = user.get_playlists()
        playlist['sysdata--lsr'] = [track['id'] for track in response]
        sqlast_hope.set_user_attr(chat_id=message.chat.id, attr_name='playlists', value=user.pack_playlists(playlist))
        if user.playlist == 'sysdata--lsr':
            try:
                track_id = user.track_id
                markup = types.InlineKeyboardMarkup()
                markup.row(types.InlineKeyboardButton('⏮️', callback_data="raise_end"),
                           types.InlineKeyboardButton('➕', callback_data=f'to_pl:{track_id}'),
                           types.InlineKeyboardButton('❤️' if track_id in user.get_liked() else '🤍',
                                                      callback_data=f'like:{track_id}:0,2'),
                           types.InlineKeyboardButton('⏭️', callback_data="raise_end"))
                markup.row(types.InlineKeyboardButton(languages[user.language].get('close', TE), callback_data='del'))
                bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=user.player_id, reply_markup=markup)
            except telebot.apihelper.ApiTelegramException:
                pass
    sqlast_hope.set_user_attr(chat_id=message.chat.id, attr_name='script', value='playlist_view::sysdata--lsr')


@bot.callback_query_handler(func=lambda call: call.data.startswith('play:'))
def play(call):
    track_id, playlist = ':'.join(call.data.split(':')[1:]).split('::')
    link = music_api.get_link(track_id)
    user = sqlast_hope.users[call.message.chat.id]
    user_playlist = user.get_playlists()[playlist] if playlist != 'liked' else user.get_liked()
    meta = music_api.get_metadata(track_id)
    markup = types.InlineKeyboardMarkup()
    like = types.InlineKeyboardButton('❤️' if track_id in user.get_liked() else '🤍',
                                      callback_data=f"like:{track_id}:0,2")
    next_callback = f'play:{user_playlist[user_playlist.index(track_id) + 1]}::{playlist}' if\
        user_playlist.index(track_id) < len(user_playlist) - 1 else "raise_end"
    prew_callback = f'play:{user_playlist[user_playlist.index(track_id) - 1]}::{playlist}' if\
        user_playlist.index(track_id) > 0 else "raise_end"
    markup.row(types.InlineKeyboardButton('⏮️', callback_data=prew_callback),
               types.InlineKeyboardButton('➕', callback_data=f'to_pl:{track_id}'), like,
               types.InlineKeyboardButton('⏭️', callback_data=next_callback))
    markup.row(types.InlineKeyboardButton(languages[user.language].get('close', TE), callback_data='del'))
    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=user.player_id)
    except telebot.apihelper.ApiTelegramException:
        pass
    finally:
        pl_name = playlist if playlist != 'sysdata--lsr' else languages[user.language].get('lsr', TE)
        pl_name = pl_name if pl_name != 'liked' else languages[user.language].get('liked', TE)
        index = f'{user_playlist.index(track_id) + 1}/{len(user_playlist)}'
        pid = bot.send_audio(audio=link, chat_id=call.message.chat.id, reply_markup=markup,
                             caption=f"{meta}\n{languages[user.language].get('from_pl', TE)}{pl_name}\n{index}").id
        sqlast_hope.set_user_attr(chat_id=call.message.chat.id, attr_name='player_id', value=pid)
        bot.answer_callback_query(callback_query_id=call.id, text=languages[user.language].get('downloaded', TE))
    sqlast_hope.set_user_attr(chat_id=call.message.chat.id, attr_name='track_id', value=track_id)
    sqlast_hope.set_user_attr(chat_id=call.message.chat.id, attr_name='playlist', value=playlist)


@bot.message_handler(content_types=['text', 'audio', 'photo', 'video', 'media', 'file', 'voice', 'video_note'])
def deleter(message):
    bot.delete_message(message.chat.id, message.id)


@bot.callback_query_handler(func=lambda call: call.data == 'del')
def del_player(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)


@bot.callback_query_handler(func=lambda call: call.data == 'raise_end')
def raise_end(call):
    bot.answer_callback_query(callback_query_id=call.id,
                              text=languages[sqlast_hope.users[call.message.chat.id].language].get('raise_end', TE))


@bot.callback_query_handler(func=lambda call: call.data.startswith('like'))
def like_track(call):
    user = sqlast_hope.users[call.message.chat.id]
    track_id = call.data.split(':')[1]
    row, col = map(int, call.data.split(':')[2].split(','))
    liked_tracks = user.get_liked()
    markup = call.message.reply_markup
    next_callback, prew_callback = None, None
    if track_id in liked_tracks:
        if track_id == user.track_id and user.playlist == 'liked':
            next_callback = f'play:{liked_tracks[liked_tracks.index(user.track_id) + 1]}::liked' if \
                liked_tracks.index(user.track_id) < len(liked_tracks) - 1 else "raise_end"
            prew_callback = f'play:{liked_tracks[liked_tracks.index(user.track_id) - 1]}::liked' if \
                liked_tracks.index(user.track_id) > 0 else "raise_end"
        like = '🤍'
        liked_tracks.remove(track_id)
        if track_id != user.track_id and user.playlist == 'liked':
            next_callback = f'play:{liked_tracks[liked_tracks.index(user.track_id) + 1]}::liked' if \
                liked_tracks.index(user.track_id) < len(liked_tracks) - 1 else "raise_end"
            prew_callback = f'play:{liked_tracks[liked_tracks.index(user.track_id) - 1]}::liked' if \
                liked_tracks.index(user.track_id) > 0 else "raise_end"
        bot.answer_callback_query(callback_query_id=call.id, text=languages[user.language].get('del_liked', TE))
    else:
        like = '❤️'
        liked_tracks.append(track_id)
        if user.playlist == 'liked':
            next_callback = f'play:{liked_tracks[liked_tracks.index(user.track_id) + 1]}::liked' if \
                liked_tracks.index(user.track_id) < len(liked_tracks) - 1 else "raise_end"
            prew_callback = f'play:{liked_tracks[liked_tracks.index(user.track_id) - 1]}::liked' if \
                liked_tracks.index(user.track_id) > 0 else "raise_end"
        bot.answer_callback_query(callback_query_id=call.id, text=languages[user.language].get('add_liked', TE))
    sqlast_hope.set_user_attr(chat_id=call.message.chat.id, attr_name='liked', value=user.pack_liked(liked_tracks))
    markup.keyboard[row][col] = types.InlineKeyboardButton(like, callback_data=f'like:{track_id}:{row},{col}')
    bot.edit_message_reply_markup(message_id=call.message.id, reply_markup=markup, chat_id=call.message.chat.id)
    if user.script == 'liked':
        main_markup = types.InlineKeyboardMarkup()
        for row_, elem in enumerate(liked_tracks):
            like_b = types.InlineKeyboardButton('❤️', callback_data=f'like:{elem}:{row_},1')
            main_markup.row(types.InlineKeyboardButton(music_api.get_metadata(elem),
                                                       callback_data=f'play:{elem}::liked'), like_b)
        main_markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE), callback_data='music'),
                        types.InlineKeyboardButton(languages[user.language].get('home', TE), callback_data='home'))
        bot.edit_message_text(reply_markup=main_markup, chat_id=call.message.chat.id, message_id=user.message_id,
                              text=languages[user.language].get('liked_text' if liked_tracks else 'empty_liked', TE))
    elif user.script.startswith('playlist_view') and track_id in user.get_playlists()[user.script.split('::')[1]]:
        pl_name = user.script.split('::')[1]
        markup = types.InlineKeyboardMarkup()
        texts = ['search_response_text', 'empty_response', 'search'] if len(user.script.split('::')) == 2 else \
            ['playlist_text', 'empty_playlist', 'playlists']
        response = user.get_playlists()[pl_name]
        u = False
        for row, elem in enumerate(response):
            u = True
            like_b = types.InlineKeyboardButton('❤️' if elem in liked_tracks else '🤍',
                                                callback_data=f'like:{elem}:{row},1')
            markup.row(types.InlineKeyboardButton(music_api.get_metadata(elem),
                                                  callback_data=f"play:{elem}::{pl_name}"), like_b)
        markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE),
                                              callback_data=texts[2]),
                   types.InlineKeyboardButton(languages[user.language].get('home', TE), callback_data='home'))
        pl_name = pl_name if pl_name != 'sysdata--lsr' else languages[user.language].get('lsr', TE)
        pl_name = '' if texts[2] == 'search' else pl_name
        try:
            bot.edit_message_text(chat_id=user.chat_id, message_id=user.message_id, reply_markup=markup,
                                  text=languages[user.language].get(texts[0] if u else texts[1], TE) + pl_name)
        except telebot.apihelper.ApiTelegramException:
            pass
    if user.playlist == 'liked' or track_id == user.track_id:
        cur_playlist = user.get_playlists()[user.playlist] if user.playlist != 'liked' else liked_tracks
        if not prew_callback:
            next_callback = f'play:{cur_playlist[cur_playlist.index(user.track_id) + 1]}::liked' if \
                cur_playlist.index(user.track_id) < len(cur_playlist) - 1 else "raise_end"
            prew_callback = f'play:{cur_playlist[cur_playlist.index(user.track_id) - 1]}::liked' if \
                cur_playlist.index(user.track_id) > 0 else "raise_end"
        try:
            markup = types.InlineKeyboardMarkup()
            markup.row(types.InlineKeyboardButton('⏮️', callback_data=prew_callback),
                       types.InlineKeyboardButton('➕', callback_data=f'to_pl:{user.track_id}'),
                       types.InlineKeyboardButton(like, callback_data=f'like:{user.track_id}:0,2'),
                       types.InlineKeyboardButton('⏭️', callback_data=next_callback))
            markup.row(types.InlineKeyboardButton(languages[user.language].get('close', TE), callback_data='del'))
            pl_name = user.playlist if user.playlist != 'sysdata--lsr' else languages[user.language].get('lsr', TE)
            pl_name = pl_name if pl_name != 'liked' else languages[user.language].get('liked', TE)
            index = f'{(cur_playlist.index(user.track_id)) + 1}/{len(cur_playlist)}'\
                if user.track_id in cur_playlist else languages[user.language].get('rem_from_pl', TE)
            bot.edit_message_caption(caption=f"{music_api.get_metadata(user.track_id)}\n"
                                             f"{languages[user.language].get('from_pl', TE)}{pl_name}\n{index}",
                                     message_id=user.player_id, chat_id=user.chat_id, reply_markup=markup)
        except telebot.apihelper.ApiTelegramException:
            pass


@bot.callback_query_handler(func=lambda call: call.data.startswith('new_pl'))
def create_playlist(call):
    user = sqlast_hope.users[call.message.chat.id]
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE), callback_data='playlists'),
               types.InlineKeyboardButton(languages[user.language].get('home', TE), callback_data='home'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup,
                          text=languages[user.language].get('new_pl_text', TE))
    bot.register_next_step_handler(call.message, pl_name_handler)


def pl_name_handler(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    user = sqlast_hope.users[message.chat.id]
    playlists = user.get_playlists()
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE), callback_data='playlists'),
               types.InlineKeyboardButton(languages[user.language].get('home', TE), callback_data='home'))
    if '::' in message.text or ';;' in message.text or 'sysdata' in message.text or message.text in playlists.keys():
        bot.register_next_step_handler(message, pl_name_handler)
        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=user.message_id, reply_markup=markup,
                                  text=languages[user.language].get('incorr_pl_name', TE))
        except telebot.apihelper.ApiTelegramException:
            pass
        return
    playlists[message.text] = {}
    sqlast_hope.set_user_attr(chat_id=message.chat.id, attr_name='playlists', value=user.pack_playlists(playlists))
    bot.edit_message_text(chat_id=message.chat.id, message_id=user.message_id, reply_markup=markup,
                          text=languages[user.language].get('created_pl_text', TE))


if __name__ == '__main__':
    try:
        bot.remove_webhook()
        print('initialize completed')
        bot.infinity_polling()
    except Exception as e:
        print(f'crushed: {e}')
        sqlast_hope.try_commit()
