import os
import requests
from telebot import TeleBot, types
import api

bot = TeleBot(os.environ['ACCESS_TOKEN'], parse_mode=None)

categories = requests.get(f"{os.environ['API_URL']}/categories").json()

subscribe_commands = [f"subscribe_{category['id']}" for category in categories]
unsubscribe_commands = [f"unsubscribe_{category['id']}" for category in categories]
show_commands = [f"show_{category['id']}" for category in categories]

@bot.message_handler(commands=['start'])
def start(message):
  user = api.create_user(message.from_user.id)

  if user == None:
    return

  markup = types.ReplyKeyboardMarkup()
  markup.add(types.KeyboardButton('Показать новости'))
  markup.add(types.KeyboardButton('Подписаться на категорию'))
  markup.add(types.KeyboardButton('Отписаться от категории'))

  bot.reply_to(message, "Привет! Используй кнопки для управления", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Подписаться на категорию')
def select_categories(message):
  categories_ids = api.get_user_categories(message.from_user.id)

  if categories_ids == None:
    return

  if len(categories_ids) == len(categories):
    return bot.send_message(message.chat.id, "Вы уже подписались на все категории новостей.")

  keyboard = types.InlineKeyboardMarkup()

  buttons = [types.InlineKeyboardButton(
    category['name'],
    callback_data=f"subscribe_{category['id']}") for category in categories if not category['id'] in categories_ids
  ]
  keyboard.add(*buttons)

  bot.reply_to(message, "Выберите категории новостей, которые вам интересны.", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in subscribe_commands)
def subscribe_to_category(call):
  category_id = call.data.split('subscribe_')[1]

  user = api.get_user_by_telegram_id(call.from_user.id)
  if user == None:
    return

  category = api.get_category_by_id(category_id)
  if category == None:
    return

  api.create_subscription(user['id'], category['id'])

  bot.answer_callback_query(call.id, f"Вы подписались на категорию {category['name']}")

@bot.message_handler(func=lambda message: message.text == 'Отписаться от категории')
def remove_categories(message):
  categories_ids = api.get_user_categories(message.from_user.id)

  if categories_ids == None:
    return

  if len(categories_ids) == 0:
    return bot.send_message(message.chat.id, "Вы ещё не подписались ни на одну категорию новостей.")

  keyboard = types.InlineKeyboardMarkup()

  buttons = [types.InlineKeyboardButton(
    category['name'],
    callback_data=f"unsubscribe_{category['id']}") for category in categories if category['id'] in categories_ids
  ]
  keyboard.add(*buttons)

  bot.reply_to(message, "Выберите категории новостей, от которых вы хотите отписаться.", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in unsubscribe_commands)
def unsubscribe_from_category(call):
  category_id = call.data.split('unsubscribe_')[1]

  user = api.get_user_by_telegram_id(call.from_user.id)
  if user == None:
    return

  category = api.get_category_by_id(category_id)
  if category == None:
    return

  api.delete_user_subscription(user['id'], category['id'])

  bot.answer_callback_query(call.id, f"Вы отписались от категории {category['name']}")

@bot.message_handler(func=lambda message: message.text == 'Показать новости')
def show_news(message):
  categories_ids = api.get_user_categories(message.from_user.id)

  if categories_ids == None:
    return

  if len(categories_ids) == 0:
    return bot.send_message(message.chat.id, "Вы ещё не подписались ни на одну категорию новостей.")

  keyboard = types.InlineKeyboardMarkup()

  buttons = [types.InlineKeyboardButton(
    category['name'],
    callback_data=f"show_{category['id']}") for category in categories if category['id'] in categories_ids
  ]
  keyboard.add(*buttons)

  bot.send_message(message.chat.id, f"Выберите категории новостей, которые требуется показать.", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in show_commands)
def show_category_news(call):
  category_id = call.data.split('show_')[1]

  user = api.get_user_by_telegram_id(call.from_user.id)
  if user == None:
    return

  category = api.get_category_by_id(category_id)
  if category == None:
    return

  news = api.get_news(category['api_name'])

  if news == None:
    return bot.send_message(call.message.chat.id, "Что-то пошло не так. Попробуйте позже")

  if len(news['articles']) == 0:
    return bot.send_message(call.message.chat.id, "Похоже, что новостей нет...")

  for article in news['articles']:
    bot.send_photo(
      call.message.chat.id,
      photo=article['urlToImage'],
      caption=f"{article['title']}\n\n{article['description']}\n\n{article['source']['name']}"
    )

bot.infinity_polling()

