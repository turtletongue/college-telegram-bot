import requests
import os

def create_user(telegram_id):
  response = requests.post(f"{os.environ['API_URL']}/users", json={ 'telegram_id': telegram_id })

  if response.status_code != 200:
    return

  return response.json()

def create_subscription(user_id, category_id):
  response = requests.post(f"{os.environ['API_URL']}/subscriptions", json={
    'user_id': user_id,
    'category_id': category_id
  })

  if response.status_code != 200:
    return

  return response.json()

def delete_user_subscription(user_id, category_id):
  response = requests.delete(f"{os.environ['API_URL']}/subscriptions?user_id={user_id}&category_id={category_id}")

  if response.status_code != 200:
    return

  return response.json()

def get_news(category):
  response = requests.get(f"{os.environ['API_URL']}/news?category={category}")

  if response.status_code != 200:
    return

  return response.json()

def get_user_by_telegram_id(telegram_id):
  user_response = requests.get(f"{os.environ['API_URL']}/users?telegram_id={telegram_id}")

  if user_response.status_code != 200:
    return

  return user_response.json()[0]

def get_category_by_id(id):
  category_response = requests.get(f"{os.environ['API_URL']}/categories/{id}")
  
  if category_response.status_code != 200:
    return

  return category_response.json()

def get_user_categories(telegram_id):
  user = get_user_by_telegram_id(telegram_id)

  user_subscriptions = requests.get(f"{os.environ['API_URL']}/subscriptions?user_id={user['id']}")

  if user_subscriptions.status_code != 200:
    return

  subscribed_categories_ids = [subscription['category_id'] for subscription in user_subscriptions.json()]

  return subscribed_categories_ids