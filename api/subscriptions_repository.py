class SubscriptionsRepository:
  def __init__(self, db):
    self.db = db

  def create(self, user_id, category_id):
    existing_subscription = self.select_user_subscription(user_id, category_id)

    if existing_subscription != None:
      return

    self.db.execute_with_cursor(lambda cursor: cursor.execute('''
      INSERT INTO 'subscriptions' (user_id, category_id) VALUES (?, ?)
    ''', (user_id, category_id)))

  def select_user_subscription(self, user_id, category_id):
    row = self.db.execute_with_cursor(lambda cursor: cursor.execute('''
      SELECT user_id, category_id FROM 'subscriptions' WHERE user_id = ? AND category_id = ?
    ''', (user_id, category_id)).fetchone())

    if row == None:
      return None

    return { 'user_id': row[0], 'category_id': row[1] }

  def select_user_subscriptions(self, user_id):
    rows = self.db.execute_with_cursor(lambda cursor: cursor.execute('''
      SELECT user_id, category_id FROM subscriptions WHERE user_id = ?
    ''', (user_id,)).fetchall())

    return list(map(lambda row: { 'user_id': row[0], 'category_id': row[1] }, rows))

  def delete_user_subscription(self, user_id, category_id):
    self.db.execute_with_cursor(lambda cursor: cursor.execute('''
      DELETE FROM 'subscriptions' WHERE user_id = ? AND category_id = ?
    ''', (user_id, category_id)))