from flask import Flask, request
import requests
import os
from database import Database
from users_repository import UsersRepository
from categories_repository import CategoriesRepository
from subscriptions_repository import SubscriptionsRepository

app = Flask(__name__)

with Database(os.environ['DATABASE_NAME']) as db:
  users_repository = UsersRepository(db)
  categories_repository = CategoriesRepository(db)
  subscriptions_repository = SubscriptionsRepository(db)

  @app.route('/news', methods=['GET'])
  def get_news():
    category = request.args.get('category')

    if category == None:
      return "Category is required", 400

    news_response = requests.get(f"{os.environ['NEWS_API_URL']}?country=ru&apiKey={os.environ['NEWS_API_KEY']}&category={category}&pageSize=3")

    if news_response.status_code != 200:
      return "Something went wrong", news_response.status_code

    return news_response.json()

  @app.route('/users', methods=['POST'])
  def create_user():
    telegram_id = request.json.get('telegram_id')

    if telegram_id == None:
      return "Telegram id is required", 400

    users_repository.create(telegram_id)

    return { 'telegram_id': telegram_id }

  @app.route('/users', methods=['GET'])
  def get_user_by_telegram_id():
    telegram_id = request.args.get('telegram_id')

    if telegram_id == None:
      return "Telegram id is required", 400

    return users_repository.select_by_telegram_id(telegram_id)

  @app.route('/subscriptions', methods=['GET'])
  def get_subscriptions():
    user_id = request.args.get('user_id')

    if user_id == None:
      return "User id is required", 400

    return subscriptions_repository.select_user_subscriptions(user_id)

  @app.route('/subscriptions', methods=['POST'])
  def create_subscription():
    user_id = request.json.get('user_id')

    if user_id == None:
      return "User id is required", 400

    category_id = request.json.get('category_id')

    if category_id == None:
      return "Category id is required"

    subscriptions_repository.create(user_id, category_id)

    return { 'user_id': user_id, 'category_id': category_id }

  @app.route('/subscriptions', methods=['DELETE'])
  def delete_user_subscription():
    user_id = request.args.get('user_id')

    if user_id == None:
      return "User id is required", 400

    category_id = request.args.get('category_id')

    if category_id == None:
      return "Category id is required"

    subscriptions_repository.delete_user_subscription(user_id, category_id)

    return { 'user_id': user_id, 'category_id': category_id }

  @app.route('/categories', methods=['GET'])
  def get_categories():
    return categories_repository.select_all()

  @app.route('/categories/<id>', methods=['GET'])
  def get_category_by_id(id):
    category = categories_repository.select_by_id(id)

    if category == None:
      return "Not Found", 404

    return category

  if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030)