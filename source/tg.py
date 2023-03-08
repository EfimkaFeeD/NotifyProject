import telebot
from telebot import types
from telegram.utils import config, get_languages, sqlast_hope


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
    markup.row(types.InlineKeyboardButton(languages[user.language].get('back', TE), callback_data='home'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                          text='В процессе деланья (нет)', reply_markup=markup)


if __name__ == '__main__':
    bot.remove_webhook()
    print('initialize completed')
    bot.infinity_polling()
